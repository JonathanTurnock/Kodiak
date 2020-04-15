import os
from pathlib import Path

from fxq.env import Environment

active_profiles = os.getenv("FXQ_ACTIVE_PROFILES").split(",") if os.getenv("FXQ_ACTIVE_PROFILES") else []
env: Environment = Environment(active_profiles)

web_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'web').absolute())
resources_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'resources').absolute())
