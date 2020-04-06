from kodiak.agent.service.consul import ConsulService
from kodiak.agent.service.docker import DockerService
from kodiak.agent.service.job import JobService
from kodiak.agent.service.run import RunService

consul_service = ConsulService()
docker_service = DockerService()
run_service = RunService(docker_service)
job_service = JobService(run_service, docker_service)
