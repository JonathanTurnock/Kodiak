import logging

import click
from fxq.core.beans.factory.annotation import Autowired

from fxq.ae.runner.constants import LOGGING_FORMAT
from fxq.ae.runner.factory import ExecutorFactory
from fxq.ae.runner.service import PipelineService, ExecutorService

__executor_service: ExecutorService = Autowired(type=ExecutorService)
__pipeline_service: PipelineService = Autowired(type=PipelineService)
__factory: ExecutorFactory = Autowired(type=ExecutorFactory)


@click.command()
@click.option('--url', '-u', required=True, multiple=False,
              help="Provide the URL of the git repository to configure pipeline from")
@click.option('--debug', is_flag=True, help="Enable debug Logging for the application")
def main(url: str, debug: bool):
    logging.basicConfig(format=LOGGING_FORMAT, level=(logging.DEBUG if debug else logging.INFO))

    executor = __factory.from_url(url)
    __executor_service.save(executor)
    __executor_service.start(executor)


if __name__ == '__main__':
    main()
