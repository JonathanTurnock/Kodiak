import logging
from sqlite3 import IntegrityError
from typing import List, Tuple

from kodiak.model.run import Status
from kodiak.server.papi._sqlite._interfaces import Dto
from kodiak.server.papi._sqlite.connection_factory import sql_commit, sql_fetch, FetchOneException
from kodiak.server.papi.exception import NoResultException

LOGGER = logging.getLogger(__name__)


class StepDto(Dto):
    def __init__(
            self,
            id: int = None,
            run_id: int = None,
            number: int = None,
            name: str = None,
            image: str = None,
            status: str = None
    ):
        self.id: int = id
        self.run_id: int = run_id
        self.number: int = number
        self.name: str = name
        self.image: str = image
        self.status: str = status

    def parameterize(self) -> dict:
        return {
            "id": self.id,
            "run_id": self.run_id,
            "number": self.number,
            "name": self.name,
            "image": self.image,
            "status": self.status
        }


class StepDao:
    _INSERT_STEP = "insert into step (run_id, number, name, image, status) values (:run_id, :number, :name, :image, :status)"
    _UPDATE_STEP = "update step set run_id=:run_id, number=:number, name=:name, image=:image, status=:status where id=:id"
    _FIND_BY_ID = "select id, run_id, number, name, image, status from step where id=?"
    _FIND_BY_RUN_ID = "select id, run_id, number, name, image, status from step where run_id=?"
    _FIND_BY_RUN_ID_AND_NUMBER = "select id, run_id, number, name, image, status from step where run_id=? and number=?"

    @staticmethod
    def save(step: StepDto) -> StepDto:
        try:
            return StepDao._do_insert(step)
        except IntegrityError as e:
            return StepDao._do_update(step)

    @staticmethod
    def find_by_id(id: int) -> StepDto:
        try:
            with sql_fetch(StepDao._FIND_BY_ID, [id], row_mapper=StepDao._map_full_row, size=1) as step_dto:
                return step_dto
        except FetchOneException:
            raise NoResultException(f"No Step Found with id: {id}") from None

    @staticmethod
    def find_all_by_run_id(run_id: int) -> List[StepDto]:
        with sql_fetch(StepDao._FIND_BY_RUN_ID, [run_id], row_mapper=StepDao._map_full_row, size=0) as step_dtos:
            return step_dtos

    @staticmethod
    def find_by_run_id_and_number(run_id: int, number: int):
        try:
            with sql_fetch(StepDao._FIND_BY_RUN_ID_AND_NUMBER, [run_id, number], row_mapper=StepDao._map_full_row,
                           size=1) as step_dto:
                return step_dto
        except FetchOneException:
            raise NoResultException(f"No Step Found with run_id: {run_id} and number: {number}")

    @staticmethod
    def _map_full_row(row: Tuple) -> StepDto:
        _id, _run_id, _number, _name, _image, _status = row
        return StepDto(id=_id, run_id=_run_id, number=_number, name=_name, image=_image,
                       status=Status.value_of(_status))

    @staticmethod
    def _do_insert(step: StepDto) -> StepDto:
        with sql_commit(StepDao._INSERT_STEP, step.parameterize()) as last_row_id:
            LOGGER.debug(f"Added step with id: {last_row_id}")
            return StepDao.find_by_id(last_row_id)

    @staticmethod
    def _do_update(step: StepDto) -> StepDto:
        existing_row = StepDao.find_by_run_id_and_number(step.run_id, step.number)
        updated_row = StepDto(
            id=existing_row.id,
            run_id=step.run_id,
            number=step.number,
            name=step.name,
            image=step.image,
            status=step.status
        )
        with sql_commit(StepDao._UPDATE_STEP, updated_row.parameterize()) as last_row_id:
            LOGGER.debug(f"Updated existing run with id: {existing_row.id}")
            return updated_row
