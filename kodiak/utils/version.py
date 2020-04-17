from packaging import version


def is_later_version(new_version, current_version):
    """
    Checks if the provided Semantic version is a later version than the current version.

    :param new_version: New Version in SemanticVer format
    :param current_version: Current Version in SemanticVer format
    :return: Returns True if the version is later, otherwise returns False
    """
    return version.parse(new_version) > version.parse(current_version)


def is_same_or_later_version(new_version, current_version):
    """
    Checks if the provided Semantic version is the same or a later version than the current version.

    :param new_version: New Version in SemanticVer format
    :param current_version: Current Version in SemanticVer format
    :return: Returns True if the version is same or later, otherwise returns False
    """
    return version.parse(new_version) >= version.parse(current_version)
