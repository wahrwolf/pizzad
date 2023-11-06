'''
This is the main file of the flask application.
It contains the routes and logic for calculating the number of pizzas needed.
'''
from flask import Flask, render_template, request
from argparse import ArgumentParser
from math import pi, ceil

app = Flask(__name__)

# The small (16cm) pizza works for one person
# This is a magic value learned by testing
PIZZA_AREA_PER_PERSON = {
        "snack": 16 ** 2 * pi,
        "dinner": 25 ** 2 * pi,
}

VALID_PORTION_SIZES = [size for size in PIZZA_AREA_PER_PERSON.keys()]


def calculate_pizzas(pizza_radius, num_people, portion_size=VALID_PORTION_SIZES[0]):
    assert num_people >= 0, "Number of people needs to be positive."
    assert pizza_radius >= 0, "Pizza radius needs to be positive."
    assert portion_size in VALID_PORTION_SIZES, f"Portion size '{portion_size}' is not in {VALID_PORTION_SIZES}"

    pizza_area = pizza_radius ** 2 * pi

    pizza_area_needed = PIZZA_AREA_PER_PERSON[portion_size] * num_people
    num_pizzas = pizza_area_needed / pizza_area

    return num_pizzas


def print_usage():
    help_message = """
    usage:
        pizzactl calculate      : calculates the number of pizzas you need to order
        pizzactl serve          : spins up a server
    """
    print(help_message)


@app.route('/')
def home():
    return render_template('index.html', valid_portion_sizes=VALID_PORTION_SIZES)


@app.route('/calculate', methods=['POST'])
def calculate():
    pizza_radius = float(request.form['radius'])
    number_of_people = int(request.form['num_people'])
    portion_size = str(request.form['portion_size'])

    try:
        num_pizzas = calculate_pizzas(
                pizza_radius=pizza_radius,
                num_people=number_of_people,
                portion_size=portion_size
        )
    except Exception as error:
        return render_template('error.html', message=str(error))

    return render_template('result.html', num_pizzas=num_pizzas)


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
    serve_parser.add_argument('--web_root', type=str, default='', help='The web root prefix if this is running behind a proxy')

    args = parser.parse_args()

    match args.command:
        case 'calculate':
            num_pizzas = calculate_pizzas(args.radius, args.num_people, args.portion_size)
            if args.use_long_format:
                print(f'Number of pizzas needed: {num_pizzas:.2f}')
            else:
                print(ceil(num_pizzas))
        case 'serve':
            if args.web_root:
                app.config["APPLICATION_ROOT"] = args.web_root
            app.run(host=args.host, port=args.port, debug=args.enable_debug)
        case _:
            print_usage()


if __name__ == '__main__':
    main()
