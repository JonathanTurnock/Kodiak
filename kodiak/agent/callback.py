import logging

from fxq.core.beans.factory.annotation import Autowired

from kodiak.model.run import Run, Step, Command

LOGGER = logging.getLogger(__name__)


def do_callback(ref_object):
    LOGGER.info(f"Performing Callback for {ref_object.__class__.__name__} - {ref_object.to_dict()}")
    obj_type = ref_object.__class__.__name__
    if obj_type == "Run":
        run_repository = Autowired("run_repository")
        run = Run(
            id=ref_object.id,
            job=ref_object.job,
            uuid=ref_object.uuid,
            status=ref_object.status,
            started=ref_object.started,
            ended=ref_object.ended
        )
        run = run_repository.save(run)
        ref_object.id = run.id
    elif obj_type == "Step":
        step_repository = Autowired("step_repository")
        step = Step(
            id=ref_object.id,
            run=ref_object.run,
            number=ref_object.number,
            name=ref_object.name,
            image=ref_object.image,
            status=ref_object.status
        )
        step = step_repository.save(step)
        ref_object.id = step.id
    elif obj_type == "Command":
        command_repository = Autowired("command_repository")
        command = Command(
            id=ref_object.id,
            step=ref_object.step,
            number=ref_object.number,
            instruction=ref_object.instruction,
            std_out=ref_object.std_out,
            std_err=ref_object.std_err
        )
        command = command_repository.save(command)
        ref_object.id = command.id
