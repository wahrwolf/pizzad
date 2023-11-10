from flask import Blueprint, render_template, request
from pizzad.calculate import calculate_consumed_pizzas, Shape, PortionSize

routes_blueprint = Blueprint('pizzad', __name__)


@routes_blueprint.route('/')
def home():
    return render_template('index.html', valid_portion_sizes=list(PortionSize))


@routes_blueprint.route('/calculate', methods=['POST'])
def calculate():
    pizza_radius = float(request.form['radius'])
    number_of_people = int(request.form['num_people'])
    portion_size = str(request.form['portion_size'])

    try:
        num_pizzas = calculate_consumed_pizzas(
                pizza_shape=Shape.CIRCLE, pizza_dimensions=(pizza_radius,),
                number_of_people=number_of_people, portion_size=portion_size)

    except Exception as error:
        return render_template('error.html', message=str(error))

    return render_template('result.html', num_pizzas=num_pizzas)
