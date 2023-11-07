'''
This file contains the logic for calculating the number of pizzas needed.
'''
from math import pi

# The small (16cm) pizza works for one person
# This is a magic value learned by testing
PIZZA_AREA_PER_PERSON = {
        "snack": 16 ** 2 * pi,
        "dinner": 25 ** 2 * pi,
}

VALID_PORTION_SIZES = list(PIZZA_AREA_PER_PERSON)


def calculate_pizzas(pizza_radius, num_people, portion_size=VALID_PORTION_SIZES[0]):
    assert num_people >= 0, "Number of people needs to be positive."
    assert pizza_radius >= 0, "Pizza radius needs to be positive."
    assert portion_size in VALID_PORTION_SIZES, f"Portion size '{portion_size}' is not in {VALID_PORTION_SIZES}"

    pizza_area = pizza_radius ** 2 * pi

    pizza_area_needed = PIZZA_AREA_PER_PERSON[portion_size] * num_people
    num_pizzas = pizza_area_needed / pizza_area

    return num_pizzas
