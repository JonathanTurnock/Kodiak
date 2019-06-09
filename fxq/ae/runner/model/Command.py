import logging

LOGGER = logging.getLogger(__name__)


class Command:
    def __init__(self, instruction: str):
        self.instruction = instruction
        self.output = []

    def append_output(self, output):
        self.output.append(output)
        print("CALLBACK:%s" % self)

    def __repr__(self):
        return str(self.__json__())

    def __json__(self):
        return {
            'instruction': self.instruction,
            'output': [str(o) for o in self.output]
        }
