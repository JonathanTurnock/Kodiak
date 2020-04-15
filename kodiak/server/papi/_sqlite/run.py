import logging
from datetime import datetime
from typing import Tuple

from kodiak.model.run import Run
from kodiak.server.papi._sqlite._interfaces import Dto
from kodiak.server.papi._sqlite.connection_factory import sql_fetch, FetchOneException, sql_commit
from kodiak.server.papi.exception import NoResultException

LOGGER = logging.getLogger(__name__)


def run_dto_of_run(run: Run):
    return RunDto(
        id=run.id,
        job_id=run.job.id,
        uuid=run.uuid,
        status=run.status.name,
        started=run.started,
        ended=run.ended
    )


class RunDto(Dto):
    def __init__(
            self,
            id: int = None,
            job_id: int = None,
            uuid: str = None,
            status: str = None,
            started: datetime = None,
            ended: datetime = None
    ):
        self.id: int = id
        self.job_id: int = job_id
        self.uuid: str = uuid
        self.status: str = status
        self.started: datetime = started
        self.ended: datetime = ended

    def parameterize(self) -> dict:
        return {
            "id": self.id,
            "job_id": self.job_id,
            "uuid": self.uuid,
            "status": self.status,
            "started": self.started,
            "ended": self.ended
        }


class RunDao:
    _INSERT_NEW_RUN = "insert into run (job_id, uuid, status, started, ended) values (?, ?, ?, ?, ?)"
    _UPDATE_EXISTING_RUN = "update run set job_id=?, uuid=?, status=?, started=?, ended=? where id=?"
    _FIND_BY_ID = "select id, job_id, uuid, status, started, ended from run where id=?"
    _FIND_BY_UUID = "select id, job_id, uuid, status, started, ended from run where uuid=?"

    @staticmethod
    def map_full_row(row: Tuple) -> RunDto:
        _id, _job_id, _uuid, _status, _started, _ended = row
        return RunDto(id=_id, job_id=_job_id, uuid=_uuid, status=_status, started=_started, ended=_ended)

    @staticmethod
    def save(run: RunDto) -> RunDto:
        if run.id is None:
            with sql_commit(RunDao._INSERT_NEW_RUN,
                            [run.job_id, run.uuid, run.status, run.started, run.ended]) as last_row_id:
                run.id = last_row_id
                LOGGER.info(f"Added new run with with id: {last_row_id}")
        else:
            with sql_commit(RunDao._UPDATE_EXISTING_RUN,
                            [run.job_id, run.uuid, run.status, run.started, run.ended, run.id]) as last_row_id:
                LOGGER.info(f"Updated run with with id: {last_row_id}")

        return RunDao.find_by_id(run.id)

    @staticmethod
    def find_by_id(id: int) -> RunDto:
        try:
            with sql_fetch(RunDao._FIND_BY_ID, [id], row_mapper=RunDao.map_full_row, size=1) as run_dto:
                return run_dto
        except FetchOneException:
            raise NoResultException(f"No Run Found with id: {id}") from None

    @classmethod
    def find_by_uuid(cls, uuid: str):
        try:
            with sql_fetch(RunDao._FIND_BY_UUID, [uuid], row_mapper=RunDao.map_full_row, size=1) as run_dto:
                return run_dto
        except FetchOneException:
            raise NoResultException(f"No Run Found with uuid: {uuid}") from None
