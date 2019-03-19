import numpy as np
import heapq
import collections

# EVENT TYPES
ARRIVAL = 0
DEPARTURE = 1

def create_event(event_time, event_type, extra_data=None):
    return (event_time, event_type, extra_data)

# samplers for times

def sample_interrival_times():
    return np.random.exponential(12)

def sample_service_times():
    return np.random.exponential(8)

class Customer(object):
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.service_finish_time = None
        self.departure_time = None
        self.service_time = service_time
        self.server = None

    def start_serving(self, clock, server):
        self.service_start_time = clock
        self.server = server

    def finish_serving(self, clock):
        self.service_finish_time = clock

    def initiate_departure(self, clock):
        self.departure_time = clock

    def W(self):
        return self.departure_time - self.arrival_time

    def Wq(self):
        return self.service_start_time - self.arrival_time

class Server(object):
    def __init__(self):
        self.free = True
        self.curr_customer = None
        self.time_active = 0

    def start_serving(self, clock, customer):
        self.curr_customer = customer
        customer.start_serving(clock, self)
        self.free = False

    def finish_serving(self, clock):
        self.curr_customer.finish_serving(clock)
        self.time_active += self.curr_customer.service_time
        self.free = True

    def is_free(self):
        return self.free

    def utilization(self, clock):
        return self.time_active / clock

class ServerList(object):
    def __init__(self, num_servers):
        self.servers = [Server() for _ in range(num_servers)]

    def get_free_server(self):
        free_server = None
        for server in self.servers:
            if server.is_free():
                return server
        return free_server

    def average_utilization(self, clock):
        utilizations = [server.utilization(clock) for server in self.servers]
        return np.mean(utilizations)

class StateMonitor(object):
    def __init__(self, initial_value=0):
        self.values = [initial_value]
        self.times = [0]
        self.probs_calculated = False
        self.table= {}

    def append(self, time, values):
        self.times.append(time)
        self.values.append(values)

    def compute_probs(self):
        if not self.probs_calculated:
            self.times = np.array(self.times)
            self.values = np.array(self.values)
            self.table = collections.defaultdict(float)
            diffs = self.times[1:] - self.times[0:-1]
            total_time = np.sum(diffs)
            for v, d in zip(self.values, diffs):
                self.table[v] += (d / total_time)
            self.probs_calculated = True

    def get_table(self):
        return self.table

    def __getitem__(self, item):
        return self.table[item]

    def mean(self):
        if not self.probs_calculated:
            self.compute_probs()
        mean_value = 0
        for k, v in self.table.items():
            mean_value += (k * v)
        return mean_value


def simulate_k_server_queue(k, time_to_simulate):
    clock = 0
    event_list = []
    num_in_queue = 0
    num_in_system = 0
    L = StateMonitor()
    Lq = StateMonitor()
    servers = ServerList(k)
    waiting_customers = []
    served_customers = []
    time_of_first_arrival = sample_interrival_times()
    first_arrival_event = create_event(time_of_first_arrival, ARRIVAL)
    heapq.heappush(event_list, first_arrival_event)
    while clock < time_to_simulate:
        curr_event = heapq.heappop(event_list)
        clock = curr_event[0]
        event_type = curr_event[1]
        extra_data = curr_event[2]
        if event_type == ARRIVAL:
            service_time = sample_service_times()
            new_customer = Customer(clock, service_time)
            waiting_customers.append(new_customer)
            free_server = servers.get_free_server()
            num_in_queue += 1
            num_in_system += 1

            next_arrival_time = clock + sample_interrival_times()
            arrival_event = create_event(next_arrival_time, ARRIVAL)
            heapq.heappush(event_list, arrival_event)

            if free_server is not None:
                customer = waiting_customers.pop(0)
                free_server.start_serving(clock, customer)
                num_in_queue -= 1
                departure_time = clock + customer.service_time
                departure_event = create_event(departure_time, DEPARTURE, {'customer': customer, 'server': free_server})
                heapq.heappush(event_list, departure_event)
        elif event_type == DEPARTURE:
            customer = extra_data['customer']
            server = extra_data['server']
            server.finish_serving(clock)
            num_in_system -= 1
            customer.initiate_departure(clock)
            served_customers.append(customer)
            if num_in_queue > 0:
                free_server = servers.get_free_server()
                customer = waiting_customers.pop(0)
                free_server.start_serving(clock, customer)
                num_in_queue -= 1
                departure_time = clock + customer.service_time
                departure_event = create_event(departure_time, DEPARTURE, {'customer': customer, 'server': free_server})
                heapq.heappush(event_list, departure_event)
        L.append(clock, num_in_system)
        Lq.append(clock, num_in_queue)

    print('Average utlilization: ', servers.average_utilization(clock))
    print('L: ', L.mean())
    print('Lq: ', Lq.mean())
    print('Pn: ', L.table)

    average_W = np.mean([cust.W() for cust in served_customers])
    average_Wq = np.mean([cust.Wq() for cust in served_customers])

    print('W: ', average_W)
    print('Wq: ', average_Wq)

simulate_k_server_queue(10, 10000)







