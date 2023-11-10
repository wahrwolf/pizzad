from math import ceil
import click

from pizzad.calculate import calculate_consumed_pizzas, Shape, PortionSize


def build_calculate_commands():

    @click.group("calc")
    def calculate_commands():
        pass

    @calculate_commands.command()
    @click.argument('radius', type=float)
    @click.argument('number-of-people', type=int)
    @click.option('--portion-size', default=PortionSize.DEFAULT,
                  type=click.Choice(list(PortionSize)),
                  help=f'Portion size (default: {PortionSize.DEFAULT})')
    @click.option('--use-long-format', is_flag=True,
                  help='Report in a more human readable format')
    def pizzas(radius, number_of_people, portion_size, use_long_format):
        """Calculate number of pizzas needed"""
        try:
            required_pizzas = calculate_consumed_pizzas(
                    pizza_shape=Shape.CIRCLE, pizza_dimensions=(radius,),
                    number_of_people=number_of_people, portion_size=portion_size)
            if use_long_format:
                click.echo(f"Number of pizzas needed: {required_pizzas:.2f}")
            else:
                click.echo(ceil(required_pizzas))
        except ValueError as error:
            click.echo(f"Error: {error}")

    return calculate_commands
