import sqlite3
from pathlib import Path

from constants import PIPELINE_BASE


def get_connection():
    return sqlite3.connect(Path(PIPELINE_BASE, "kodiak.db").absolute())
