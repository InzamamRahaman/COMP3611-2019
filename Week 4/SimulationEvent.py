class SimulationEvent(object):
    def __init__(self, event_time):
        self.event_time = event_time

    def get_time(self):
        return self.event_time

    def __le__(self, other):
        return self.event_time <= other.event_time

    def __lt__(self, other):
        return self.event_time < other.event_time

    def __eq__(self, other):
        return self.event_time == other.event_time

    def __ne__(self, other):
        return self.event_time != other.event_time

    def __gt__(self, other):
        return self.event_time > other.event_time

    def __ge__(self, other):
        return self.event_time >= other.event_time