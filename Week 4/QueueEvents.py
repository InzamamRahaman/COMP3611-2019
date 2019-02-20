
from SimulationEvent import SimulationEvent

from enum import Enum


class QueueEventTypes(Enum):
    ARRIVAL = 0
    DEPARTURE = 1


ARRIVAL = QueueEventTypes.ARRIVAL
DEPARTURE = QueueEventTypes.DEPARTURE


class QueueEvents(SimulationEvent):

    def __init__(self, event_time, event_type):
        super().__init__(event_time)
        self.event_type = event_type

    def __repr__(self):
        return f'{self.event_type} @ {self.event_time}'