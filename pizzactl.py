'''
This is the main file of the flask application.
It contains the routes and logic for calculating the number of pizzas needed.
'''
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

from pathlib import Path
from tempfile import gettempdir

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
    persistence_strategy = PersistDictAsJSONStrategy(Path(gettempdir(), __name__))
    persistence_manager.set_strategy(persistence_strategy)

    try:
        order_manager = persistence_manager.load_instance(
                uuid=None, target_class=OrderManager)
    except Exception:
        order_manager = OrderManager()

    cli = build_cli(server, persistence_manager, order_manager)
    cli()

    persistence_manager.save_instance(order_manager)


if __name__ == '__main__':
    main()
