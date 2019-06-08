import re

from fxq.core.stereotype import Component

from fxq.ae.runner.model import GitRepository


@Component
class GitUrlMarshaller:
    HTTP_GIT_URL_REGEX = "https{0,1}://(.*?)/(.*?)/(.*?)\.git"

    SSH_GIT_URL_REGEX = "(.*?):(.*?)/(.*?)\.git"

    def marshall_url(self, url: str) -> GitRepository:
        if re.match(GitUrlMarshaller.HTTP_GIT_URL_REGEX, url) is not None:
            return self._marshal_http_url(url)
        elif re.match(GitUrlMarshaller.SSH_GIT_URL_REGEX, url) is not None:
            return self._marshal_ssh_url(url)
        else:
            raise RuntimeError("Failed to match the URL to an accepted format")

    def _marshal_ssh_url(self, url: str):
        m = re.match(GitUrlMarshaller.SSH_GIT_URL_REGEX, url)

        if "@" in m.group(1):
            site = m.group(1).split("@")[1]
        else:
            site = m.group(1)

        url = url.replace(m.group(1), site)
        return GitRepository(url, site, m.group(2), m.group(3))

    def _marshal_http_url(self, url: str):
        m = re.match(GitUrlMarshaller.HTTP_GIT_URL_REGEX, url)

        if "@" in m.group(1):
            site = m.group(1).split("@")[1]
        else:
            site = m.group(1)

        url = url.replace(m.group(1), site)
        return GitRepository(url, site, m.group(2), m.group(3))
