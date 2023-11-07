from math import ceil
import click

from .calculations import calculate_pizzas, VALID_PORTION_SIZES
from .webapp import WebServer


def build_order_commands():
    pass


def build_serve_commands(server: WebServer):
    @click.group()
    def serve_commands():
        pass

    @serve_commands.command()
    @click.option('--port', type=int, default=5000, help='Port number (default: 5000)')
    @click.option('--host', type=str, default='localhost', help='Host name (default: localhost)')
    @click.option('--enable-debug', is_flag=True, help='Enable debug mode')
    @click.option('--url-prefix', type=str, default='', help='Proxy url prefix (default: "")')
    def serve(host, port, enable_debug, url_prefix):
        try:
            server.setup(url_prefix)
            server.run(host=host, port=port, enable_debug=enable_debug)
        except Exception as error:
            click.echo(f"Could not start server due: {error}")

    return serve_commands


def build_calculate_commands():
    default_portion = VALID_PORTION_SIZES[0]

    @click.group()
    def calculate_commands():
        pass

    @calculate_commands.command()
    @click.argument('radius', type=float)
    @click.argument('number-of-people', type=int)
    @click.option('--portion-size', type=click.Choice(VALID_PORTION_SIZES), default=default_portion, help=f'Portion size (default: {default_portion})')
    @click.option('--use-long-format', is_flag=True, help='Report in a more human readable format')
    def calculate(radius, number_of_people, portion_size, use_long_format):
        """Calculate number of pizzas needed"""
        try:
            required_pizzas = calculate_pizzas(radius, number_of_people, portion_size)
            if use_long_format:
                click.echo(f"Number of pizzas needed: {required_pizzas:.2f}")
            else:
                click.echo(ceil(required_pizzas))
        except ValueError as error:
            click.echo(f"Error: {error}")

    return calculate_commands


def build_cli(server: WebServer):
    cli = click.CommandCollection()

    cli.add_source(build_serve_commands(server))
    cli.add_source(build_calculate_commands())

    return cli
