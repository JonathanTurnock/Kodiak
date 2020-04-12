from typing import List

from kodiak.server.papi.connection_factory import get_connection


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
        self.std_out: str = str(std_out)
        self.std_err: str = str(std_err)


class CommandDao:
    _INSERT_NEW_COMMAND = "insert into command (step_id, number, instruction, std_out, std_error) values (?, ?, ?, ?, ?)"
    _UPDATE_EXISTING_COMMAND = "update command set step_id=?, number=?, instruction=?, std_out=?, std_error=? where id=?"

    def save(self, command: CommandDto) -> CommandDto:
        _connection = get_connection()
        try:
            if command.id is None:
                cursor = _connection.execute(CommandDao._INSERT_NEW_COMMAND,
                                             [command.step_id, command.number, command.instruction, command.std_out,
                                              command.std_err])
                command.id = cursor.lastrowid
            else:
                _connection.execute(CommandDao._UPDATE_EXISTING_COMMAND,
                                    [command.step_id, command.number, command.instruction, command.std_out,
                                     command.std_err, command.id])
            _connection.commit()
            return command
        finally:
            _connection.close()
