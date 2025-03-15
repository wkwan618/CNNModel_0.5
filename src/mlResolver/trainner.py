
import torch.optim as optim
import torch.nn as nn
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torch import amp

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





def modelTrainer(model, processedData: list, epochs, learningRate, batchSize, patience, modelOutputPath: str):

    use_amp = torch.cuda.is_available()
    device = torch.device("cuda" if use_amp else "cpu")
    print(f"Using device: {device}")
    model.to(device)

    if use_amp:
        torch.backends.cudnn.benchmark = True  

    # Prepare dataset
    dataset = CustomDataset(processedData)
    trainSize = int(0.8 * len(dataset)) 
    valSize = len(dataset) - trainSize
    trainSet, validSet = random_split(dataset, [trainSize, valSize])

    trainLoader = DataLoader(trainSet, batch_size=batchSize, shuffle=True)
    validLoader = DataLoader(validSet, batch_size=batchSize, shuffle=False)

    # Move loss function to the correct device
    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = optim.Adam(model.parameters(), lr=learningRate)

    scaler = amp.GradScaler(device=device)

    best_val_loss = float('inf')
    patience_counter = 0

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        for x, y in trainLoader:
            x, y = x.to(device), y.to(device)

            optimizer.zero_grad()
            with amp.autocast(device_type=device.type):
                outputs = model(x)
                outputs = outputs.squeeze(1)
                loss = criterion(outputs, y)

            if device == 'cuda':
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
            else:
                loss.backward()
                optimizer.step()

            running_loss += loss.item()

        train_loss = running_loss / len(trainSet)

        # Validation loop
        correct = 0
        total = 0
        val_loss = 0.0
        model.eval()

        with torch.no_grad():
            for x, y in validLoader:
                x, y = x.to(device), y.to(device)

                with amp.autocast(device_type=device.type):
                    outputs = model(x)
                    outputs = outputs.squeeze(1)
                    loss = criterion(outputs, y)

                val_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                y = y.argmax(dim=1)
                total += y.size(0)
                correct += (predicted == y).sum().item()

        val_loss /= len(validSet)   
        accuracy = 100 * correct / total

        if (epoch + 1) % max(epochs // 5, 1) == 0 or epoch == epochs - 1:
            print(f"Epoch [{epoch + 1} / {epochs}]:")
            print(f'Train Loss: {train_loss:.4f}')
            print(f'Val Loss: {val_loss:.4f}')
            print(f'Accuracy: {accuracy:.2f}%')

        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), modelOutputPath)
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping triggered at epoch {epoch + 1} / {epochs}:")
                print(f'Train Loss: {train_loss:.4f}')
                print(f'Val Loss: {val_loss:.4f}')
                print(f'Accuracy: {accuracy:.2f}%')
                break

    print('Training complete')
    torch.save(model.state_dict(), modelOutputPath)


