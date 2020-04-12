from kodiak.agent.model.status import Status
from kodiak.server.papi.connection_factory import get_connection


def step_dto_of_step(step):
    return StepDto(
        id=step.id,
        run_id=step.run.id,
        number=step.number,
        name=step.name,
        image=step.image,
        status=step.status
    )


class StepDto(object):
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


class StepDao:
    _INSERT_NEW_STEP = "insert into step (run_id, number, name, image, status) values (?, ?, ?, ?, ?)"
    _UPDATE_EXISTING_STEP = "update step set run_id=?, number=?, name=?, image=?, status=? where id=?"

    def save(self, step: StepDto) -> StepDto:
        _connection = get_connection()
        try:
            if step.id is None:
                cursor = _connection.execute(StepDao._INSERT_NEW_STEP,
                                             [step.run_id, step.number, step.name, step.image, step.status])
                step.id = cursor.lastrowid
            else:
                _connection.execute(StepDao._UPDATE_EXISTING_STEP,
                                    [step.run_id, step.number, step.name, step.image, step.status, step.id])
            _connection.commit()
            return step
        finally:
            _connection.close()
