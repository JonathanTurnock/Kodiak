import uuid

from fxq.ae.runner.marshaller import GitUrlMarshaller


class Request:
    def __init__(self, url: str, owner: str, repo: str, remove: bool = True):
        self.id: str = str(uuid.uuid4())
        self.owner: str = owner
        self.repo: str = repo
        self.url: str = url
        self.remove: bool = remove

    @staticmethod
    def of_url(url: str):
        git_repo = GitUrlMarshaller.marshall_url(url)
        return Request(
            url=git_repo.url,
            owner=git_repo.maintainer,
            repo=git_repo.repo
        )
