import os
import click
import json
import project_manager
import webbrowser

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
    return directoryProject

def searchFor(searchTerm):
    # Define the search term
    search_term = searchTerm
    
    # Construct the URL
    url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
    
    # Open in the default browser
    webbrowser.open(url)
    return "opened in browser"

def executeAICommand(ctx, data):
    if data["type"] == "file":
        fileName = data["name"]
        if data["folder"] == "currentProject":
            if project_manager.currentProjectVar == "":
                return "You have to set the current Project first"
            projectName = project_manager.currentProjectVar
        else:
            projectName = data["folder"]

        filePath = createFile(ctx, fileName, projectName)
        return f"File created successful. Path: {filePath}"
    
    if data["type"] == "folder":
        if data["folder"] == "currentProject":
            if project_manager.currentProjectVar == "":
                return "You have to set the current Project first"
            projectname = project_manager.currentProjectVar
        else:
            projectname = data["folder"]
        folderPath = createFolder(ctx, data["name"], projectname)
        return f"Folder created successful. Path: {folderPath}"
    
    if data["type"] == "newProject":
        dirName = data["name"]
        newDirectory = project_manager.createDir(ctx, dirName)
        return f"Project created successful. Path: {newDirectory}"
    
    if data["type"] == "openProjectfolder":
        if data["name"] == "currentProject":
            if project_manager.currentProjectVar == "":
                return "You have to set the current Project first"
            projectName = project_manager.currentProjectVar
        else:
            projectName = data["name"]
        directoryProject = openProjectFolder(ctx, projectName)
        return directoryProject
    
    if data["type"] == "setCurrentProject":
        name = data["name"]
        status = project_manager.setProject(name)
        return status
    
    if data["type"] == "searchInBrowser":
        term = data["term"]
        status = searchFor(term)
        return status
