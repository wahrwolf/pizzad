from math import ceil
import click
from flask import Flask

from calculations import calculate_pizzas, VALID_PORTION_SIZES
from webapp import blueprint


def build_order_commands():
    pass


def build_serve_commands():
    @click.group()
    def serve_commands():
        pass

    @serve_commands.command()
    @click.option('--port', type=int, default=5000, help='Port number (default: 5000)')
    @click.option('--host', type=str, default='0.0.0.0', help='Host name (default: 0.0.0.0)')
    @click.option('--enable-debug', is_flag=True, help='Enable debug mode')
    @click.option('--url-prefix', type=str, default='', help='Proxy url prefix (default: /)')
    def serve(host, port, enable_debug, url_prefix):
        try:
            app = Flask(__name__)
            if url_prefix:
                app.config["APPLICATION_ROOT"] = url_prefix
            app.register_blueprint(blueprint, url_prefix=url_prefix)
            app.run(host=host, port=port, debug=enable_debug)
        except Exception as error:
            click.echo(f"Error: {error}")

    return serve_commands


def build_calculate_commands():
    @click.group()
    def calculate_commands():
        pass

    @calculate_commands.command()
    @click.argument('radius', type=float)
    @click.argument('number-of-people', type=int)
    @click.option('--portion-size', type=click.Choice(VALID_PORTION_SIZES), default=VALID_PORTION_SIZES[0], help='Portion size (default: slice)')
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


def build_cli():
    cli = click.CommandCollection()

    cli.add_source(build_serve_commands())
    cli.add_source(build_calculate_commands())

    return cli
