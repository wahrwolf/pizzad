"""
Usescases that represent common operations around orders
An order represents the desire of some users that to consume a pizza

In this module are all usecases from a domain perspective
"""


# Basic interactions with users, orders and options
def cerate_new_order():
    return NotImplementedError


def delete_order_by_id():
    return NotImplementedError


def get_orders_by_query():
    return NotImplementedError


def create_new_user():
    return NotImplementedError


def get_users_by_query():
    return NotImplementedError


def delete_user_by_id():
    return NotImplementedError


def create_new_otion_for_order():
    return NotImplementedError


def query_options_for_order():
    return NotImplementedError


def get_option_for_order_by_id():
    return NotImplementedError


def delete_option_for_order_by_id():
    return NotImplementedError


# Things users want to do
def add_option_to_order():
    return NotImplementedError


def open_order_for_participant_registration():
    return NotImplementedError


def register_participant_for_option():
    return NotImplementedError


def close_order_for_participant_registration():
    return NotImplementedError


def get_any_compatible_option_for_user():
    return NotImplementedError


def get_all_available_options_for_user():
    return NotImplementedError


def create_order_with_compatible_options_for_user_collection():
    return NotImplementedError
