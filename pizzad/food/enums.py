from enum import StrEnum, Enum, auto


class Allergen(StrEnum):
    MILK = auto()
    GLUTEN = auto()
    CRAB = auto()
    EGG = auto()
    FISH = auto()
    PEANUT = auto()
    SOJA = auto()
    SESAM = auto()
    MUSTARD = auto()
    NUT = auto()
    MOLLUSC = auto()
    SULFAT = auto()
    LUPIN = auto()

    ANIMAL = auto()
    TREIF = auto()
    HARAM = auto()

    def __str__(self) -> str:
        return self.name


class Ingredient(Enum):
    CHEESE = (Allergen.MILK,)

    VEGETARIAN = (Allergen.MILK, Allergen.EGG)
    MEAT = (Allergen. CRAB, Allergen.EGG, Allergen.FISH, Allergen.ANIMAL)

    def __init__(self, *args: list[Allergen]):
        self._allergenes = {arg for arg in args if isinstance(arg, Allergen)}

    def contains_allergenes(self, *args: list[Allergen]):
        for allergen in args:
            if allergen in self._allergenes:
                return True
        return False

    def __contains__(self, other) -> bool:
        if isinstance(other, Allergen):
            return other in self._allergenes
        return False

    def get_allergenes(self) -> set[Allergen]:
        return self._allergenes

    def __str__(self) -> str:
        return self.name


class FoodType(StrEnum):
    PIZZA = auto()
    BAGUETTE = auto()
    SOUP = auto()
    SUSHI = auto()
