from fxq.core.beans.factory.annotation import Autowired

from kodiak.agent import AgentInterface
from kodiak.model.job import Job
from kodiak.model.run import Run
from kodiak.server.gql.schema_adapter import to_gql_schema
from kodiak.server.papi.repos import JobRepository, RunRepository

_job_repository: JobRepository = Autowired("job_repository")
_run_repository: RunRepository = Autowired("run_repository")


def add_job(value, info, **args):
    job = Job(name=args["name"], url=args["url"])
    job = _job_repository.save(job)
    return to_gql_schema(job)


def update_job(value, info, **args):
    existing_job = _job_repository.find_by_uuid(args["uuid"])
    job = Job(uuid=args["uuid"], name=args["name"], url=args["url"])
    _job_repository.save(job)
    return to_gql_schema(job)


def remove_job(value, info, **args):
    _job_repository.delete_by_uuid(args["uuid"])
    return True


def start_job(value, info, **args):
    job: Job = _job_repository.find_by_uuid(args["uuid"])
    run_uuid = AgentInterface.run_job(job.uuid, job.name, job.url)
    return to_gql_schema(_run_repository.find_by_uuid(run_uuid))


def get_job_by_uuid(value, info, **args):
    job = _job_repository.find_by_uuid(args["uuid"])
    job = to_gql_schema(job)
    return


def get_jobs(value, info, **args):
    return [to_gql_schema(job) for job in _job_repository.find_all()]


def get_run(value, info, **args):
    run: Run = _run_repository.find_by_uuid(args["uuid"])
    response = to_gql_schema(run)
    return response


def get_runs_for_job(value, info, **args):
    return [to_gql_schema(run) for run in _run_repository.find_all_by_job_uuid(args["uuid"])]


def remove_run(value, info, **args):
    _run_repository.delete_by_uuid(args["uuid"])
    return True


resolver_map = {
    'RootQuery': {
        'getJobs': get_jobs,
        'getJob': get_job_by_uuid,
        'getRunsForJob': get_runs_for_job,
        'runJob': start_job,
        'getRun': get_run
    },
    'RootMutation': {
        'addJob': add_job,
        'updateJob': update_job,
        'removeJob': remove_job,
        'removeRun': remove_run
    }
}
