import logging

from constants import LOGGING_FORMAT

if __name__ == '__main__':
    logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)

import click

from app import app


@click.command()
@click.option('--debug', is_flag=True, help="Enable debug Logging for the application")
def main(debug: bool):
    logging.basicConfig(format=LOGGING_FORMAT, level=(logging.DEBUG if debug else logging.INFO))
    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()
