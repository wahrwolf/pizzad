import click

from pizzad.persistence.manager import PersistenceManager
from pizzad.orders.manager import OrderManager


def build_order_commands(
        persistence_manager: PersistenceManager,
        order_manager: OrderManager):
    @click.group("order")
    def order_commands():
        pass

    @order_commands.command()
    @click.argument('name', type=str)
    def create(name):
        order_manager.create_order_if_not_exist(name)
        persistence_manager.save_instance(order_manager)

    @order_commands.command()
    @click.argument('name', type=str)
    def show(name):
        orders = order_manager.get_orders(name)
        if len(orders) >= 1:
            order = orders[0]
            print(f"{order.name}: {order.get_number_of_participants()}")

    @order_commands.command()
    @click.argument('name', type=str)
    def close(name):
        orders = order_manager.get_orders(name)
        if len(orders) >= 1:
            order = orders[0]
            print(f"{order.name}: {order.get_number_of_participants()}")
            order.close()
        persistence_manager.save_instance(order_manager)

    return order_commands
