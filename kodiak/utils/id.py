import uuid


def new_string_id():
    return str(uuid.uuid4()).replace("-", "")
