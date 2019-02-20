class Customer(object):
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.service_start = -1
        self.service_finish = -1

    def start_serving(self, curr_time):
        self.service_start = curr_time

    def finish_serving(self, curr_time):
        self.service_finish = curr_time

