import logging
from typing import List

import yaml
from fxq.core.stereotype import Component

from kodiak.server.papi._sqlite.schema.dao import SchemaDao
from kodiak.server.papi._sqlite.schema.model import ChangeSet

LOGGER = logging.getLogger(__name__)


@Component(name="schema_interface")
class SchemaInterface:
    def __init__(self):
        self._available_changesets: List[ChangeSet] = self._get_available_changesets()

    def check_for_updates(self):
        [SchemaDao.apply_changeset(cs) for cs in self._available_changesets if
         cs.is_newer_than(SchemaInterface._get_current_version())]

    @staticmethod
    def _get_current_version():
        return SchemaDao.get_current_version()

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
