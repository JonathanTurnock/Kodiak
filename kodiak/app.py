import docker
import requests
from flask import Flask, request, jsonify

from kodiak.agent.model.job import Job
from kodiak.agent.model.run import Run
from kodiak.agent.model.status import Health
from kodiak.bootstrap import job_service, docker_service

app = Flask(__name__)


@app.route('/api/request', methods=['POST'])
def start():
    job: Job = Job.of_dict(request.json)
    run: Run = job_service.process_request(job)
    return jsonify(
        run.to_dict()
    )


@app.route('/api/actuator/health', methods=['GET'])
def check_health():
    try:
        docker_service.list_containers()
        return jsonify(Health("UP").to_dict())
    except requests.exceptions.ConnectionError as e:
        return jsonify(
            Health("DOWN", {"error": "Docker ConnectionError, Check Docker Engine and Socket is up"}).to_dict())
    except docker.errors.APIError:
        return jsonify(Health("DOWN", {
            "error": "Docker APIError, Check Docker Engine is Running and API Socket is working"}).to_dict())
    except Exception as e:
        print(e.__class__)
        return jsonify(Health("DOWN", {"error": str(e)}).to_dict())
