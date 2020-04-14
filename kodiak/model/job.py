from kodiak.utils.id import new_string_id


class Job:
    def __init__(
            self,
            uuid: str = None,
            name: str = None,
            url: str = None
    ):
        self._uuid: str = uuid if uuid is not None else new_string_id()
        self._name: str = name
        self._url: str = url

    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url
