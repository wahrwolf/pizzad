'''
This is the main file of the flask application.
It contains the routes and logic for calculating the number of pizzas needed.
'''
from argparse import ArgumentParser
from math import ceil
from cli import build_cli


def main():
    cli = build_cli()
    cli()


if __name__ == '__main__':
    main()
