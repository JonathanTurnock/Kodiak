from typing import List

from fxq.core.beans.factory.annotation import Autowired

from kodiak.agent.service.job import JobService
from kodiak.model.job import Job
from kodiak.model.run import Run, Step, Command
from kodiak.server.gql.schema_adapter import to_gql_schema
from kodiak.server.papi.repos import JobRepository, RunRepository, StepRepository, CommandRepository

_job_repository: JobRepository = Autowired("job_repository")
_run_repository: RunRepository = Autowired("run_repository")
_step_repository: StepRepository = Autowired("step_repository")
_command_repository: CommandRepository = Autowired("command_repository")
_job_service: JobService = Autowired("job_service")


def add_job(value, info, **args):
    job = Job()
    job.name = args["name"]
    job.url = args["url"]
    job = _job_repository.save(job)
    return to_gql_schema(job)


def start_job(value, info, **args):
    job: Job = _job_repository.find_by_id(args["id"])
    run_uuid = _job_service.process_request(job)
    return to_gql_schema(_run_repository.find_by_uuid(run_uuid))


def get_job_by_id(value, info, **args):
    job = _job_repository.find_by_id(args["id"])
    return to_gql_schema(job)


def get_jobs(value, info, **args):
    return [to_gql_schema(job) for job in _job_repository.find_all()]


def get_run(value, info, **args):
    def get_commands(step_id):
        commands: List[Command] = _command_repository.find_all_by_step_id(step_id)
        return [to_gql_schema(command) for command in commands]

    def get_steps(run_id):
        steps: List[Step] = _step_repository.find_all_by_run_id(run_id)
        steps_resp = []
        for step in steps:
            step_resp = to_gql_schema(step)
            step_resp["commands"] = get_commands(step.id)
            steps_resp.append(step_resp)
        return steps_resp

    run: Run = _run_repository.find_by_uuid(args["uuid"])
    response = to_gql_schema(run)
    response["steps"] = get_steps(run.id)
    return response


resolver_map = {
    'RootQuery': {
        'getJobs': get_jobs,
        'getJob': get_job_by_id,
        'runJob': start_job,
        'getRun': get_run
    },
    'RootMutation': {
        'addJob': add_job,
    }
}
