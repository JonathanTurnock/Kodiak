from kodiak.agent.model.status import Status
from kodiak.server.papi.connection_factory import get_connection


def run_dto_of_run(run):
    return RunDto(
        id=run.id,
        job_id=run.job.id,
        uuid=run.uuid,
        status=run.status,
        started=run.started,
        ended=run.ended
    )


class RunDto(object):
    def __init__(
            self,
            id: int = None,
            job_id: int = None,
            uuid: str = None,
            status: Status = None,
            started=None,
            ended=None
    ):
        self.id: int = id
        self.job_id: int = job_id
        self.uuid: str = uuid
        self.status: str = status.name
        self.started = started
        self.ended = ended

    @staticmethod
    def of_row(row):
        return RunDto(
            id=row[0],
            job_id=row[1],
            uuid=row[2],
            status=Status.value_of(row[3]),
            started=row[4],
            ended=row[5]
        )


class RunDao:
    _INSERT_NEW_RUN = "insert into run (job_id, uuid, status, started, ended) values (?, ?, ?, ?, ?)"
    _UPDATE_EXISTING_RUN = "update run set job_id=?, uuid=?, status=?, started=?, ended=? where id=?"
    _FIND_BY_ID = "select id, job_id, uuid, status, started, ended from run where id=?"

    def save(self, run: RunDto) -> RunDto:
        _connection = get_connection()
        try:
            if run.id is None:
                cursor = _connection.execute(RunDao._INSERT_NEW_RUN,
                                             [run.job_id, run.uuid, run.status, run.started, run.ended])
                run.id = cursor.lastrowid
            else:
                _connection.execute(RunDao._UPDATE_EXISTING_RUN,
                                    [run.job_id, run.uuid, run.status, run.started, run.ended, run.id])
            _connection.commit()
            return run
        finally:
            _connection.close()

    def find_by_id(self, id) -> RunDto:
        _connection = get_connection()
        try:
            cursor = _connection.execute(RunDao._FIND_BY_ID, [id])
            return RunDto.of_row(cursor.fetchone())
        finally:
            _connection.close()
