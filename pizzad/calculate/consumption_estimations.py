from abc import ABC, abstractmethod
from .enums import PortionSize
from .area_algorithms import CircleAreaAlgorithm


class ConsumptionEstimationStrategy(ABC):
    @staticmethod
    @abstractmethod
    def estimate_consumed_pizza_area(
            number_of_people: int, portion_size: PortionSize):
        raise NotImplementedError


class WahrwolfsPizzaConsumptionEstimationStrategy(
        ConsumptionEstimationStrategy):
    """
    Through testing wahrwolf found that 16cm pizza is a snack and 25 is a meal
    All estimations are based on that logic.
    Scales well after >10 people
    """
    PIZZA_RADIUS_PER_PERSON = {
            PortionSize.DINNER: 25,
            PortionSize.SNACK: 16
    }

    @staticmethod
    def estimate_consumed_pizza_area(
             number_of_people: int, portion_size: PortionSize):

        if portion_size not in WahrwolfsPizzaConsumptionEstimationStrategy\
                .PIZZA_RADIUS_PER_PERSON:
            raise NotImplementedError
        radius = WahrwolfsPizzaConsumptionEstimationStrategy\
            .PIZZA_RADIUS_PER_PERSON[portion_size]
        return number_of_people * CircleAreaAlgorithm.calculate_area((radius,))


class NomBaguetteConsumptionEstimationStrategy(ABC):
    """
    Natürliche Offensichtliche Mengenschätzung für Baguettes
    5 Baguette für 10 Leute
    60% * 5 Baguettes für 10 Leute als Baguette + Dip
    30% * 5 Baguette für 10 Leute als Beilage
    """
    BAGUETTES_PER_GROUP_OF_FIVE = {
            PortionSize.DINNER = 2.0/3.0 * 5 / 10
    pass
