class GitRepository:
    def __init__(self, url: str, site: str, maintainer: str, repo: str):
        self.url = url
        self.site = site
        self.maintainer = maintainer
        self.repo = repo
