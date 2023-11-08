import click

from pizzad.web.server import WebServer
from .server import build_server_commands
from .calculate import build_calculate_commands


def build_cli(server: WebServer):
    @click.group()
    def cli():
        pass

    cli.add_command(build_server_commands(server))
    cli.add_command(build_calculate_commands())

    return cli
