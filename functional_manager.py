import os
import click

def createFolder(ctx, title:str, currentProject):
    config = ctx.obj
    project_path = config["Project"]["path"]
    directoryProject = os.path.join(project_path, currentProject)
    directory = os.path.join(directoryProject, title)
    os.makedirs(directory, exist_ok=True)
    print("Folder created")

def createFile(ctx, filename:str, currentProject:str):
    config = ctx.obj
    project_path = config["Project"]["path"]
    directoryProject = os.path.join(project_path, currentProject)
    directory = os.path.join(directoryProject, filename)
    with open(directory, "w", encoding="utf-8") as datei:
        datei.write("New file created by Navis\n")
    print(f"File created: {directory}")

def openProjectFolder(ctx, currentProject):
    config = ctx.obj
    project_path = config["Project"]["path"]
    directoryProject = os.path.join(project_path, currentProject)
    os.system(rf'xdg-open {directoryProject}')
    print("Folder opened")