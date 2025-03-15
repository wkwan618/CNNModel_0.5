# ML Chart Server

A machine learning system for predicting stock price movements using chart image analysis. This project converts stock price data into visual chart representations, processes them into tensor format, and uses a CNN model to predict whether prices will go up or down.

## Table of Contents

- [System Overview](#system-overview)
- [System Architecture](#system-architecture)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Chart Image Processing](#chart-image-processing)
- [Model Architecture](#model-architecture)
- [Training Process](#training-process)
- [Label Encoding](#label-encoding)
- [Dataset Preparation](#dataset-preparation)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Comparison with Stock_CNN-main](#comparison-with-stock-cnn-main)

## System Overview

ML Chart Server converts historical stock price data into standardized chart images and uses a convolutional neural network (CNN) to predict future price movements. Key features:
- *****
- Converts stock data to visual charts
- Processes charts into tensor representations
- Binary classification (Up/Down) of future price movements
- Provides prediction probabilities via API
- Works with variable time horizons (5, 20, or 60 day lookbacks)

## System Architecture

The system follows a well-structured architecture:

1. **FastAPI Backend**: `main.py` sets up a FastAPI server with endpoints for retrieving predictions and chart images.

2. **Data Processing Pipeline**:
   - Data downloading: `dataDownloader.ipynb` 
   - Data processing: `processDataToGraphData.py`
   - Chart generation: `createChart.py`
   - Image transformation: `chatTransformer.py`

3. **ML Training System**:
   - Model definition: `cnn5to5.py`
   - Training loop: `trainner.py`
   - Training workflow: `trainAndRun.ipynb`

4. **Prediction Service**:
   - API endpoint `/getPrediction`
   - API endpoint `/getPredictionImg/{imgID}`

## Data Processing Pipeline

The data processing flow works as follows:

1. **Raw Data Acquisition**:
   - CSV files with historical price data are loaded
   - Moving averages are calculated

2. **Data Structuring**: `processDataToGraphData.py` converts raw data into structured format:
   ```python
   graphData[fileName] = {
       'initialDate': initialDate,
       'asOfDate': asOfDate,
       'predictionDate': predictionDate,
       'asOfDateClose': asOfDateClose,
       'predictionClose': predictionClose,
       'change': change,  # Target variable - price change percentage
       'dataObj': dataObj,
   }
   ```

3. **Chart Generation**: `createChart.py` uses mplfinance to create standardized charts:
   ```python
   createOneChart(
       tradingDates = rowData["dataObj"]["tradingDate"][0:lookbackDays],
       closes = rowData["dataObj"]["close"][0:lookbackDays],
       # ...other data...
       folderPath = chartsFolderPath,
       fileName = fileName
   )
   ```

4. **Image Transformation**: `chatTransformer.py` converts charts to tensors:
   ```python
   vectorImage = transformOneImage(lookbackDays, fileName, chartsFolderPath, fileExtension)
   ```

## Chart Image Processing

Charts are processed into a standardized format suitable for the CNN model:

1. **Image Transformation Pipeline**:
   ```python
   imageTransform = transforms.Compose([
       transforms.Grayscale(num_output_channels=1),
       transforms.Resize(resizer),
       transforms.ToTensor(),
       transforms.Lambda(lambda x: binarize(x))
   ])
   ```

2. **Resizing Based on Lookback Period**:
   - 5-day lookback: (32, 15)
   - 20-day lookback: (64, 60)
   - 60-day lookback: (96, 180)

3. **Binarization**: Converting grayscale to binary (black and white)
   ```python
   def binarize(tensor, threshold=0.5):
       return (tensor > threshold).float()
   ```

## Model Architecture

The CNN model architecture (`cnn5to5.py`) consists of:

```python
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(1, 64, (5, 3), padding=(2, 1), stride=(1, 1), dilation=(1, 1))),
            ('BN', nn.BatchNorm2d(64, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1)))
        ]))
        
        self.conv2 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(64, 128, (5, 3), padding=(2, 1), stride=(1, 1), dilation=(1, 1))), 
            ('BN', nn.BatchNorm2d(128, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) 
        ]))

        self.DropOut = nn.Dropout(p=0.5)
        self.FC = nn.Linear(15360, 2)
        self.Softmax = nn.Softmax(dim=1)
```

Key components:
- Input: Binary chart images (1 channel)
- Two convolutional layers with batch normalization
- Dropout (p=0.5) to prevent overfitting
- Fully connected layer with 2 outputs (Up/Down)
- Softmax activation for probability outputs

## Training Process

The model training process in `trainner.py`:

1. **Dataset Preparation**:
   ```python
   dataset = CustomDataset(processedData)
   trainSize = int(0.8 * len(dataset)) 
   valSize = len(dataset) - trainSize
   trainSet, validSet = random_split(dataset, [trainSize, valSize])
   ```

2. **Training Configuration**:
   ```python
   criterion = nn.CrossEntropyLoss()
   optimizer = optim.Adam(model.parameters(), lr=learningRate)
   ```

3. **Training Loop**:
   ```python
   for epoch in range(epochs):
       model.train()
       # Training code...
       
       # Validation code...
       if val_loss < best_val_loss:
           best_val_loss = val_loss
           patience_counter = 0
           torch.save(model.state_dict(), modelOutputPath)
   ```

4. **Early Stopping**: Training stops when validation loss stops improving after a set number of epochs.

## Label Encoding

Price movements are encoded as binary classification labels:

1. **Calculating Price Change**:
   ```python
   change = (predictionClose - asOfDateClose) / asOfDateClose
   ```

2. **Binary Classification Labels**:
   ```python
   y = [1, 0] if y >= 0 else [0, 1]
   ```
   - `[1, 0]` represents price increase (or no change)
   - `[0, 1]` represents price decrease

3. **During Prediction**:
   ```python
   prediction = "Up" if upProbability >= downProbability else "Down"
   ```

## Dataset Preparation

Chart data and labels are prepared for training in the following manner:

1. **Data Storage Format**: JSON file with the structure:
   ```json
   [
     {
       "x": [[ ... binary image tensor values ... ]],
       "y": [1, 0]  // or [0, 1] for "down" prediction
     },
     // More samples...
   ]
   ```

2. **Custom PyTorch Dataset**:
   ```python
   class CustomDataset(Dataset):
       def __init__(self, data):
           self.data = data

       def __len__(self):
           return len(self.data)

       def __getitem__(self, idx):
           sample = self.data[idx]
           x = torch.tensor(sample["x"], dtype=torch.float32)
           y = torch.tensor(sample["y"], dtype=torch.float32)
           return x, y
   ```

3. **Data Flow for Training**:
   ```
   Chart Images → Tensors → List of {"x": tensor, "y": label} → JSON File
       ↓
   JSON File loaded → CustomDataset.__init__(data) 
       ↓
   DataLoader created with Dataset
       ↓
   Training loop: for x, y in trainLoader
       ↓ 
   Model: outputs = model(x) → Loss: loss = criterion(outputs, y)
   ```

## API Endpoints

The system exposes two main API endpoints:

1. **Get Prediction**:
   ```
   POST /getPrediction
   ```
   - Input: Stock ticker and optional as-of date
   - Output: Prediction object with probabilities and direction

2. **Get Prediction Image**:
   ```
   GET /getPredictionImg/{imgID}
   ```
   - Input: Image ID from prediction response
   - Output: Chart image used for prediction

Response format:
```json
{
  "graphDataImgID": "string",
  "dayOfPrediction": 5,
  "upProbability": 0.75,
  "downProbability": 0.25,
  "inputDateFrom": "2023-01-01",
  "inputDateTo": "2023-01-05",
  "prediction": "Up"
}
```

## Getting Started

### Prerequisites

- Python 3.7+
- Required packages (see requirements.txt)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Training a Model

1. Prepare historical price data in CSV format
2. Run the data processing notebook:
   ```
   jupyter notebook trainAndRun.ipynb
   ```
3. Adjust training parameters as needed and run the training cells

### Running the API Server

```
python main.py
```

The server will start on port 5000 by default.

### Making Predictions

```python
import requests
import json

response = requests.post(
    "http://localhost:5000/getPrediction",
    json={"ticker": "AAPL"}
)

prediction = response.json()
print(f"Prediction: {prediction['prediction']}")
print(f"Up probability: {prediction['upProbability']}")
print(f"Down probability: {prediction['downProbability']}")
```

## Comparison with Stock_CNN-main

This section presents a detailed comparison between the ML Chart Server and Stock_CNN-main implementations, which are both systems for predicting stock price movements using chart images.

### Architecture Comparison

#### ML Chart Server
- **Model Structure**: 2 convolutional layers with batch normalization
- **Layer Progression**: 1 → 64 → 128 channels
- **Activation**: Standard ReLU activations
- **Convolution Parameters**: 
  - Stride: (1,1)
  - Dilation: (1,1)
  - Padding: (2,1)
- **Final Feature Vector**: 15,360 features

#### Stock_CNN-main
- **Model Structure**: 3 convolutional layers with batch normalization
- **Layer Progression**: 1 → 64 → 128 → 256 channels
- **Activation**: LeakyReLU (negative_slope=0.01)
- **Convolution Parameters**:
  - Stride: (3,1) - Larger vertical steps
  - Dilation: (2,1) - Expanded receptive field
  - Padding: (12,1) - Much larger vertical padding
- **Final Feature Vector**: 46,080 features (3x larger)

### Data Processing & Image Handling

#### ML Chart Server
- **Image Sizes**: Different sizes based on lookback period
  - 5-day: (32, 15)
  - 20-day: (64, 60)
  - 60-day: (96, 180)
- **Data Storage**: Stores processed data as JSON with image tensors and labels
- **Model Handling**: Uses same 2-layer model architecture for all lookback periods

#### Stock_CNN-main
- **Image Sizes**: Same size definitions, but always reshapes to (64,60)
  ```python
  IMAGE_WIDTH = {5: 15, 20: 60, 60: 180}
  IMAGE_HEIGHT = {5: 32, 20: 64, 60: 96}
  ```
- **Data Storage**: Uses binary memory-mapped files (.dat) for image storage
- **Reshaping**: Forces all inputs to same dimensions
  ```python
  x = x.reshape(-1,1,64,60)
  ```
- **Focus**: Primarily focused on 20-day prediction period in the implementation

### Training Approach

#### ML Chart Server
- **Training/Validation Split**: 80/20
- **Early Stopping**: Implemented with patience parameter
- **Optimizer**: Adam with customizable learning rate
- **Mixed Precision**: Supports mixed precision training with CUDA

#### Stock_CNN-main
- **Training/Validation Split**: 70/30
- **Multi-GPU Support**: Implemented for faster training
- **ONNX Export**: Supports exporting models to ONNX format
- **Batch Sizes**: Larger (128 for training, 256 for validation)

### Prediction & Classification

#### ML Chart Server
- **Binary Classification**: Up/Down prediction
- **Label Encoding**: 
  ```python
  y = [1, 0] if y >= 0 else [0, 1]  # [Up, Down]
  ```
- **Prediction Endpoint**: Provides REST API endpoint for predictions

#### Stock_CNN-main
- **Same Classification Approach**: Up/Down prediction
- **Threshold Adjustment**: Uses 0.58 as threshold (not just 0.5)
  - "We choose the threshold (for the predict logit) as 0.58"
- **Performance Analysis**: More focus on backtesting performance

### Integration & Code Reuse

- **Shared Components**: Stock_CNN-main actually imports and reuses parts of the ML Chart Server codebase
  ```python
  # Add the image generation codebase to Python path
  IMAGE_GEN_PATH = "/Users/warrenkwan/Documents/Programs/mlChartServer - prod - 0.5/app"
  sys.path.append(IMAGE_GEN_PATH)
  ```
- **Data Generation**: Stock_CNN-main leverages ML Chart Server's chart generation capabilities
- **Adaptation**: Stock_CNN-main adapts ML Chart Server's output to its own format

### Architectural Philosophy Differences

#### ML Chart Server
- **Production Focus**: Designed as a web service with API endpoints
- **Flexibility**: Handles different lookback periods natively
- **Simplicity**: More straightforward model architecture

#### Stock_CNN-main
- **Research Focus**: Implementation of an academic paper
- **Complexity**: Deeper model with more aggressive parameter choices
- **Analysis**: More tools for performance analysis and visualization

### Convolution Parameter Impact

The parameter differences in convolution layers reflect fundamentally different approaches to processing chart images:

- **ML Chart Server**: More conservative approach that preserves detail throughout network
- **Stock_CNN-main**: More aggressive downsampling vertically with expanded receptive field, suggesting a belief that:
  1. Broad pattern recognition is more important than fine detail
  2. Relationships between distant price levels matter more than local fluctuations
  3. Extreme prices (highs/lows) deserve special attention (via extensive padding)

These findings demonstrate two different but effective approaches to the same problem of predicting stock price movements from chart images, with ML Chart Server focusing on production deployment and Stock_CNN-main on research implementation.

## License

[Specify your license here]

## Acknowledgments

[Any acknowledgments] 