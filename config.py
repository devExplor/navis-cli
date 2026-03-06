from pathlib import Path
from platformdirs import user_config_dir
import tomllib
import click

APP_NAME = "navis"

config_dir = Path(user_config_dir(APP_NAME))
config_file = config_dir / "config.toml"


def create_default_config():
    config_dir.mkdir(parents=True, exist_ok=True)

    config_file.write_text("""
[general]
username = "user"

[Model]
apiURL = "http://localhost:11434"
modelName = "PLACEHOLDER"

[Project]
path = "/home"
""")


def load_config():

    if not config_file.exists():
        create_default_config()

    with open(config_file, "rb") as f:
        return tomllib.load(f)


@click.command()
def config_show():
    print(config_file)