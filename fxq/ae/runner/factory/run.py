import yaml

from fxq.ae.runner.model.job import Job
from fxq.ae.runner.model.run import Run, Command, Step


class RunFactory:

    @staticmethod
    def get_from_yml_file(job: Job, yml_path: str) -> Run:
        with open(yml_path) as ymlf:
            run_yml = yaml.load(ymlf, Loader=yaml.SafeLoader)
            run = Run(job)
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
