import click

from pizzad.web.server import WebServer
from pizzad.orders.manager import OrderManager
from pizzad.persistence.manager import PersistenceManager

from .server import build_server_commands
from .calculate import build_calculate_commands
from .orders import build_order_commands


def build_cli(
        server: WebServer,
        persistence_manager: PersistenceManager,
        order_manager: OrderManager):
    @click.group()
    def cli():
        pass

    cli.add_command(build_order_commands(persistence_manager, order_manager))
    cli.add_command(build_server_commands(server))
    cli.add_command(build_calculate_commands())

    return cli
