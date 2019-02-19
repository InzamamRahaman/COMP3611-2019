import numpy as np

from FutureEventList import FutureEventList
from Customer import Customer
from Server import Server
from QueueEvents import QueueEvents, ARRIVAL, DEPARTURE
from Monitor import Monitor


def sample_interrival_time():
    return np.random.uniform(1, 10)

def sample_service_time():
    return np.random.uniform(1, 3)

MAX_TIME_TO_SIMULATE = 24 * 60
event_list = FutureEventList()
first_arrival_time = sample_interrival_time()
current_time = 0
next_arrival = current_time + first_arrival_time
first_arrival = QueueEvents(first_arrival_time, ARRIVAL)
event_list.enqueue(first_arrival)
first_service_time = sample_service_time()
customers = []
curr_customer = 0
num_in_queue = 0
num_in_system = 0
server = Server()
monitor = Monitor()

while current_time < MAX_TIME_TO_SIMULATE:
    next_event = event_list.dequeue()
    if next_event.event_type == ARRIVAL:
        num_in_queue += 1
        next_arrival_time = current_time + first_arrival_time
        service_time = sample_service_time()
        new_customer = Customer(next_event.get_time(), service_time)
        customers.append(new_customer)
        next_arrival_event = QueueEvents(next_arrival_time, ARRIVAL)
        event_list.enqueue(next_arrival_event)
        if server.is_free():
            server.start_service(customers[curr_customer])








