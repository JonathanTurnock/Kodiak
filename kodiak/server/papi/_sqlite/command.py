import logging
from sqlite3 import IntegrityError
from typing import List, Tuple

import jsonpickle

from kodiak.server.papi._sqlite._interfaces import Dto
from kodiak.server.papi._sqlite.connection_factory import FetchOneException, sql_fetch, sql_commit
from kodiak.server.papi.exception import NoResultException

LOGGER = logging.getLogger(__name__)


class CommandDto(Dto):
    def __init__(
            self,
            id: int = None,
            step_id: int = None,
            number: int = None,
            instruction: str = None,
            std_out: List[str] = None,
            std_err: List[str] = None
    ):
        self.id: int = id
        self.step_id: int = step_id
        self.number: int = number
        self.instruction: str = instruction
        self.std_out: List[str] = std_out
        self.std_err: List[str] = std_err

    def parameterize(self) -> dict:
        return {
            "id": self.id,
            "step_id": self.step_id,
            "number": self.number,
            "instruction": self.instruction,
            "std_out": jsonpickle.encode(self.std_out),
            "std_err": jsonpickle.encode(self.std_err),
        }


class CommandDao:
    _INSERT_COMMAND = "insert into command (step_id, number, instruction, std_out, std_error) values (:step_id, :number, :instruction, :std_out, :std_err)"
    _UPDATE_COMMAND = "update command set step_id=:step_id, number=:number, instruction=:instruction, std_out=:std_out, std_error=:std_err where id=:id"
    _FIND_BY_ID = "select id, step_id, number, instruction, std_out, std_error from command where id=?"
    _FIND_BY_STEP_ID = "select id, step_id, number, instruction, std_out, std_error from command where step_id=?"
    _FIND_BY_STEP_ID_AND_NUMBER = "select id, step_id, number, instruction, std_out, std_error from command where step_id=? and number=?"

    @staticmethod
    def save(command: CommandDto) -> CommandDto:
        try:
            return CommandDao._do_insert(command)
        except IntegrityError as e:
            return CommandDao._do_update(command)

    @staticmethod
    def find_by_id(id: int) -> CommandDto:
        try:
            with sql_fetch(CommandDao._FIND_BY_ID, [id], row_mapper=CommandDao._map_full_row, size=1) as command_dto:
                return command_dto
        except FetchOneException:
            raise NoResultException(f"No Command Found with id: {id}") from None

    @staticmethod
    def find_all_by_step_id(step_id: int) -> List[CommandDto]:
        with sql_fetch(CommandDao._FIND_BY_STEP_ID, [step_id], row_mapper=CommandDao._map_full_row,
                       size=0) as step_dtos:
            return step_dtos

    @staticmethod
    def find_by_step_id_and_number(step_id: int, number: int) -> CommandDto:
        try:
            with sql_fetch(CommandDao._FIND_BY_STEP_ID_AND_NUMBER, [step_id, number],
                           row_mapper=CommandDao._map_full_row,
                           size=1) as command_dto:
                return command_dto
        except FetchOneException:
            raise NoResultException(f"No Command Found with step_id: {step_id} and number: {number}") from None

    @staticmethod
    def _map_full_row(row: Tuple) -> CommandDto:
        _id, _step_id, _number, _instruction, _std_out, _std_err = row
        return CommandDto(id=_id, step_id=_step_id, number=_number, instruction=_instruction,
                          std_out=jsonpickle.decode(_std_out),
                          std_err=jsonpickle.decode(_std_err))

    @staticmethod
    def _do_insert(command: CommandDto) -> CommandDto:
        with sql_commit(CommandDao._INSERT_COMMAND, command.parameterize()) as last_row_id:
            LOGGER.debug(f"Added command with id: {last_row_id}")
            return CommandDao.find_by_id(last_row_id)

    @staticmethod
    def _do_update(command: CommandDto) -> CommandDto:
        existing_row = CommandDao.find_by_step_id_and_number(command.step_id, command.number)
        updated_row = CommandDto(
            id=existing_row.id,
            step_id=command.step_id,
            number=command.number,
            instruction=command.instruction,
            std_out=command.std_out,
            std_err=command.std_err
        )
        with sql_commit(CommandDao._UPDATE_COMMAND, updated_row.parameterize()) as last_row_id:
            LOGGER.debug(f"Updated existing command with id: {existing_row.id}")
            return updated_row
