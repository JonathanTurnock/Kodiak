import uuid

class Pipeline(object):
    def __init__(self, url:str):
        self.id: uuid.UUID = uuid.uuid4()
        self.url: str = url

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url
        }

