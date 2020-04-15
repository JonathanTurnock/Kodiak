import logging
from typing import Tuple, List

from kodiak.model.run import Status
from kodiak.server.papi._sqlite._interfaces import Dto
from kodiak.server.papi._sqlite.connection_factory import sql_commit, sql_fetch, FetchOneException
from kodiak.server.papi.exception import NoResultException

LOGGER = logging.getLogger(__name__)


def step_dto_of_step(step):
    return StepDto(
        id=step.id,
        run_id=step.run.id,
        number=step.number,
        name=step.name,
        image=step.image,
        status=step.status
    )


class StepDto(Dto):
    def __init__(
            self,
            id: int = None,
            run_id: int = None,
            number: int = None,
            name: str = None,
            image: str = None,
            status: Status = None
    ):
        self.id: int = id
        self.run_id: int = run_id
        self.number: int = number
        self.name: str = name
        self.image: str = image
        self.status: str = status.name

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
    _INSERT_NEW_STEP = "insert into step (run_id, number, name, image, status) values (?, ?, ?, ?, ?)"
    _UPDATE_EXISTING_STEP = "update step set run_id=?, number=?, name=?, image=?, status=? where id=?"
    _FIND_BY_ID = "select id, run_id, number, name, image, status from step where id=?"
    _FIND_BY_RUN_ID = "select id, run_id, number, name, image, status from step where run_id=?"

    @staticmethod
    def map_full_row(row: Tuple) -> StepDto:
        _id, _run_id, _number, _name, _image, _status = row
        return StepDto(id=_id, run_id=_run_id, number=_number, name=_name, image=_image,
                       status=Status.value_of(_status))

    @staticmethod
    def save(step: StepDto) -> StepDto:
        if step.id is None:
            with sql_commit(StepDao._INSERT_NEW_STEP,
                            [step.run_id, step.number, step.name, step.image, step.status]) as last_row_id:
                LOGGER.info(f"Added new job with with id: {last_row_id}")
                step.id = last_row_id
        else:
            with sql_commit(StepDao._UPDATE_EXISTING_STEP,
                            [step.run_id, step.number, step.name, step.image, step.status, step.id]) as last_row_id:
                LOGGER.info(f"Updated existing step with with id: {last_row_id}")
        return StepDao.find_by_id(step.id)

    @staticmethod
    def find_by_id(id: int) -> StepDto:
        try:
            with sql_fetch(StepDao._FIND_BY_ID, [id], row_mapper=StepDao.map_full_row, size=1) as step_dto:
                return step_dto
        except FetchOneException:
            raise NoResultException(f"No Step Found with id: {id}") from None

    @staticmethod
    def find_all_by_run_id(run_id: int) -> List[StepDto]:
        try:
            with sql_fetch(StepDao._FIND_BY_RUN_ID, [run_id], row_mapper=StepDao.map_full_row, size=0) as step_dtos:
                return step_dtos
        except FetchOneException:
            raise NoResultException(f"No Steps Found with run_id: {run_id}") from None
