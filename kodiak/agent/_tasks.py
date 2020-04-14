from datetime import datetime
from pathlib import Path
from typing import List

import yaml

from kodiak.agent._callback import do_callback
from kodiak.agent._errors import RunException
from kodiak.model.run import Status, Run, Step, Command
from kodiak.utils.id import new_string_id


class RunTask:
    def __init__(self, job):
        self._run = Run(
            job=job,
            uuid=new_string_id(),
            status=Status.PENDING,
        )
        self.uuid = self._run.uuid
        do_callback(self)

    def start(self) -> None:
        self._run.status = Status.IN_PROGRESS
        self._run.started = datetime.now()
        do_callback(self)

    def complete(self) -> None:
        self._run.status = Status.SUCCESSFUL
        self._run.ended = datetime.now()
        do_callback(self)

    def fail(self) -> None:
        self._run.status = Status.FAILED
        self._run.ended = datetime.now()
        do_callback(self)

    def is_in_progress(self) -> bool:
        return self._run.status == Status.IN_PROGRESS

    def is_failed(self) -> bool:
        return self._run.status == Status.FAILED

    def get_run(self) -> Run:
        return self._run

    def get_step(self, step_no: int) -> Step:
        return self._run.steps[step_no]

    def get_steps(self) -> List[Step]:
        return self._run.steps

    def start_step(self, step_no: int):
        self._run.steps[step_no - 1].status = Status.IN_PROGRESS
        do_callback(self)

    def complete_step(self, step_no: int):
        self._run.steps[step_no - 1].status = Status.SUCCESSFUL
        do_callback(self)

    def fail_step(self, step_no: int):
        self._run.steps[step_no - 1].status = Status.FAILED
        do_callback(self)

    def abort_step(self, step_no: int):
        self._run.steps[step_no - 1].status = Status.ABORTED
        do_callback(self)

    def abort_pending_steps(self):
        for step in self.get_steps():
            if self.step_is_pending(step.number):
                self.abort_step(step.number)
        do_callback(self)

    def step_is_in_progress(self, step_no: int) -> bool:
        return self._run.steps[step_no - 1].status == Status.IN_PROGRESS

    def step_is_failed(self, step_no: int) -> bool:
        return self._run.steps[step_no - 1].status == Status.FAILED

    def step_is_pending(self, step_no: int) -> bool:
        return self._run.steps[step_no - 1].status == Status.PENDING

    def get_command(self, step_no: int, command_no: int) -> Command:
        return self._run.steps[step_no - 1].commands[command_no - 1]

    def get_commands(self, step_no: int) -> List[Command]:
        return self._run.steps[step_no - 1].commands

    def add_output(self, step_no: int, command_no: int, output: str):
        self._run.steps[step_no - 1].commands[command_no - 1].std_out.append(output)
        do_callback(self)

    def add_error(self, step_no: int, command_no: int, error: str):
        self._run.steps[step_no - 1].commands[command_no - 1].std_err.append(error)
        do_callback(self)

    def configure_from_yml_file(self, yml_path: str):
        RunTask.__validate_clone(yml_path)
        RunTask.__validate_yml_presence(yml_path)
        with open(yml_path) as ymlf:
            run_yml = yaml.load(ymlf, Loader=yaml.SafeLoader)
            s_no = 0
            for s in run_yml["pipelines"]["steps"]:
                s_no += 1
                step = Step(
                    run=self._run,
                    number=s_no,
                    name=s["step"]["name"],
                    image=s["step"]["image"])
                se_no = 0
                for script_entry in s["step"]["script"]:
                    se_no += 1
                    command = Command(
                        step=step,
                        number=se_no,
                        instruction=script_entry)
                    step.commands.append(command)

                self._run.steps.append(step)
        do_callback(self)

    @staticmethod
    def __validate_clone(yml_path):
        yml_path_parent = Path(yml_path).parent
        if not yml_path_parent.exists():
            raise RunException(f"Clone not completed as folder {yml_path_parent.absolute()} does not exist")

    @staticmethod
    def __validate_yml_presence(yml_path):
        yml_path = Path(yml_path)
        if not yml_path.exists():
            raise RunException(f"Unable to locate {yml_path.absolute()}, are you sure the file exists in the repo?")
