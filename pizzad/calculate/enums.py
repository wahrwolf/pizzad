from enum import StrEnum, auto


class PortionSize(StrEnum):
    DINNER = auto()
    SNACK = auto()
    DEFAULT = SNACK


class Shape(StrEnum):
    CIRCLE = auto()
    SQUARE = auto()
    RECTANGLE = auto()
    DEFAULT = CIRCLE
