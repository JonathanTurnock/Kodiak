import re

from fxq.ae.runner.model import GitRepository


class GitUrlMarshaller:
    HTTP_GIT_URL_REGEX = "https{0,1}://(.*?)/(.*?)/(.*?)\.git"

    SSH_GIT_URL_REGEX = "(.*?):(.*?)/(.*?)\.git"

    @staticmethod
    def marshall_url(url: str) -> GitRepository:
        if re.match(GitUrlMarshaller.HTTP_GIT_URL_REGEX, url) is not None:
            return GitUrlMarshaller._marshal_http_url(url)
        elif re.match(GitUrlMarshaller.SSH_GIT_URL_REGEX, url) is not None:
            return GitUrlMarshaller._marshal_ssh_url(url)
        else:
            raise RuntimeError("Failed to match the URL to an accepted format")

    @staticmethod
    def _marshal_ssh_url(url: str):
        m = re.match(GitUrlMarshaller.SSH_GIT_URL_REGEX, url)

        if "@" in m.group(1):
            site = m.group(1).split("@")[1]
        else:
            site = m.group(1)

        url = url.replace(m.group(1), site)
        return GitRepository(url, site, m.group(2), m.group(3))

    @staticmethod
    def _marshal_http_url(url: str):
        m = re.match(GitUrlMarshaller.HTTP_GIT_URL_REGEX, url)

        if "@" in m.group(1):
            site = m.group(1).split("@")[1]
        else:
            site = m.group(1)

        url = url.replace(m.group(1), site)
        return GitRepository(url, site, m.group(2), m.group(3))
