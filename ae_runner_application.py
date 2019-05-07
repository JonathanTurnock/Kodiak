from flask import Flask

app = Flask(__name__)

from repository import PipelineRepository
pipeline_repo = PipelineRepository()

from service import PipelineService
pipeline_service = PipelineService()

import controller.api

if __name__ == '__main__':
    app.run()
