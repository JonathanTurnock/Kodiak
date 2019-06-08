import logging

from fxq.core.beans.factory.annotation import Autowired

from fxq.ae.runner.factory import ExecutorFactory
from fxq.ae.runner.service import PipelineService, ExecutorService

format = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
logging.basicConfig(format=format, level=logging.INFO)

__executor_service: ExecutorService = Autowired(type=ExecutorService)
__pipeline_service: PipelineService = Autowired(type=PipelineService)
__factory: ExecutorFactory = Autowired(type=ExecutorFactory)


def main(url: str):
    executor = __factory.from_url(url)
    __executor_service.save(executor)
    __executor_service.start(executor)


if __name__ == '__main__':
    url = "git@bitbucket.org:fxquants/aep-hello-world.git"
    main(url)
