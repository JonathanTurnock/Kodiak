from pathlib import Path

import yaml

from kodiak.agent.model.job import Job
from kodiak.agent.model.run import Run, Command, Step
from kodiak.agent.service.run import RunException


class RunFactory:

    @staticmethod
    def prepare(job: Job):
        return Run(job)

    @staticmethod
    def configure_from_yml_file(run: Run, yml_path: str) -> Run:
        RunFactory.__validate_clone(yml_path)
        RunFactory.__validate_yml_presence(yml_path)
        with open(yml_path) as ymlf:
            run_yml = yaml.load(ymlf, Loader=yaml.SafeLoader)
            s_no = 0
            for s in run_yml["pipelines"]["steps"]:
                s_no += 1
                step = Step(run, s_no, s["step"]["name"], s["step"]["image"])
                se_no = 0
                for se in s["step"]["script"]:
                    se_no += 1
                    command = Command(step, se_no, se)
                    step.commands.append(command)

                run.steps.append(step)

            return run

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
