import logging

import docker
from docker import DockerClient
from docker.models.containers import Container
from fxq.core.stereotype import Service

from fxq.ae.runner import constants
from fxq.ae.runner.model import Command

LOGGER = logging.getLogger(__name__)


@Service
class DockerService:

    def __init__(self):
        self._docker_client: DockerClient = docker.from_env()

    def provision(self, name: str, image: str, workspace_path: str = None) -> Container:
        name = name.replace(" ", "_")
        image = image if ":" in image else image + ":latest"
        LOGGER.info("Pulling Container Image %s" % image)
        self._docker_client.images.pull(image)
        LOGGER.info("Provisioning Container \"%s\" with Image:\"%s\"" % (name, image))
        if workspace_path is None:
            return self._provision_without_volume(name, image)
        else:
            return self._provision_with_volume(name, image, workspace_path)

    def run_command(self, container: Container, command: Command) -> Command:
        LOGGER.info("Running Container Command \"%s\"" % command.instruction)
        response = container.exec_run(
            ["/bin/sh", "-c", command.instruction],
            privileged=True,
            tty=True,
            stream=True,
            demux=False,
            workdir=constants.PIPELINE_MOUNT_TARGET
        )
        while True:
            try:
                command.append_output(next(response.output).decode())
            except StopIteration:
                break

        return command

    def teardown(self, container: Container):
        LOGGER.debug("Starting Teardown")
        container.stop(timeout=1)
        container.remove()

    def _provision_without_volume(self, name: str, image: str) -> Container:
        return self._docker_client.containers.run(
            name=name,
            image=image,
            command="tail -f /dev/stdout",
            detach=True
        )

    def _provision_with_volume(self, name: str, image: str, workspace_path: str) -> Container:
        return self._docker_client.containers.run(
            name=name,
            image=image,
            command="tail -f /dev/stdout",
            detach=True,
            volumes={
                workspace_path: {
                    'bind': constants.PIPELINE_MOUNT_TARGET,
                    'mode': 'rw'
                }
            }
        )
