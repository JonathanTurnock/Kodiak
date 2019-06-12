from flask import Flask, request, jsonify
from fxq.core.beans.factory.annotation import Autowired

from fxq.ae.runner.model import Request
from fxq.ae.runner.service import RequestService

app = Flask(__name__)

request_service = Autowired(type=RequestService)


@app.route('/api/request', methods=['POST'])
def start():
    return jsonify(
        request_service.process_request(
            Request.of_url(request.json["url"])
        ).__json__()
    )
