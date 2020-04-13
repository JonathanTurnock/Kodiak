from typing import Dict


class Health():
    def __init__(self, status: str, details: Dict = None):
        self.status = status
        self.details = details

    def to_dict(self):
        resp = {
            'status': self.status
        }

        if self.details:
            resp["details"] = self.details

        return resp
