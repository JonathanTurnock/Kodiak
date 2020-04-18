import logging
import os
import sys
from pathlib import Path

from kodiak.utils.env import get_override, has_override

LOGGER = logging.getLogger(__name__)


def get_working_dir() -> str:
    working_dirs = {
        "darwin": str(Path(Path.home(), ".kodiak").absolute()),
        "linux": str(Path(Path.home(), ".kodiak").absolute())
    }
    try:
        v = "PIPELINE_BASE"
        _pb = get_override(v) if has_override(v) else working_dirs[sys.platform]
        LOGGER.info(f"Using {_pb} as pipeline base")
        os.makedirs(_pb, exist_ok=True)
        return _pb
    except KeyError:
        raise Exception(
            f"Unsupported operating system, supported systems are {[k for k in working_dirs.keys()]}, define envar KODIAK_HOME to continue...") from None


def get_database_path() -> str:
    _dbp = Path(working_dir, "kodiak.db")
    os.makedirs(_dbp.parent, exist_ok=True)
    return str(_dbp.absolute())


working_dir = get_working_dir()
database_path = get_database_path()
