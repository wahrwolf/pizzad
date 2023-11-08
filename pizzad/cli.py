from math import ceil
import click

from .calculations import calculate_pizzas, VALID_PORTION_SIZES
from .web.server import WebServer


def build_server_commands(server: WebServer):
    @click.group("server")
    def server_commands():
        pass

    @server_commands.command()
    @click.option('--port', type=int, default=5000,
                  help='Port number (default: 5000)')
    @click.option('--host', type=str, default='localhost',
                  help='Host name (default: localhost)')
    @click.option('--enable-debug', is_flag=True,
                  help='Enable debug mode')
    @click.option('--url-prefix', type=str, default='',
                  help='Proxy url prefix (default: "")')
    def run(host, port, enable_debug, url_prefix):
        try:
            server.setup(url_prefix)
            server.run(host=host, port=port, enable_debug=enable_debug)
        except Exception as error:
            click.echo(f"Could not start server due: {error}")

    return server_commands


def build_calculate_commands():
    default_portion = VALID_PORTION_SIZES[0]

    @click.group("calc")
    def calculate_commands():
        pass

    @calculate_commands.command()
    @click.argument('radius', type=float)
    @click.argument('number-of-people', type=int)
    @click.option('--portion-size', default=default_portion,
                  type=click.Choice(VALID_PORTION_SIZES),
                  help=f'Portion size (default: {default_portion})')
    @click.option('--use-long-format', is_flag=True,
                  help='Report in a more human readable format')
    def pizzas(radius, number_of_people, portion_size, use_long_format):
        """Calculate number of pizzas needed"""
        try:
            required_pizzas = calculate_pizzas(
                    radius, number_of_people, portion_size)
            if use_long_format:
                click.echo(f"Number of pizzas needed: {required_pizzas:.2f}")
            else:
                click.echo(ceil(required_pizzas))
        except ValueError as error:
            click.echo(f"Error: {error}")

    return calculate_commands


def build_cli(server: WebServer):
    @click.group()
    def cli():
        pass

    cli.add_command(build_server_commands(server))
    cli.add_command(build_calculate_commands())

    return cli
