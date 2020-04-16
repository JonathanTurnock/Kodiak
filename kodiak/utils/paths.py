import logging
import os
import tempfile
from pathlib import Path

from kodiak.utils.env import get_override, has_override

LOGGER = logging.getLogger(__name__)


def get_pipeline_base() -> str:
    get_default = lambda: f"{tempfile.gettempdir()}/kodiak"
    v = "PIPELINE_BASE"
    _pb = get_override(v) if has_override(v) else get_default()
    LOGGER.info(f"Using {_pb} as pipeline base")
    os.makedirs(_pb, exist_ok=True)
    return _pb


def get_database_path() -> str:
    _dbp = Path(pipeline_base, "kodiak.db")
    os.makedirs(_dbp.parent, exist_ok=True)
    return str(_dbp.absolute())


pipeline_base = get_pipeline_base()
database_path = get_database_path()
