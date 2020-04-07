import tempfile

PIPELINE_BASE = "%s/kodiak-pipelines" % tempfile.gettempdir()
PIPELINE_MOUNT_TARGET = "/opt/kodiak/pipeline"
PROJECTS_FOLDER = "projects"
PIPELINE_YML_NAME = "kodiak.yml"
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
JSON_HEADERS = {'content-type': 'application/json'}
URI_LIST_HEADERS = {'content-type': 'text/uri-list'}
