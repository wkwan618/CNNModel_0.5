

import requests
import json
import jsonref
import ast
from typing import Literal
from pydantic import BaseModel
from commonPyLib.helpers.file import FileHelper

GetSchemaFromUnion = Literal["local", "server"]

class HttpRequestSchemaMapperItem(BaseModel):
    serverUrl: str
    path: str
    method: str

class FuncNameWithDes(BaseModel):
    name: str
    description: str


class OpenaiHttpToolSchema(BaseModel):
    httpRequestToolMapper: dict[str, HttpRequestSchemaMapperItem] = {}
    openaiToolsSchema: list[dict] = []
    functionNamesWithDescription: list[FuncNameWithDes] = []

    def append(
        self, 
        serverUrl: str, 
        path: str, 
        method: str, 
        operationId: str, 
        description: str, 
        requestBody: dict, 
    ):
        self.httpRequestToolMapper[operationId] = HttpRequestSchemaMapperItem(
            serverUrl=serverUrl,
            path=path,
            method=method,
        )
        self.openaiToolsSchema.append(
            {
                "type": "function",
                "function": {
                    "name": operationId,
                    "description": description,
                    "parameters": requestBody,
                }
            }
        )
        self.functionNamesWithDescription.append(FuncNameWithDes(name=operationId, description=description))

    def getOpenaiToolSchemaByFuncName(self, funcName: str) -> dict | None:
        for tool in self.openaiToolsSchema:
            if tool["function"]["name"] == funcName:
                return tool
        return None
    
    def getNameWithDescriptionByFuncName(self, funcName: str) -> FuncNameWithDes | None:
        for nameWithDes in self.functionNamesWithDescription:
            if nameWithDes.name == funcName:
                return nameWithDes
        return None
    
    def saveToJson(self, schemaFilePath: str, mapperFilePath: str):
        FileHelper.saveToJson(schemaFilePath, self.openaiToolsSchema)
        mappers = []
        for key, value in self.httpRequestToolMapper.items():
            mappers.append({
                "function": key,
                "method": value.method,
                "path": value.path,
                "baseUrl": value.serverUrl,
            })
        FileHelper.saveToJson(mapperFilePath, mappers)


class OpenapiSpecProcessor:

    @staticmethod
    def destructRef(schema: dict) -> dict:
        return jsonref.replace_refs(schema, merge_props=True,)
    
    @staticmethod
    def removeUnneededFields(schema: dict) -> dict:
        for path, value in schema['paths'].items():
            for method, methodValue in value.items():
                del schema['paths'][path][method]['responses']
        schema = str(schema)
        schema = ast.literal_eval(schema)
        del schema['components']
        return schema
    
    @staticmethod
    def cleanSchema(schema: dict, apiBaseUrl: str) -> dict:
        schema = OpenapiSpecProcessor.destructRef(schema)
        schema = OpenapiSpecProcessor.removeUnneededFields(schema)
        schema["servers"] = [{"url": apiBaseUrl}]
        return schema

    @staticmethod
    def getFromServer(url, apiBaseUrl: str) -> dict:
        response = requests.get(url)
        schema = response.json()
        return OpenapiSpecProcessor.cleanSchema(schema, apiBaseUrl)

    @staticmethod
    def getFromLocal(jsonFilePath: str, apiBaseUrl: str) -> dict:
        with open(jsonFilePath, "r") as f:
            schema = json.load(f)
        f.close()
        return OpenapiSpecProcessor.cleanSchema(schema, apiBaseUrl)
    
    @staticmethod
    def toOpenAIToolsSchema(openApiSchema: dict) -> OpenaiHttpToolSchema:
        httpToolSchema = OpenaiHttpToolSchema()
        ###
        serverUrl = openApiSchema["servers"][0]["url"]
        for path, pathValue in openApiSchema["paths"].items():
            for method, methodValue in pathValue.items():
                operationId:str = methodValue.get("operationId", "").capitalize()
                description = methodValue.get("description", "")
                params = methodValue.get("parameters", [])
                reqBodySchema = (
                    methodValue.get("requestBody", {})
                    .get("content", {})
                    .get("application/json", {})
                    .get("schema")
                )
                param_properties = {
                    param["name"]: param["schema"]
                    for param in params
                    if "schema" in param
                }
                reqBodySchema["properties"]["parameters"] = {
                    "type": "object",
                    "properties": param_properties,
                }
                httpToolSchema.append(
                    serverUrl,
                    path,
                    method,
                    operationId,
                    description,
                    reqBodySchema,
                )
        return httpToolSchema


        
