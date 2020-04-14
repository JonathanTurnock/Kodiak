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


def start_job(value, info, **args):
    job: Job = _job_repository.find_by_uuid(args["uuid"])
    run_uuid = AgentInterface.run_job(job.uuid, job.name, job.url)
    return to_gql_schema(_run_repository.find_by_uuid(run_uuid))


def get_job_by_id(value, info, **args):
    job = _job_repository.find_by_id(args["id"])
    job = to_gql_schema(job)
    return


def get_jobs(value, info, **args):
    return [to_gql_schema(job) for job in _job_repository.find_all()]


def get_run(value, info, **args):
    run: Run = _run_repository.find_by_uuid(args["uuid"])
    response = to_gql_schema(run)
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
