import logging
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict

from constants import PIPELINE_BASE

LOGGER = logging.getLogger(__name__)


class FetchOneException(Exception):
    pass


def get_connection():
    LOGGER.debug("Obtaining Database Connection")
    t0 = time.time()
    connection = sqlite3.connect(Path(PIPELINE_BASE, "kodiak.db").absolute())
    t1 = time.time()
    LOGGER.debug(f"Obtained Database Connection in {t1 - t0}")
    return connection


@contextmanager
def sql_fetch(query: str, params: List[any] or Dict, row_mapper, size=0):
    connection = get_connection()
    try:
        LOGGER.debug(f"Executing SQL Query:\nQUERY:{query}\nPARAMS: {params}")
        t0 = time.time()
        cursor = connection.execute(query, params)
        if size == 0:
            yield [row_mapper(row) for row in cursor.fetchall()]
        elif size == 1:
            row = cursor.fetchone()
            if row is None:
                raise FetchOneException("No Results Found!")
            yield row_mapper(row)
        elif size > 1:
            yield [row_mapper(row) for row in cursor.fetchmany(size=size)]
        t1 = time.time()
        LOGGER.debug(f"Executed Statement in {t1 - t0}")
    finally:
        LOGGER.debug("Closing Database Connection")
        connection.close()


@contextmanager
def sql_commit(statement: str, params: List[any] or Dict):
    connection = get_connection()
    try:
        LOGGER.debug(f"Executing SQL Statement:\nQUERY:{statement}\nPARAMS: {params}")
        t0 = time.time()
        cursor = connection.execute(statement, params)
        connection.commit()
        _id = cursor.lastrowid
        LOGGER.debug(f"Commit completed with id: {_id}")
        yield _id
        t1 = time.time()
        LOGGER.debug(f"Executed Statement in {t1 - t0}")

    finally:
        LOGGER.debug("Closing Database Connection")
        connection.close()
