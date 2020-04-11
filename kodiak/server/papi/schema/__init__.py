import logging
from typing import List

import yaml

from kodiak.server.papi.schema.dao import SchemaDao
from kodiak.server.papi.schema.model import ChangeSet

LOGGER = logging.getLogger(__name__)


class SchemaInterface:
    def __init__(self, schema_dao: SchemaDao):
        self._available_changesets: List[ChangeSet] = SchemaInterface._get_available_changesets()
        self._schema_dao = schema_dao

    def check_for_updates(self):
        [self._schema_dao.apply_changeset(cs) for cs in self._available_changesets if
         cs.is_newer_than(self._get_current_version())]

    def _get_current_version(self):
        return self._schema_dao.get_current_version()

    @staticmethod
    def _get_available_changesets():
        versions = []
        with open('resources/db/ddl/changelog-master.yml', 'r') as f:
            master_changelog = yaml.load(f, Loader=yaml.FullLoader)

        for j in master_changelog["changelog"]:
            with open(j["include"]["file"], 'r') as f:
                changelog = yaml.load(f, Loader=yaml.FullLoader)

            for j in changelog["changelog"]:
                versions.append(ChangeSet.parse_yml(j["changeset"]))

        return versions
