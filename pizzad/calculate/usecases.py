from typing import Tuple
from .enums import Shape, PortionSize
from .oracle import PizzaConsumptionOracle as Oracle
from .consumption_estimations import \
        WahrwolfsPizzaConsumptionEstimationStrategy as WahrwolfsEstimation

from .area_algorithms import (
        CircleAreaAlgorithm as CircleAlgorithm,
        SquareAreaAlgorithm as SquareAlgorithm,
        RectangleAreaAlgorithm as RectangleAlgorithm
)

oracle = Oracle().set_estimation_strategy(WahrwolfsEstimation)\
        .register_area_algorithm(
                shape=Shape.CIRCLE, algorithm=CircleAlgorithm)\
        .register_area_algorithm(
                shape=Shape.RECTANGLE, algorithm=RectangleAlgorithm)\
        .register_area_algorithm(
                shape=Shape.SQUARE, algorithm=SquareAlgorithm)


def calculate_consumed_pizzas(
        number_of_people: int, pizza_dimensions: Tuple[float, ...],
        portion_size: PortionSize = PortionSize.DEFAULT,
        pizza_shape: Shape = Shape.DEFAULT):
    return oracle.estimate_consumed_pizzas(
            number_of_people=number_of_people, portion_size=portion_size,
            dimensions=pizza_dimensions, shape=pizza_shape)
