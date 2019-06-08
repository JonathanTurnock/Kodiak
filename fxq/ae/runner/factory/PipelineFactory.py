from fxq.core.stereotype import Component

from fxq.ae.runner.model import Pipeline, Step
from fxq.ae.runner.model.Command import Command


@Component
class PipelineFactory:

    def pipeline_of(self, name: str, pipeline_dict: dict):
        pipeline = Pipeline(None, name)
        for s in pipeline_dict["pipelines"]["steps"]:
            step = Step(s["step"]["name"], s["step"]["image"])
            for se in s["step"]["script"]:
                command = Command(se)
                step.add_script_command(command)

            pipeline.add_step(step)

        return pipeline
