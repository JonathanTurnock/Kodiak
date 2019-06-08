import tempfile

PIPELINE_BASE = "%s/fxquants-pipelines" % tempfile.gettempdir()
PIPELINE_MOUNT_TARGET = "/opt/fxquants/pipeline"
PROJECTS_FOLDER = "projects"
PIPELINE_YML_NAME = "fxq-pipeline.yml"
