'''
This is the main file of the flask application.
It contains the routes and logic for calculating the number of pizzas needed.
'''
from argparse import ArgumentParser
from math import ceil
from flask import Flask

from calculations import calculate_pizzas, VALID_PORTION_SIZES
from webapp import blueprint


def print_usage():
    help_message = """
    usage:
        pizzactl calculate      : calculates the number of pizzas you need to order
        pizzactl serve          : spins up a server
    """
    print(help_message)


def main():
    parser = ArgumentParser(description='Calculate number of pizzas needed for a group.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subparser for the 'calculate' command
    calculate_parser = subparsers.add_parser('calculate',help='Calculate number of pizzas needed')
    calculate_parser.add_argument('radius', type=float, help='Radius of the pizza in centimeters')
    calculate_parser.add_argument('num_people', type=int, help='Number of people in the group')
    calculate_parser.add_argument('--portion_size', type=str, choices=VALID_PORTION_SIZES,
                                  help='Served portion size', nargs='?', default=VALID_PORTION_SIZES[0])
    calculate_parser.add_argument('--use_long_format', type=bool, default=False,
                                  help='Report in a more human readable format', nargs='?')

    # Subparser for the 'calculate' command
    serve_parser = subparsers.add_parser('serve', help='Serve the pizza calclualtor web UI')
    serve_parser.add_argument('--port', default=5000, type=int, help='Port name to listen for incomming request')
    serve_parser.add_argument('--host', default="localhost", type=str, help='Host name for the server to use')
    serve_parser.add_argument('--enable_debug', type=bool, help='Enables debug for the sever')
    serve_parser.add_argument('--url_prefix', type=str, default='', help='The proxy url prefix to use')

    args = parser.parse_args()

    match args.command:
        case 'calculate':
            num_pizzas = calculate_pizzas(args.radius, args.num_people, args.portion_size)
            if args.use_long_format:
                print(f'Number of pizzas needed: {num_pizzas:.2f}')
            else:
                print(ceil(num_pizzas))
        case 'serve':
            app = Flask(__name__)
            if args.url_prefix:
                app.config["APPLICATION_ROOT"] = args.url_prefix
            app.register_blueprint(blueprint, url_prefix=args.url_prefix)
            app.run(host=args.host, port=args.port, debug=args.enable_debug)
        case _:
            print_usage()


if __name__ == '__main__':
    main()
