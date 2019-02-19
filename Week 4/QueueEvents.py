
from SimulationEvent import SimulationEvent

from enum import Enum




class QueueEventTypes(Enum):
    ARRIVAL = 0
    DEPARTURE = 0


ARRIVAL = QueueEventTypes.ARRIVAL
DEPARTURE = QueueEventTypes.DEPARTURE


class QueueEvents(SimulationEvent):

    def __init__(self, event_time, event_type):
        super().__init__(event_time)
        self.event_type = event_type
