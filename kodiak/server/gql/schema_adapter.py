from typing import Dict

from multipledispatch import dispatch

from kodiak.model.job import Job
from kodiak.model.run import Run, Step, Command


@dispatch(Job)
def to_gql_schema(job: Job) -> Dict:
    return {
        "id": job.id,
        "name": job.name,
        "url": job.url
    }


@dispatch(Run)
def to_gql_schema(run: Run) -> Dict:
    return {
        "id": run.id,
        "uuid": run.uuid,
        "job": to_gql_schema(run.job),
        "status": run.status.name,
        "started": run.started,
        "ended": run.ended
    }


@dispatch(Step)
def to_gql_schema(step: Step) -> Dict:
    return {
        "id": step.id,
        "run": to_gql_schema(step.run),
        "number": step.number,
        "name": step.name,
        "image": step.image,
        "status": step.status.name
    }


@dispatch(Command)
def to_gql_schema(command: Command) -> Dict:
    return {
        "id": command.id,
        "step": to_gql_schema(command.step),
        "number": command.number,
        "instruction": command.instruction,
        "std_out": command.std_out,
        "std_err": command.std_err
    }
