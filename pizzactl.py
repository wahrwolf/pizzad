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
else:
    from pizzad.cli import build_cli
    from pizzad.web.server import FlaskWebServer
    from pizzad.web.routes import routes_blueprint

server = FlaskWebServer(routes_blueprint)
app = server.to_flask_app()


def main():
    cli = build_cli(server)
    cli()


if __name__ == '__main__':
    main()
