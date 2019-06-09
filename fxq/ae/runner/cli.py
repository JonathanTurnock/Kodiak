import logging

import click

from fxq.ae.runner.constants import LOGGING_FORMAT
from fxq.ae.runner.fxq_ae_runner_app import app


@click.command()
@click.option('--debug', is_flag=True, help="Enable debug Logging for the application")
def main(debug: bool):
    logging.basicConfig(format=LOGGING_FORMAT, level=(logging.DEBUG if debug else logging.INFO))
    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()
