import logging
import os
import shutil
import threading

from docker import DockerClient, from_env
from docker.models.containers import Container
from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Service
from git import Repo

from bootstrap import PIPELINE_MOUNT_TARGET, PROJECTS_FOLDER, PIPELINE_YML_NAME
from kodiak.agent._errors import RunException, StdErrException, StepException
from kodiak.agent._tasks import RunTask
from kodiak.model.job import Job
from kodiak.utils.id import new_string_id
from kodiak.utils.paths import get_working_dir, working_dir

LOGGER = logging.getLogger(__name__)


@Service(name="docker_service")
class DockerService:

    def __init__(self):
        self._docker_client: DockerClient = from_env()

    def list_containers(self):
        return self._docker_client.containers.list()

    def provision(self, name: str, image: str, workspace_path: str = None) -> Container:
        """
        Provisions a docker container with the given name, based off the given image.

        The Workspace is then mounted if provided allowing the files within the workspace to be accessed from within the
        docker container.

        :param name: Name for the Container
        :param image: Image for the Container
        :param workspace_path: Workspace to Mount into the Container
        :return: Returns the running Container
        """
        name = name.replace(" ", "_")
        image = image if ":" in image else image + ":latest"
        LOGGER.info("Pulling Container Image %s" % image)
        self._docker_client.images.pull(image)
        LOGGER.info("Provisioning Container \"%s\" with Image:\"%s\"" % (name, image))
        if workspace_path is None:
            return self._provision_without_volume(name, image)
        else:
            return self._provision_with_volume(name, image, workspace_path)

    def run_command(self, container: Container, instruction: str):
        """
        Executes the given instruction on the container and returns the output.

        :param container: Container to send the instruction to
        :param instruction: Instruction to send via sh
        :return: Returns the instruction output
        """
        LOGGER.info("Running Container Command \"%s\"" % instruction)
        response = container.exec_run(
            ["/bin/sh", "-c", instruction],
            privileged=True,
            stream=True,
            demux=True,
            workdir=PIPELINE_MOUNT_TARGET
        )
        return response.output

    def teardown(self, container: Container):
        """
        Tears the container down stopping it forcibly and removing it

        :param container: Container to remove
        :return: No Return Value
        """
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
                    'bind': PIPELINE_MOUNT_TARGET,
                    'mode': 'rw'
                }
            }
        )


@Service(name="run_service")
class RunService:

    def __init__(self, docker_service=Autowired("docker_service")):
        self._docker_service: DockerService = docker_service

    def start(self, run: RunTask, workspace_path: str):
        LOGGER.info("Executing Run uuid %s" % run.uuid)
        try:
            run.start()
            for step in run.get_steps():
                try:
                    LOGGER.info("Setting up step %s" % step.name)
                    run.start_step(step.number)
                    container = None
                    try:
                        container = self._docker_service.provision(run.uuid, step.image, workspace_path)
                        LOGGER.info("Running commands for step %s" % step.name)
                        for command in step.commands:
                            LOGGER.info("Running command %s" % command.instruction)
                            output = self._docker_service.run_command(container, command.instruction)
                            while True:
                                try:
                                    std_out, std_err = next(output)
                                    if std_out:
                                        run.add_output(step.number, command.number, std_out.decode())
                                    if std_err:
                                        run.add_error(step.number, command.number, std_err.decode())
                                        raise StdErrException("Execution stopped due to command receiving stdErr")
                                except StopIteration:
                                    break
                    except Exception as e:
                        LOGGER.error(
                            "Exception caught during step, marking as failed, set to Debug for the full stacktrace")
                        LOGGER.debug(e)
                        run.fail_step(step.number)
                    finally:
                        self._docker_service.teardown(container)

                    if run.step_is_failed(step.number):
                        raise StepException("Step aborted due to Failed Step Status")

                    run.complete_step(step.number)
                except Exception as e:
                    LOGGER.error(
                        "Error occurred in Step #%s - %s, failing run, set to Debug for the full stacktrace" % (
                            step.number, step.name))
                    LOGGER.debug(e)
                    run.fail()
                    break

            if run.is_failed():
                raise RunException("Run aborted due to Failed Run Status")

            run.complete()
        except RunException:
            LOGGER.error("Run Failed, aborting remaining Steps")
            run.abort_pending_steps()
        LOGGER.info("Completed Executing the run %s" % run.uuid)


@Service(name="job_service")
class JobService:

    def __init__(self, run_service=Autowired("run_service"), docker_service=Autowired("docker_service")):
        self.run_service = run_service
        self.docker_service = docker_service
        LOGGER.info("System Pipeline Base set to %s" % working_dir)

    def process_request(self, job: Job) -> str:
        """
        Starts a new Run of the given job.

        :param job: Job Object to start the run for
        :return: UUID of the run
        """
        LOGGER.info("Processing Request %s" % job._name)
        run = RunTask(job)
        t = threading.Thread(target=self._run, args=(run,))
        t.start()
        return run.uuid

    def _run(self, run: RunTask):
        workspace_path: str = JobService._get_workspace_path()
        JobService._clone_repo(run.get_run().job.url, workspace_path)
        LOGGER.debug("Cloned Repo into Workspace %s" % workspace_path)
        run.configure_from_yml_file("%s/%s" % (workspace_path, PIPELINE_YML_NAME))
        LOGGER.info("Starting a new run thread for uuid %s" % run.uuid)
        self.run_service.start(run, workspace_path)
        shutil.rmtree(workspace_path)
        LOGGER.info("Finishing run thread for uuid %s" % run.uuid)

    @staticmethod
    def _get_workspace_path() -> str:
        return "%s/%s/%s" % (
            get_working_dir(),
            PROJECTS_FOLDER,
            new_string_id()
        )

    @staticmethod
    def _clone_repo(url: str, workspace_path: str) -> Repo:
        if os.path.exists(workspace_path): shutil.rmtree(workspace_path)
        return Repo.clone_from(url, workspace_path)
