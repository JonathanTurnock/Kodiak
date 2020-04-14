from fxq.core.beans.factory.annotation import Autowired

from kodiak.agent._services import JobService
from kodiak.agent._tasks import RunTask
from kodiak.model.job import Job


class AgentInterface:
    """
    Interface to the agent package, this can be used to schedule a new Job to be run via the agent.
    """

    _job_service: JobService = Autowired("job_service")

    @staticmethod
    def run_job(uuid: str, name: str, url: str):
        """
        Schedules a new Run of a job based off the job information provided.
        :param uuid: uuid of the Job for the callback functionality to map correctly
        :param name: Name of the Job
        :param url: url for the job
        :return: UUID of the Run which can be used to query status
        """
        job = Job(uuid, name, url)
        run_task_uuid = AgentInterface._job_service.process_request(job)
        return run_task_uuid
