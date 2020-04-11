from fxq.commons.marshalling import DictMarshal

from bootstrap import job_dao
from kodiak.agent.model.job import Job
from kodiak.server.gql.utils import build_executable_schema
from kodiak.server.gql.utils import build_executable_schema, get_schema_def


def add_job(value, info, **args):
    job = Job(args["name"], args["url"])
    job = job_dao.save(job)
    return DictMarshal.to_dict(job)


def get_job_by_uuid(value, info, **args):
    job = job_dao.find_job_by_uuid(args["uuid"])
    return DictMarshal.to_dict(job)


def get_jobs(value, info, **args):
    return [DictMarshal.to_dict(job) for job in job_dao.find_jobs()]


resolvers = {
    'RootQuery': {
        'getJobs': get_jobs,
        'getJob': get_job_by_uuid
    },
    'RootMutation': {
        'addJob': add_job,
    }
}

schema = build_executable_schema(get_schema_def(), resolvers)
