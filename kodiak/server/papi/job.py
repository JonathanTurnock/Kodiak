from typing import List

from kodiak.server.papi.connection_factory import get_connection


def job_dto_of_job(job):
    j = JobDto()
    j.id = job.id
    j.name = job.name
    j.url = job.url
    return j


class JobDto(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.url = None

    @staticmethod
    def of_row(row):
        job = JobDto()
        job.id = row[0]
        job.name = row[1]
        job.url = row[2]
        return job


class JobDao:
    _FIND_ALL_JOBS = "select id, name, url from job"
    _INSERT_NEW_JOB = "insert into job (name, url) values (?, ?)"
    _UPDATE_EXISTING_JOB = "update job set name=?, url=? where id=?"
    _FIND_JOB_BY_ID = "select id, name, url from job where id = ?"

    def save(self, job: JobDto) -> JobDto:
        _connection = get_connection()
        try:
            if job.id is None:
                cursor = _connection.execute(JobDao._INSERT_NEW_JOB, [job.name, job.url])
                job.id = cursor.lastrowid
            else:
                _connection.execute(JobDao._UPDATE_EXISTING_JOB, [job.name, job.url, job.id])
            _connection.commit()
            return job
        finally:
            _connection.close()

    def find_job_by_id(self, id) -> JobDto:
        _connection = get_connection()
        try:
            cursor = _connection.execute(JobDao._FIND_JOB_BY_ID, [id])
            return JobDto.of_row(cursor.fetchone())
        finally:
            _connection.close()

    def find_jobs(self) -> List[JobDto]:
        _connection = get_connection()
        try:
            cursor = _connection.execute(JobDao._FIND_ALL_JOBS)
            results = cursor.fetchall()
            return [JobDto.of_row(row) for row in results]
        finally:
            _connection.close()
