import logging

LOGGER = logging.getLogger(__name__)


class Command:
    def __init__(self, instruction: str):
        self.instruction = instruction
        self.output = []

    def append_output(self, output):
        self.output.append(output)
        LOGGER.debug("CALLBACK:%s" % self)

    def __repr__(self):
        return str({
            'instruction': self.instruction,
            'output': self.output
        })
