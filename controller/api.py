from ae_runner_application import app, pipeline_service
from flask import jsonify, request, abort
from model import Pipeline
import http, logging
from typing import List

LOGGER = logging.getLogger("ApiController")

def error_400(error_message:str):
    return jsonify(error=error_message), http.HTTPStatus.BAD_REQUEST

def error_500():
    return jsonify(error="An error occured while processing the request"), http.HTTPStatus.INTERNAL_SERVER_ERROR

def created_201(pipeline: Pipeline):
    return jsonify(pipeline.serialize()), http.HTTPStatus.CREATED

def ok_200(pipelines: List[Pipeline]):
    serializedList = []
    for pipeline in pipelines:
        serializedList.append(pipeline.serialize())
    return jsonify(serializedList), http.HTTPStatus.OK

@app.route('/api/pipeline', methods= ['POST'])
def new_pipeline():
    if not request.json:
        return error_400('POST must be of type JSON')
    elif not 'url' in request.json:
        return error_400('POST must contain "url"')
    else:
        try:
            return created_201(pipeline_service.createPipeline(request.json["url"]))
        except Exception as e:
            LOGGER.error(e)
            return error_500()

@app.route('/api/pipeline', methods= ['GET'])
def get_pipelines():
    try:
        return ok_200(pipeline_service.getPipelines())
    except Exception as e:
        LOGGER.error(e)
        return error_500()