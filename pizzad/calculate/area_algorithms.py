from math import pi
from enum import StrEnum, auto
from typing import Tuple
from abc import ABC, abstractmethod


class AreaCalculationAlgorithm(ABC):
    @staticmethod
    @abstractmethod
    def calculate_area(dimensions: Tuple[float, ...]):
        raise NotImplementedError


class SquareAreaAlgorithm(AreaCalculationAlgorithm):
    @staticmethod
    def calculate_area(dimensions: Tuple[float, ...]):
        if len(dimensions) != 1:
            raise NotImplementedError(
                    f"{len(dimensions)} dimension given"
                    "This algorithm can only calculate 1D square areas!"
            )

        return RectangleAreaAlgorithm.calculate_area(
                (dimensions[0], dimensions[0]))


class RectangleAreaAlgorithm(AreaCalculationAlgorithm):
    @staticmethod
    def calculate_area(dimensions: Tuple[float, ...]):
        if len(dimensions) != 2:
            raise NotImplementedError(
                    f"{len(dimensions)} dimension{'' if len(dimensions) == 1 else 's'} given"
                    "This algorithm can only calculate 2D rectable areas!"
            )

        return dimensions[0] * dimensions[1]


class CircleAreaAlgorithm(AreaCalculationAlgorithm):
    @staticmethod
    def calculate_area(dimensions: Tuple[float, ...]):
        if len(dimensions) != 1:
            raise NotImplementedError(
                    f"{len(dimensions)} dimension given"
                    "This algorithm can only calculate 1D circle areas!"
            )
        radius = dimensions[0]
        return radius ** 2 * pi
