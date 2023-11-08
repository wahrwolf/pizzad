from math import ceil
import click

from pizzad.calculations import calculate_pizzas, VALID_PORTION_SIZES


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
