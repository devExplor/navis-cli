import os
import click
import json

def clean_json(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    text = text.replace("json", "", 1).strip()

    return text

def createFolder(ctx, title:str, currentProject):
    config = ctx.obj
    project_path = config["Project"]["path"]
    directoryProject = os.path.join(project_path, currentProject)
    directory = os.path.join(directoryProject, title)
    os.makedirs(directory, exist_ok=True)
    print("Folder created")
    return directory

def createFile(ctx, filename:str, currentProject:str):
    config = ctx.obj
    project_path = config["Project"]["path"]
    directoryProject = os.path.join(project_path, currentProject)
    directory = os.path.join(directoryProject, filename)
    with open(directory, "w", encoding="utf-8") as datei:
        datei.write("New file created by Navis\n")
    print(f"File created: {directory}")
    return directory

def openProjectFolder(ctx, currentProject):
    config = ctx.obj
    project_path = config["Project"]["path"]
    directoryProject = os.path.join(project_path, currentProject)
    os.system(rf'xdg-open {directoryProject}')
    print("Folder opened")


def executeAICommand(ctx, data):
    if data["type"] == "file":
        fileName = data["name"]
        folderName = data["folder"]

        filePath = createFile(ctx, fileName, folderName)
        return f"File created seuccesfuly. Path: {filePath}"
    if data["type"] == "folder":
        folderPath = createFolder(ctx, data["name"], "FirstProject")
        return f"Folder created seuccesfuly. Path: {folderPath}"