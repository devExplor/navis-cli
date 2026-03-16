import click
import navis
import os


currentProjectVar = ""

#@navis.project.command()
#@click.pass_context
def createDir(ctx, title:str):
    config = ctx.obj
    project_path = config["Project"]["path"]
    directory = os.path.join(project_path, title)
    os.makedirs(directory, exist_ok=True)
    print("Project created")
    print(directory)
    return directory

def setProject(setCurrentProject):
    # Festlegen des aktuellen Projekts
    global currentProjectVar
    currentProjectVar = setCurrentProject
    return "project set successful"