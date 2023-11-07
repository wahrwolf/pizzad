'''
This is the main file of the flask application.
It contains the routes and logic for calculating the number of pizzas needed.
'''
from cli import build_cli
from webapp import FlaskWebServer
from routes import routes_blueprint


def main():
    server = FlaskWebServer(routes_blueprint)
    cli = build_cli(server)
    cli()


if __name__ == '__main__':
    main()
