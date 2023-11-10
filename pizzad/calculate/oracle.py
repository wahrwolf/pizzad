from typing import Tuple
from .area_algorithms import AreaCalculationAlgorithm
from .consumption_estimations import ConsumptionEstimationStrategy
from .enums import PortionSize, Shape


class PizzaConsumptionOracle:
    algorithm_registry: dict[Shape, AreaCalculationAlgorithm]
    consumption_estimation_strategy: ConsumptionEstimationStrategy

    def __init__(self):
        self.algorithm_registry = {}

    def register_area_algorithm(
            self, shape: Shape, algorithm: AreaCalculationAlgorithm):
        self.algorithm_registry[shape] = algorithm
        return self

    def set_estimation_strategy(self, strategy: ConsumptionEstimationStrategy):
        self.consumption_estimation_strategy = strategy
        return self

    def estimate_consumed_pizzas(self,
                                 dimensions: Tuple[float, ...],
                                 number_of_people: int,
                                 portion_size: PortionSize, shape: Shape):
        area_per_pizza = self.algorithm_registry[shape]\
                .calculate_area(dimensions)
        required_pizza_area = self.consumption_estimation_strategy\
            .estimate_consumed_pizza_area(
                    number_of_people=number_of_people, portion_size=portion_size)

        return required_pizza_area / area_per_pizza
