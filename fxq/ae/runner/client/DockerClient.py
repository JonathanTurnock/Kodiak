import logging

import docker
import yaml
from docker.errors import ContainerError
from fxq.core.stereotype import Component
from git import Repo

from fxq.ae.runner import constants

LOGGER = logging.getLogger("DockerClient")


@Component
class DockerClient:

    def __init__(self):
        self._client = docker.from_env()

    def execute_pipeline_from_repo(self, repo: Repo):
        workspace_path = repo.working_dir
        with open("%s/%s" % (workspace_path, constants.PIPELINE_YML_NAME)) as ymlf:
            pipeline_config = yaml.load(ymlf, Loader=yaml.SafeLoader)
            LOGGER.debug("Loaded YAML Config file %s" % pipeline_config)

        for step in pipeline_config["pipelines"]["default"]:
            try:
                LOGGER.info("Running Step %s" % step["step"]["name"])
                container = self._client.containers.run(
                    name="TEST",
                    image=pipeline_config["image"],
                    command="tail -f /dev/null",
                    detach=True,
                    volumes={
                        workspace_path: {
                            'bind': constants.PIPELINE_MOUNT_TARGET,
                            'mode': 'rw'
                        }
                    }
                )

                for script_entry in step["step"]["script"]:
                    LOGGER.info(self._run_script(container, script_entry))

            except ContainerError as e:
                LOGGER.error(e.stderr)
            finally:
                LOGGER.info("Pipeline Teardown")
                container = self._client.containers.get("TEST")
                container.stop(timeout=1)
                container.remove()

                try:
                    if step["step"]["commit"]:
                        repo.git.add('--all')
                        repo.git.commit(message="FXQ Pipeline Commit")
                        repo.git.push()
                except KeyError:
                    pass
                except Exception as e:
                    LOGGER.error("Failed to commit changes ", e)


    def _run_script(self, container, script):
        exec_output = container.exec_run(
            ["/bin/bash", "-c", script],
            privileged=True,
            tty=True,
            workdir=constants.PIPELINE_MOUNT_TARGET
        )

        return "%s:\n%s" % (script, exec_output[1].decode().strip())
