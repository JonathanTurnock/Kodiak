import logging

from fxq.core.beans.factory.annotation import Autowired

from kodiak.server.papi.repos import RunRepository

LOGGER = logging.getLogger(__name__)
_run_repository: RunRepository = Autowired("run_repository")


def do_callback(run_task):
    _run_repository.save(run_task.get_run())
