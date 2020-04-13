class Job:
    def __init__(
            self,
            id: int = None,
            name: str = None,
            url: str = None
    ):
        self.id: int = id
        self.name: str = name
        self.url: str = url
