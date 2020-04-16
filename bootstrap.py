import logging
import os
from pathlib import Path

from fxq.env import Environment

LOGGER = logging.getLogger(__name__)

PIPELINE_MOUNT_TARGET = "/opt/kodiak/pipeline"
PROJECTS_FOLDER = "projects"
PIPELINE_YML_NAME = "kodiak.yml"
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
JSON_HEADERS = {'content-type': 'application/json'}
URI_LIST_HEADERS = {'content-type': 'text/uri-list'}

active_profiles = os.getenv("FXQ_ACTIVE_PROFILES").split(",") if os.getenv("FXQ_ACTIVE_PROFILES") else []
env: Environment = Environment(active_profiles)

web_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'web').absolute())
resources_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'resources').absolute())
