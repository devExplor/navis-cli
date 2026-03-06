import click
import navis
import os

#@navis.project.command()
@click.pass_context
def createDir(ctx, title:str):
    config = ctx.obj
    project_path = config["Project"]["path"]
    directory = os.path.join(project_path, title)
    os.makedirs(directory, exist_ok=True)
    print("Project created")