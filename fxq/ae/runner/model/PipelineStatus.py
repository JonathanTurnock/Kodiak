from enum import Enum


class PipelineStatus(Enum):
    PENDING = 1
    SUCCESSFUL = 2
    FAILED = 3
    IN_PROGRESS = 4
    PAUSED = 5
    STOPPED = 6
