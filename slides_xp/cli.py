"""
CLI

Main entrypoint to the program.
"""

import asyncio
from importlib.metadata import version
from pathlib import Path

import click
from granian.constants import Interfaces
from granian.server.embed import Server

from slides_xp import make_app

PACKAGE = "slides_xp"

VERSION = version(PACKAGE)

HELP_TEXT = f"""
sxp

Slides XP CLI, version {VERSION}
"""


@click.command("sxp", help=HELP_TEXT, options_metavar="<options>")
@click.version_option(VERSION, package_name=PACKAGE)
@click.argument(
    "paths",
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        readable=True,
        path_type=Path,
    ),
    nargs=-1,
    required=True,
)
@click.option(
    "--theme",
    envvar="SXP_THEME",
    help="Theme directory to serve CSS stylesheets from",
)
@click.option(
    "-h",
    "--host",
    default="127.0.0.1",
    envvar="SXP_HOST",
    help="IP address to listen on",
)
@click.option(
    "-p",
    "--port",
    type=int,
    default=3000,
    envvar="SXP_PORT",
    help="Port to run server on",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Whether to enable Flask debug mode",
)
def cli(
    paths: tuple[Path, ...],
    *,
    theme: str | None,
    host: str,
    port: int,
    debug: bool,
):
    """
    Entrypoint to CLI.
    """
    app = make_app(list(paths), theme)

    if debug:
        app.run(host, port, True)
    else:
        from asgiref.wsgi import WsgiToAsgi

        server = Server(
            WsgiToAsgi(app),
            address=host,
            port=port,
            interface=Interfaces.ASGI,
        )
        asyncio.run(server.serve())
