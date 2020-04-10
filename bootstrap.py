import os
import sqlite3
from pathlib import Path

from constants import PIPELINE_BASE
from kodiak.agent.service.docker import DockerService
from kodiak.agent.service.job import JobService
from kodiak.agent.service.run import RunService
from kodiak.server.schema.sqlite import v1

web_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'web').absolute())
resources_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'resources').absolute())

docker_service = DockerService()
run_service = RunService(docker_service)
job_service = JobService(run_service, docker_service)

kodiak_db = sqlite3.connect(Path(PIPELINE_BASE, "kodiak.db").absolute())
v1.setup(kodiak_db)
