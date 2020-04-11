from typing import List

from kodiak.agent.model.job import Job
from kodiak.server.papi.connection_factory import get_connection


def map_row(row):
    job = Job(row[2], row[3])
    job.uuid = row[1]
    job.id = row[0]
    return job


class JobDao:
    _FIND_ALL_JOBS = "select id, uuid, name, url from job"
    _FIND_JOB_BY_UUID = "select id, uuid, name, url from job where uuid = ?"
    _INSERT_NEW_JOB = "insert into job (uuid, name, url) values (?, ?, ?)"
    _UPDATE_EXISTING_JOB = "update job set uuid=?, name=?, url=? where id=?"

    def save(self, job: Job) -> Job:
        _connection = get_connection()
        try:
            if job.id is None:
                _connection.execute(JobDao._INSERT_NEW_JOB, [job.uuid, job.name, job.url])
            else:
                _connection.execute(JobDao._UPDATE_EXISTING_JOB, [job.uuid, job.name, job.url, job.id])
            _connection.commit()
            cursor = _connection.execute(JobDao._FIND_JOB_BY_UUID, [job.uuid])
            return map_row(cursor.fetchone())
        finally:
            _connection.close()

    def find_job_by_uuid(self, uuid):
        _connection = get_connection()
        try:
            cursor = _connection.execute(JobDao._FIND_JOB_BY_UUID, [uuid])
            return map_row(cursor.fetchone())
        finally:
            _connection.close()

    def find_jobs(self) -> List[Job]:
        _connection = get_connection()
        try:
            cursor = _connection.execute(JobDao._FIND_ALL_JOBS)
            results = cursor.fetchall()
            return [map_row(row) for row in results]
        finally:
            _connection.close()
