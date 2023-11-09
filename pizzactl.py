'''
This is the main file of the flask application.
It contains the routes and logic for calculating the number of pizzas needed.
'''
from pathlib import Path
from tempfile import gettempdir

from pizzad import get_missing_dependencies
missing_dependencies = get_missing_dependencies()
if missing_dependencies:
    ERROR_MESSAGE = "ERROR: Missing dependenc"\
            f"{'y' if len(missing_dependencies) == 1 else 'ies'}!"
    if __name__ == '__main__':
        import sys
        print(f"{ERROR_MESSAGE} {missing_dependencies})")
        sys.exit(1)
    else:
        raise NotImplementedError(ERROR_MESSAGE, missing_dependencies)


from pizzad.cli import build_cli
from pizzad.web.server import FlaskWebServer
from pizzad.web.routes import routes_blueprint

from pizzad.persistence.manager import PersistenceManager
from pizzad.persistence.strategies import PersistDictAsJSONStrategy
from pizzad.orders.manager import OrderManager


server = FlaskWebServer(routes_blueprint)
app = server.to_flask_app()


def main():
    persistence_manager = PersistenceManager()
    persistence_strategy = PersistDictAsJSONStrategy(Path(gettempdir(), "pizzad"))
    persistence_manager.set_strategy(persistence_strategy)

    try:
        order_manager = persistence_manager.load_instance(
                uuid=None, target_class=OrderManager)
    except FileNotFoundError:
        print("Could not find existing Order Manager. Creating it now!")
        order_manager = OrderManager()
    else:
        print("Found existing Order Manager. Reuisng it!")
    finally:
        print(order_manager.to_dict())

    cli = build_cli(server, persistence_manager, order_manager)
    cli()


if __name__ == '__main__':
    main()
