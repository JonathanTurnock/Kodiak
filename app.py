import os
from pathlib import Path

from docker.errors import APIError
from flask import Flask, request, jsonify, send_from_directory

from kodiak.agent.model.job import Job
from kodiak.agent.model.run import Run
from kodiak.agent.model.status import Health
from kodiak.agent.service.docker import DockerService
from kodiak.agent.service.job import JobService
from kodiak.agent.service.run import RunService

web_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'web').absolute())

docker_service = DockerService()
run_service = RunService(docker_service)
job_service = JobService(run_service, docker_service)

app = Flask(__name__, root_path=web_root)


@app.route('/')
def index():
    return send_from_directory(web_root, 'index.html')


@app.route('/<file>')
def web(file):
    return send_from_directory(web_root, file)


@app.route('/api/request', methods=['POST'])
def start():
    job: Job = Job.of_dict(request.json)
    run: Run = job_service.process_request(job)
    return jsonify(
        run.to_dict()
    )


@app.route('/api/health', methods=['GET'])
def check_health():
    try:
        docker_service.list_containers()
        return jsonify(Health("UP").to_dict())
    except ConnectionError as e:
        return jsonify(
            Health("DOWN", {"error": "Docker ConnectionError, Check Docker Engine and Socket is up"}).to_dict())
    except APIError:
        return jsonify(Health("DOWN", {
            "error": "Docker APIError, Check Docker Engine is Running and API Socket is working"}).to_dict())
    except Exception as e:
        print(e.__class__)
        return jsonify(Health("DOWN", {"error": str(e)}).to_dict())
