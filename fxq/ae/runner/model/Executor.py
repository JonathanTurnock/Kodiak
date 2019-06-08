class Executor:
    def __init__(self, id: int, url: str, owner: str, repo: str, remove: bool = True):
        self.id: int = id
        self.owner: str = owner
        self.repo: str = repo
        self.url: str = url
        self.remove: bool = remove
