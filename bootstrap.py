import os
from pathlib import Path

web_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'web').absolute())
resources_root = str(Path(os.path.abspath(os.path.dirname(__file__)), 'resources').absolute())
