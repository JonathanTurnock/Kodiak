from bootstrap import job_dao, job_service
from kodiak.agent.model.job import Job
from kodiak.server.gql.utils import build_executable_schema
from kodiak.server.gql.utils import build_executable_schema, get_schema_def
from kodiak.server.papi.job import job_dto_of_job, JobDao
from kodiak.server.papi.run import RunDao


def add_job(value, info, **args):
    job = Job(args["name"], args["url"])
    job = job_dao.save(job_dto_of_job(job))
    return {
        "id": job.id,
        "name": job.name,
        "url": job.url
    }


def start_job(value, info, **args):
    job_dao = JobDao()
    job_dto = job_dao.find_job_by_id(args["id"])
    job = Job(job_dto.name, job_dto.url)
    job.id = job_dto.id
    run = job_service.process_request(job)
    return {
        "id": run.id,
        "jobId": run.job.id,
        "uuid": run.uuid,
        "status": run.status.name,
        "started": run.started,
        "ended": run.ended
    }


def get_job_by_id(value, info, **args):
    job = job_dao.find_job_by_id(args["id"])
    return {
        "id": job.id,
        "name": job.name,
        "url": job.url
    }


def get_jobs(value, info, **args):
    return [{
        "id": job.id,
        "name": job.name,
        "url": job.url
    } for job in job_dao.find_jobs()]


def get_run(value, info, **args):
    run_dao = RunDao()
    run_dto = run_dao.find_by_id(args["id"])
    return {
        "id": run_dto.id,
        "jobId": run_dto.job_id,
        "uuid": run_dto.uuid,
        "status": run_dto.status,
        "started": run_dto.started,
        "ended": run_dto.ended
    }


resolvers = {
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

schema = build_executable_schema(get_schema_def(), resolvers)
