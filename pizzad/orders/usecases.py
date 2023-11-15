"""
Usescases that represent common operations around orders
An order represents the desire of some users that to consume a pizza

In this module are all usecases from a domain perspective
"""
from uuid import UUID
from typing import Optional
from functools import reduce
from pizzad.food import Ingredient
from pizzad.user.abc import User, UserFactory, UserRegistry
from .models import (
        Order, OrderRegistry, OrderFactory,
        OrderOption, OrderOptionRegistry, OrderOptionFactory)


# Basic interactions with users, orders and options
def create_new_order(order_name: str,
                     factory: OrderFactory,
                     registry: OrderRegistry
                     ) -> Order:
    order = factory.create_order(name=order_name)
    registry.register_member(order)
    return order


def delete_order_by_id(uuid: UUID, registry: OrderRegistry):
    registry.delete_member_by_id(uuid)


def get_orders_by_query(registry: OrderRegistry, **kwargs) -> set[Order]:
    orders = registry.get_orders_by_query(**kwargs)
    return orders


def create_new_user(user_name: str,
                    factory: UserFactory,
                    registry: UserRegistry
                    ) -> User:
    user = factory.create_user(name=user_name)
    return user


def get_users_by_query(registry: UserRegistry, **kwargs) -> set[User]:
    users = registry.get_users_by_query(**kwargs)
    return users


def delete_user_by_id(uuid: UUID, registry: UserRegistry):
    registry.delete_member_by_id(uuid)


def create_new_option_for_order(
        order: Order, option_name: str, ingredients: set[Ingredient],
        factory: OrderOptionFactory
        ) -> OrderOption:
    option = factory.create_option(
            name=option_name, ingredients=ingredients)
    order.add_option(option)
    return order


def query_options_for_order(order: Order, **query_arguments):
    options = order.get_options(**query_arguments)
    return options


def get_option_by_id(uuid: UUID, registry: OrderOptionRegistry) -> OrderOption:
    option = registry.get_member_by_id(uuid)
    return option


def delete_option_by_id(uuid: UUID, registry: OrderOptionRegistry):
    registry.delete_member_by_id(uuid)


# Things users want to do
def add_option_to_order(order: Order, option_name: str,
                        ingredients: Optional[set[Ingredient]] = None
                        ) -> Order:

    option = OrderOptionFactory.create_option(name=option_name)
    if ingredients:
        for ingredient in ingredients:
            option.add_ingredient(ingredient)
    order.add_option(option)
    return order


def open_order_for_participant_registration(order: Order):
    if order.is_closed_for_registration():
        order.open_order_for_participant_registration()


def register_participant_for_option(
        order: Order, option: OrderOption, participant: User) -> Order:
    if (
            not order.is_closed_for_registration() and
            option in order.get_options()):

        order.register_participant_for_option(
                participant=participant, option=option)
    return order


def close_order_for_participant_registration(order: Order) -> Order:
    if not order.is_closed_for_registration():
        order.close_for_registration()
    return order


def get_all_available_options(registry: OrderRegistry):
    open_orders = [
            order for order in registry.get_all_members()
            if not order.is_closed_for_registration()
    ]

    available_options = reduce(
            lambda a, b: a.join(b.get_options()),
            open_orders, set()
    )

    return available_options


def get_all_compatible_options_for_user(user: User, registry: OrderRegistry):
    available_options = get_all_available_options(registry)
    non_allergic_options = filter(
            lambda option: (user.get_allergies() not in option),
            available_options)

    options_with_compatible_ingredients = filter(
            lambda option: (user.get_excluded_ingredients not in option),
            non_allergic_options)

    return options_with_compatible_ingredients


def create_order_with_compatible_options_for_user_collection():
    return NotImplementedError
