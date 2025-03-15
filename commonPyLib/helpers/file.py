
from pydantic import BaseModel
import json
import os

class PathBase(BaseModel):
    folderRootPath: str

    def __str__(self) -> str:
        return self.folderRootPath
    

class BloombergDataFolderPath(PathBase):
    modelDataField: str = None
    productSegmentMapper: str = None

    def __init__(self, folderRootPath: str) -> None:
        super().__init__(
            folderRootPath=folderRootPath,
            modelDataField=f"{folderRootPath}/modelDataField",
            productSegmentMapper=f"{folderRootPath}/productSegmentMapper"
        )


class MlChartFolderPath(PathBase):
    models: str = None
    trainingImgs: str = None
    prodImgs: str = None
    devProject: str = None
    rawData: str = None

    def __init__(self, folderRootPath: str) -> None:
        super().__init__(
            folderRootPath=folderRootPath,
            models=f"{folderRootPath}/models",
            trainingImgs=f"{folderRootPath}/trainingImgs",
            prodImgs=f"{folderRootPath}/prodImgs",
            devProject=f"{folderRootPath}/devProject",
            rawData=f"{folderRootPath}/rawData"
        )

class AppFolderPath:
    __rootPath = "./files"
    localDependence = f"{__rootPath}/localDependence"
    temp = f"{__rootPath}/temp"
    boosted = f"{__rootPath}/boosted"
    bloomberg = BloombergDataFolderPath(f"{__rootPath}/bloomberg")
    dcf = f"{__rootPath}/dcf"
    youTubeVideo = f"{__rootPath}/youTubeVideo"
    mlChart = MlChartFolderPath(f"{__rootPath}/mlChart")
    # appOneDriver = f"{__rootPath}/appOneDriver"
    # appTwoDriver = AppTwoDriver( f"{__rootPath}/appTwoDriver")

    @staticmethod
    def getMLChartProjectFolderPath(projectName: str) -> tuple[str, str, str, str, str]:
        projectFolderPath = f"{AppFolderPath.mlChart.devProject}/{projectName}"
        chartsFolderPath = f"{projectFolderPath}/charts"
        modelsFolderPath = f"{projectFolderPath}/models"
        rawDataFolder = f"{AppFolderPath.mlChart.rawData}"
        processedDataFile = f"{projectFolderPath}/processedData.json"
        return (
            projectFolderPath,
            chartsFolderPath,
            modelsFolderPath,
            rawDataFolder,
            processedDataFile
        )


class FileHelper:

    @staticmethod
    def isFileExist(filePath: str) -> bool:
        return os.path.exists(filePath)
    
    @staticmethod
    def loadFromJson(filePath: str, defaultValue = None):
        if FileHelper.isFileExist(filePath):
            with open(filePath, "r") as f:
                return json.load(f)
        else:
            return defaultValue
        
    @staticmethod
    def saveToJson(filePath: str, data: dict, indent: int | None = 4):
        with open(filePath, "w") as f:
            json.dump(data, f, indent=indent)
        f.close()

    @staticmethod
    def createFolderIfNotExists(fullPath: str):
        if not os.path.exists(fullPath):
            os.makedirs(fullPath)