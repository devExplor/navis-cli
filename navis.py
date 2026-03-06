import os
import click
import crud
import config
import project_manager
import requests
import time
import ollama
from ollama import Client
from ollama import chat
import subprocess
from rich.panel import Panel
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich import box
from rich import print
from rich.align import Align
from pyfiglet import Figlet
from config import load_config
from pathlib import Path
from platformdirs import user_config_dir
from prompt_toolkit import PromptSession
import functional_manager

console = Console()
session = PromptSession()

#Navis
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx) -> None:
    ctx.obj = load_config()
    if ctx.invoked_subcommand is None:
        f = Figlet(font="slant")
        #print(f.renderText("NAVIS"))
        #print("Hi, I'm NAVIS!")
        console.print(Panel(
            Align.center(f.renderText("NAVIS")),
            title="NAVIS-cli",
            subtitle="Version 1.0",
            box=box.DOUBLE_EDGE))
        while True:
            try:
                #console.print("[bold dark_magenta]You> [/bold dark_magenta]", end='')
                user_input = console.input("[bold dark_magenta]You> [/bold dark_magenta]")
                if user_input.lower() in ["exit", "quit"]:
                    console.print("\n[bold red]NAVIS shutting down...[/bold red]")
                    break
                #client = Client(
                #     host=ctx.obj["Model"]["apiURL"],
                #     headers={'x-some-header': 'some-value'})
                #response = client.chat(model=ctx.obj["Model"]["modelName"], messages=[
                #    {
                #        'role': 'user',
                #        'content': user_input,
                #        },
                #        ])
                stream = chat(
                    model=ctx.obj["Model"]["modelName"],
                    messages=[{'role': 'user', 'content': user_input}],
                    stream=True,)
                #print(response.message.content)
                modelName = ctx.obj["Model"]["modelName"]
                console.print(f"[bold green]{modelName}> [/bold green]", end='')
                for chunk in stream:
                    console.print(chunk['message']['content'], end='')

                # Live Panel für dynamische Anzeige
                #buffer = ""  # gesamte Antwort
                #with Live(Panel(Markdown(buffer), title=modelName, border_style="green", expand=False), refresh_per_second=20) as live:
                #    for chunk in stream:
                #        content = chunk['message']['content']
                #        # Wörter nicht mitten brechen: Wort-für-Wort anhängen
                #        for word in content.split(" "):
                #            last_line = buffer.split("\n")[-1] if buffer else ""
                #            if len(last_line) + len(word) + 1 > console.width - 4:  # -4 für Panel-Rand
                #                buffer += "\n"
                #                if buffer and not buffer.endswith("\n"):
                #                    buffer += " "
                #                    buffer += word
                # Markdown Panel live updaten
                #live.update(Panel(Markdown(buffer), title=f"[bold green]{modelName}>[/bold green]", border_style="green", expand=False))
                #time.sleep(0.01)  # realistisches Tippen

                console.print()
            except KeyboardInterrupt:
                console.print("\n[red]Interrupted[/red]")
            except EOFError:
                break

#Config
@click.group()
def config():
    pass

@config.command()
def path():
    config_file = getConfigPath()
    print(config_file)

@config.command()
def edit():
    config_file = getConfigPath()
    subprocess.run(["nano", str(config_file)])
    

def getConfigPath():
    APP_NAME = "navis"
    config_dir = Path(user_config_dir(APP_NAME))
    config_file = config_dir / "config.toml"
    return config_file

#Project
@click.group()
@click.pass_context
def project(ctx):
    pass


@project.command()
@click.argument("title")
@click.pass_context
def create(ctx, title:str):
    #project_manager.createDir(ctx, title)
    config = ctx.obj
    project_path = config["Project"]["path"]
    directory = os.path.join(project_path, title)
    os.makedirs(directory, exist_ok=True)

    print("Project created")
    print(directory)

@click.group()
@click.pass_context
def function(ctx):
    pass

@function.command()
@click.argument("projectname")
@click.pass_context
def openFolder(ctx, projectname:str):
    functional_manager.openProjectFolder(ctx, projectname)

@function.command()
@click.argument("filename")
@click.pass_context
def fileCreate(ctx, filename:str):
    functional_manager.createFile(ctx, filename, "FirstProject")

@function.command()
@click.argument("title")
@click.pass_context
def folderCreate(ctx, title:str):
    functional_manager.createFolder(ctx, title, "FirstProject")

#add Command
cli.add_command(crud.run)
cli.add_command(config)
cli.add_command(project)
cli.add_command(function)