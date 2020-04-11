from typing import List

from kodiak.utils.version import is_later_version


class SchemaQueryException(Exception):
    pass


class Change:
    def __init__(self, path):
        self.path = path


class ChangeSet:
    def __init__(self, version, comment, author):
        self.version = version
        self.comment = comment
        self.author = author
        self.changes: List[Change] = []
        self.rollback: List[Change] = []

    def is_newer_than(self, version):
        return is_later_version(self.version, version)

    @staticmethod
    def parse_yml(yml: dict):
        """Factory Method which parses a changeset entry in the changelog and returns a changeset instance"""
        changeset = ChangeSet(yml["version"], yml["comment"], yml["author"])
        for change in yml["changes"]:
            changeset.changes.append(Change(change["sql_file"]["path"]))

        for rollback in yml["rollback"]:
            changeset.rollback.append(Change(rollback["sql_file"]["path"]))

        return changeset
