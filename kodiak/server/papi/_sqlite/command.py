import logging
from typing import List, Tuple

import jsonpickle

from kodiak.server.papi._sqlite.connection_factory import sql_commit, FetchOneException, sql_fetch
from kodiak.server.papi.exception import NoResultException

LOGGER = logging.getLogger(__name__)


def command_dto_of_command(command):
    return CommandDto(
        id=command.id,
        step_id=command.step.id,
        number=command.number,
        instruction=command.instruction,
        std_out=command.std_out,
        std_err=command.std_err
    )


class CommandDto(object):
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


class CommandDao:
    _INSERT_NEW_COMMAND = "insert into command (step_id, number, instruction, std_out, std_error) values (?, ?, ?, ?, ?)"
    _UPDATE_EXISTING_COMMAND = "update command set step_id=?, number=?, instruction=?, std_out=?, std_error=? where id=?"
    _FIND_BY_ID = "select id, step_id, number, instruction, std_out, std_error from command where id=?"
    _FIND_BY_STEP_ID = "select id, step_id, number, instruction, std_out, std_error from command where step_id=?"

    @staticmethod
    def map_full_row(row: Tuple) -> CommandDto:
        _id, _step_id, _number, _instruction, _std_out, _std_err = row
        return CommandDto(id=_id, step_id=_step_id, number=_number, instruction=_instruction,
                          std_out=jsonpickle.decode(_std_out),
                          std_err=jsonpickle.decode(_std_err))

    @staticmethod
    def save(command: CommandDto) -> CommandDto:
        if command.id is None:
            with sql_commit(CommandDao._INSERT_NEW_COMMAND,
                            [command.step_id, command.number, command.instruction, jsonpickle.encode(command.std_out),
                             jsonpickle.encode(command.std_err)]) as last_row_id:
                LOGGER.debug(f"Added new command with with id: {last_row_id}")
                command.id = last_row_id
        else:
            with sql_commit(CommandDao._UPDATE_EXISTING_COMMAND,
                            [command.step_id, command.number, command.instruction, jsonpickle.encode(command.std_out),
                             jsonpickle.encode(command.std_err),
                             command.id]) as last_row_id:
                LOGGER.debug(f"Updated existing command with with id: {last_row_id}")
        return CommandDao.find_by_id(command.id)

    @staticmethod
    def find_by_id(id: int) -> CommandDto:
        try:
            with sql_fetch(CommandDao._FIND_BY_ID, [id], row_mapper=CommandDao.map_full_row, size=1) as command_dto:
                return command_dto
        except FetchOneException:
            raise NoResultException(f"No Command Found with id: {id}") from None

    @staticmethod
    def find_all_by_step_id(step_id: int) -> List[CommandDto]:
        try:
            with sql_fetch(CommandDao._FIND_BY_STEP_ID, [step_id], row_mapper=CommandDao.map_full_row,
                           size=0) as step_dtos:
                return step_dtos
        except FetchOneException:
            raise NoResultException(f"No Commands Found with step_id: {step_id}") from None
