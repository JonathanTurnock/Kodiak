import logging

from kodiak.server.papi.command import CommandDao, command_dto_of_command
from kodiak.server.papi.run import RunDao, run_dto_of_run
from kodiak.server.papi.step import StepDao, step_dto_of_step

LOGGER = logging.getLogger(__name__)


def do_callback(ref_object):
    LOGGER.info(f"Performing Callback for {ref_object.__class__.__name__} - {ref_object.to_dict()}")
    obj_type = ref_object.__class__.__name__
    if obj_type == "Run":
        run_dao = RunDao()
        run_dto = run_dao.save(run_dto_of_run(ref_object))
        ref_object.id = run_dto.id
    elif obj_type == "Step":
        step_dao = StepDao()
        step_dto = step_dao.save(step_dto_of_step(ref_object))
        ref_object.id = step_dto.id
    elif obj_type == "Command":
        command_dao = CommandDao()
        command_dto = command_dao.save(command_dto_of_command(ref_object))
        ref_object.id = command_dto.id
