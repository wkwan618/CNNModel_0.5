

import os
from PIL import Image
from torchvision import transforms



def binarize(tensor, threshold=0.5):
    return (tensor > threshold).float()


def getImageTransform(lookbackDays):
    if lookbackDays not in [5, 20, 60]: raise Exception(f"lookbackDays must be 5, 20, or 60, but got {lookbackDays}")
    resizer = (32, 15)
    if lookbackDays == 20:
        resizer = (64, 60)
    if lookbackDays == 60:
        resizer = (96, 180)
    imageTransform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize(resizer),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: binarize(x))
    ])
    return imageTransform



def transformOneImage(lookbackDays: int, fileName: str, chartsFolderPath: str, fileExtension: str = ".png",) -> list:
    imageTransform = getImageTransform(lookbackDays)
    fileNameWithExtension = f"{fileName}{fileExtension}"
    if fileNameWithExtension.endswith(fileExtension) == False: raise Exception(f"File {fileNameWithExtension} is not a {fileExtension} file")
    fullPath = os.path.join(chartsFolderPath, fileNameWithExtension)
    image = Image.open(fullPath)
    vectorImage = imageTransform(image)
    vectorImage = vectorImage * 255
    return vectorImage


def chartDataTransformers(lookbackDays: int, graphData: dict, chartsFolderPath: str, fileExtension: str = ".png",) -> list:
    processedData = []
    for fileName, value in graphData.items():
        vectorImage = transformOneImage(lookbackDays, fileName, chartsFolderPath, fileExtension)
        y = value["change"]
        y = [1, 0] if y >= 0 else [0, 1]
        obj = {"x": vectorImage.tolist(), "y": y}
        processedData.append(obj)
    return processedData

