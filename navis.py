import click
import crud
import config
import requests
import ollama
from rich.panel import Panel
from rich.console import Console
from rich import box
from rich import print
from rich.align import Align
from pyfiglet import Figlet

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx) -> None:
    if ctx.invoked_subcommand is None:
        f = Figlet(font="slant")
        #print(f.renderText("NAVIS"))
        #print("Hi, I'm NAVIS!")
        console.print(Panel(
            Align.center(f.renderText("NAVIS")),
            title="NAVIS-cli",
            subtitle="Version 1.0",
            box=box.DOUBLE_EDGE))

cli.add_command(crud.run)
cli.add_command(config.config)