import logging

from flask import Flask

from fxq.ae.runner.controller.ExecutorApiController import executor_api_controller
from fxq.ae.runner.controller.PipelineApiController import pipeline_api_controller

logging.basicConfig(format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s", level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(executor_api_controller, url_prefix='/')
app.register_blueprint(pipeline_api_controller, url_prefix="/")

for rule in app.url_map.iter_rules():
    LOGGER.info("Methods: %s Endpoint: %s Path:%s" % (rule.methods, rule.endpoint, rule))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
