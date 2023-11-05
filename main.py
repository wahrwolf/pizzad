'''
This is the main file of the flask application.
It contains the routes and logic for calculating the number of pizzas needed.
'''
from flask import Flask, render_template, request
from math import pi

app = Flask(__name__)

# The small (16cm) pizza works for one person
# This is a magic value learned by testing
PIZZA_AREA_PER_PERSON = 16 ** 2 * pi


def calculate_pizzas(pizza_radius, num_people):
    assert num_people >= 0, "Number of people needs to be positive."
    assert pizza_radius >= 0, "Pizza radius needs to be positive."

    pizza_area = pizza_radius ** 2 * pi

    pizza_area_needed = PIZZA_AREA_PER_PERSON * num_people
    num_pizzas = pizza_area_needed / pizza_area

    return num_pizzas

def main():
    parser = argparse.ArgumentParser(description='Calculate number of pizzas needed for a group.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subparser for the 'calculate' command
    calculate_parser = subparsers.add_parser('calculate', help='Calculate number of pizzas needed')
    calculate_parser.add_argument('radius', type=float, help='Radius of the pizza in centimeters')
    calculate_parser.add_argument('num_people', type=int, help='Number of people in the group')

    # Subparser for the 'calculate' command
    serve_parser = subparsers.add_parser('serve', help='Serve the pizza calclualtor web UI')
    serve_parser.add_argument('port', type=int, help='Port name to listen for incomming request')
    serve_parser.add_argument('host', type=str, help='Host name for the server to use')

    args = parser.parse_args()

    if args.command == 'calculate':
        num_pizzas = calculate_pizzas(args.radius, args.num_people)
        print(f'Number of pizzas needed: {num_pizzas:.2f}')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    pizza_radius = float(request.form['radius'])
    pizza_area = pizza_radius ** 2 * pi
    number_of_people = int(request.form['num_people'])

    if number_of_people == 0:
        return render_template('error.html', message="Number of people cannot be zero.")

    pizza_area_needed = PIZZA_AREA_PER_PERSON * number_of_people
    num_pizzas = pizza_area_needed / pizza_area

    return render_template('result.html', num_pizzas=num_pizzas)


if __name__ == '__main__':
    main()

if __name__ == '__main__':
    app.run(debug=True)

