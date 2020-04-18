from http import HTTPStatus
from os import path
from pathlib import Path

from docker.errors import APIError
from flask import Flask, jsonify, send_from_directory, request
from flask_graphql import GraphQLView
from fxq.core.beans.factory.annotation import Autowired

from bootstrap import web_root
from kodiak.agent import AgentInterface
from kodiak.model.status import Health
from kodiak.server.gql import schema

app = Flask(__name__, root_path=web_root)

app.add_url_rule('/api/graphql',
                 view_func=GraphQLView.as_view('graphql', graphiql_version="0.17.5", schema=schema,
                                               graphiql=True))


# app.add_url_rule('/api/graphql/batch', view_func=GraphQLView.as_view('graphql', schema=schema, batch=True))


@app.route('/')
def index():
    return send_from_directory(web_root, 'index.html')


@app.route('/<file>')
def web(file):
    if path.exists(Path(web_root, file)):
        return send_from_directory(web_root, file)
    else:
        return index()


@app.route('/api/request', methods=['POST'])
def start():
    try:
        run_uuid = AgentInterface.run_job(str(request.json["uuid"]), str(request.json["name"]),
                                          str(request.json["url"]))
        return jsonify({"uuid": run_uuid})
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND


@app.route('/api/health', methods=['GET'])
def check_health():
    try:
        docker_service = Autowired("job_service")
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
