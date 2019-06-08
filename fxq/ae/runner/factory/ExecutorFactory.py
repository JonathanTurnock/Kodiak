from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Component

from fxq.ae.runner.marshaller import GitUrlMarshaller
from fxq.ae.runner.model import Executor


@Component
class ExecutorFactory:

    @Autowired
    def __init__(self, git_url_marshaller: GitUrlMarshaller):
        self.git_url_marshaller = git_url_marshaller

    def from_url(self, url: str):
        git_repo = self.git_url_marshaller.marshall_url(url)
        return Executor(
            id=None,
            url=git_repo.url,
            owner=git_repo.maintainer,
            repo=git_repo.repo
        )
