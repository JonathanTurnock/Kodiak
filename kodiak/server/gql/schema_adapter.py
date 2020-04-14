from typing import Dict

from multipledispatch import dispatch

from kodiak.model.job import Job
from kodiak.model.run import Step, Command, Run


@dispatch(Job)
def to_gql_schema(job: Job) -> Dict:
    return {
        "uuid": job.uuid,
        "name": job._name,
        "url": job._url
    }


@dispatch(Run)
def to_gql_schema(run: Run) -> Dict:
    return {
        "uuid": run.uuid,
        "job": to_gql_schema(run.job),
        "status": run.status.name,
        "started": run.started,
        "ended": run.ended,
        "steps": [to_gql_schema(step) for step in run.steps]
    }


@dispatch(Step)
def to_gql_schema(step: Step) -> Dict:
    return {
        "number": step.number,
        "name": step.name,
        "image": step.image,
        "status": step.status.name,
        "commands": [to_gql_schema(command) for command in step.commands]
    }


@dispatch(Command)
def to_gql_schema(command: Command) -> Dict:
    return {
        "number": command.number,
        "instruction": command.instruction,
        "std_out": [e for e in command.std_out],
        "std_err": [e for e in command.std_err]
    }
