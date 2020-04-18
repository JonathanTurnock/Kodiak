import logging
from datetime import datetime
from sqlite3 import IntegrityError
from typing import Tuple, List

from kodiak.server.papi._sqlite._interfaces import Dto
from kodiak.server.papi._sqlite.connection_factory import sql_fetch, FetchOneException, sql_commit
from kodiak.server.papi.exception import NoResultException

LOGGER = logging.getLogger(__name__)


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
    _INSERT_RUN = "insert into run (job_id, uuid, status, started, ended) values (:job_id, :uuid, :status, :started, :ended)"
    _DELETE_RUN = "delete from run where id=?"
    _UPDATE_RUN = "update run set job_id=:job_id, uuid=:uuid, status=:status, started=:started, ended=:ended where id=:id"
    _FIND_BY_ID = "select id, job_id, uuid, status, started, ended from run where id=?"
    _FIND_BY_UUID = "select id, job_id, uuid, status, started, ended from run where uuid=?"
    _FIND_ALL_BY_JOB_ID = "select id, job_id, uuid, status, started, ended from run where job_id=?"

    @staticmethod
    def save(run: RunDto) -> RunDto:
        try:
            return RunDao._do_insert(run)
        except IntegrityError as e:
            return RunDao._do_update(run)

    @staticmethod
    def find_by_id(id: int) -> RunDto:
        try:
            with sql_fetch(RunDao._FIND_BY_ID, [id], row_mapper=RunDao._map_full_row, size=1) as run_dto:
                return run_dto
        except FetchOneException:
            raise NoResultException(f"No Run Found with id: {id}") from None

    @staticmethod
    def find_by_uuid(uuid: str) -> RunDto:
        try:
            with sql_fetch(RunDao._FIND_BY_UUID, [uuid], row_mapper=RunDao._map_full_row, size=1) as run_dto:
                return run_dto
        except FetchOneException:
            raise NoResultException(f"No Run Found with uuid: {uuid}") from None

    @staticmethod
    def find_all_by_job_id(id: int) -> List[RunDto]:
        with sql_fetch(RunDao._FIND_ALL_BY_JOB_ID, [id], row_mapper=RunDao._map_full_row, size=0) as run_dtos:
            return run_dtos

    @staticmethod
    def delete(run: RunDto) -> None:
        with sql_commit(RunDao._DELETE_RUN, [run.id]):
            LOGGER.debug(f"Removed Run with id: {run.id}")

    @staticmethod
    def _map_full_row(row: Tuple) -> RunDto:
        _id, _job_id, _uuid, _status, _started, _ended = row
        return RunDto(id=_id, job_id=_job_id, uuid=_uuid, status=_status, started=_started, ended=_ended)

    @staticmethod
    def _do_insert(job: RunDto) -> RunDto:
        with sql_commit(RunDao._INSERT_RUN, job.parameterize()) as last_row_id:
            LOGGER.debug(f"Added run with id: {last_row_id}")
            return RunDao.find_by_id(last_row_id)

    @staticmethod
    def _do_update(run: RunDto) -> RunDto:
        existing_row = RunDao.find_by_uuid(run.uuid)
        updated_row = RunDto(
            id=existing_row.id,
            job_id=run.job_id,
            uuid=existing_row.uuid,
            status=run.status,
            started=run.started,
            ended=run.ended
        )
        with sql_commit(RunDao._UPDATE_RUN, updated_row.parameterize()) as last_row_id:
            LOGGER.debug(f"Updated existing run with id: {existing_row.id}")
            return updated_row
