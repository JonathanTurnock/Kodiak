import logging

from kodiak.server.papi._sqlite.connection_factory import get_connection
from kodiak.server.papi._sqlite.schema.model import SchemaQueryException, ChangeSet

LOGGER = logging.getLogger(__name__)


class SchemaDao:
    _INSERT_NEW_VERSION = "insert into changelog (version, author, comment) values (?, ?, ?)"
    _GET_CURRENT_VERSION = "select version from changelog order by id desc limit 1"

    @staticmethod
    def get_current_version():
        """
        Gets the current schema version, if schema is not initialized returns 0.0.0

        :return: Current schema version
        """
        _connection = get_connection()
        try:
            cur = _connection.execute(SchemaDao._GET_CURRENT_VERSION)
            return cur.fetchone()[0]
        except Exception as e:
            if str(e) in ("no such table: changelog", "'NoneType' object is not subscriptable"):
                return "0.0.0"
            LOGGER.error("Failed to get current database version")
            raise SchemaQueryException("Exception was thrown while querying current changelog version")
        finally:
            _connection.close()

    @staticmethod
    def apply_changeset(changeset: ChangeSet):
        """
        Applies the given changeset to the database schema

        :param changeset: Changeset to Apply
        """
        LOGGER.info(f"Updating Database to version {changeset.version}")
        _connection = get_connection()
        try:
            LOGGER.debug(f"Applying Changeset Changes")
            [SchemaDao._apply_change(change.path) for change in changeset.changes]
            LOGGER.debug(f"Updating Changelog")
            SchemaDao._log_changeset_applied(changeset)
            LOGGER.info(f"Updated Database to version {changeset.version}")
        except Exception as e:
            SchemaDao.rollback_changeset(changeset)
        finally:
            _connection.close()

    def rollback_changeset(self, changeset: ChangeSet):
        """
        Runs the rollback for the given changeset

        :param changeset: Changeset to Rollback
        """
        LOGGER.error(f"Attempted to apply changeset {changeset.version} but failed, applying rollback")
        [self._apply_change(rollback.path) for rollback in changeset.rollback]
        LOGGER.info(f"Successfully applied rollback, current database version is {SchemaDao.get_current_version()}")

    @staticmethod
    def _apply_change(change_file):
        """
        Executes a Change File on the database

        :param sql_file: Path to the change file to apply
        """
        _connection = get_connection()
        try:
            with open(change_file, 'r') as sf:
                _connection.executescript(sf.read())
                _connection.commit()
        finally:
            _connection.close()

    @staticmethod
    def _log_changeset_applied(changeset: ChangeSet):
        """
        Logs that the changeset has been applied to the changelog

        :param changeset: Changeset to apply
        """
        _connection = get_connection()
        try:
            LOGGER.debug(f"Updating schema active version to {changeset.version}")
            _connection.execute(SchemaDao._INSERT_NEW_VERSION,
                                [changeset.version, changeset.author, changeset.comment])
            _connection.commit()
            _connection.close()
        finally:
            _connection.close()
