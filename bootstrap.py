import os
from pathlib import Path

from kodiak.agent.service.docker import DockerService
from kodiak.agent.service.job import JobService
from kodiak.agent.service.run import RunService
from kodiak.server.papi.job.dao import JobDao
from kodiak.server.papi.schema import SchemaInterface, SchemaDao

web_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'web').absolute())
resources_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'resources').absolute())

docker_service = DockerService()
run_service = RunService(docker_service)
job_service = JobService(run_service, docker_service)
schema_dao: SchemaDao = SchemaDao()
schema_interface: SchemaInterface = SchemaInterface(schema_dao)
schema_interface.check_for_updates()
job_dao: JobDao = JobDao()
