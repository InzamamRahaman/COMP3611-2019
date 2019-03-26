import numpy as np
import heapq
import matplotlib.pylab as plt

R1 = 'Ride 1'
R2 = 'Ride 2'
SP = 'Swimming Pool'

TRANSITION_PROBS = {
    R1: {R1: 0.6, R2: 0.2, SP: 0.2},
    R2: {R1: 0.3, R2: 0.5, SP: 0.2},
    SP: {R1: 0.3, R2: 0.3, SP: 0.4}
}

AVG_SERVICE_TIMES = {
    R1: 10,
    R2: 5,
    SP: 20
}

CAPACITIES = {
    R1: 5,
    R2: 3,
    SP: -1,
}

def transition(current_state):
    distributions = TRANSITION_PROBS[current_state]
    probs = list(distributions.values())
    states = list(distributions.keys())
    next_state = np.random.choice(a=states, p=probs)
    return next_state

def get_service_time(current_state):
    return np.random.exponential(AVG_SERVICE_TIMES[current_state])


FROM_R1 = 0
FROM_R2 = 1
FROM_SP = 2

def create_event(event_time, event_type, event_data=None):
    return (event_time, event_type, event_data)

EVENT_TO_CURRENT_STATE = {
    FROM_R1: R1,
    FROM_R2: R2,
    FROM_SP: SP
}

NEXT_STATE_TO_EVENT = {
    R1: FROM_R1,
    R2: FROM_R2,
    SP: FROM_SP
}

class TimeInStateLogs(object):
    def __init__(self):
        self.data = {
            R1: [], R2: [], SP: []
        }

    def __getitem__(self, item):
        if item not in self.data:
            raise ValueError('No state named "', str(item), '"')
        return self.data[item]

    def __setitem__(self, key, value):
        if key not in self.data:
            raise ValueError('No state named "', str(key), '"')
        self.data[key].append(value)

    def append(self, key, value):
        self[key] = value

    def __sub__(self, other):
        r1a = np.array(self[R1])
        r2a = np.array(self[R2])
        spa = np.array(self[SP])

        r1b = np.array(other[R1])
        r2b = np.array(other[R2])
        spb = np.array(other[SP])

        r1 = r1a - r1b[:len(r1a)]
        r2 = r2a - r2b[:len(r2a)]
        r3 = spa - spb[:len(spa)]


        return {R1: r1, R2: r2 , SP: r3 }

class Customer(object):
    def __init__(self):
        self.arrival_times = TimeInStateLogs()
        self.service_times = TimeInStateLogs()
        self.time_of_service = TimeInStateLogs()
        self.end_of_service = TimeInStateLogs()
        self.current_state = None

    def arrive(self, state, clock):
        self.arrival_times.append(state, clock)
        self.current_state = state

    def service(self, state):
        time = get_service_time(state)
        self.service_times.append(state, time)
        return time

    def start_service(self, state, clock):
        self.time_of_service.append(state, clock)
        return self.service(state)

    def end_service(self, state, clock):
        self.end_of_service.append(state, clock)

    def get_waiting_times(self):
        waiting_times = self.time_of_service - self.arrival_times
        return waiting_times

    def get_average_waiting_times(self):
        waiting_times = self.get_waiting_times()
        d = {}
        for k,v in waiting_times.items():
            d[k] = np.mean(v) if len(v) else 0
        return d

class Server(object):
    def __init__(self, state):
        self.state = state
        self.current_customer = None
        self.time_active = 0.0
        self.free = True
        self.t = None

    def start_serving(self, customer, clock):
        self.current_customer = customer
        self.free = False
        time_of_dept = self.current_customer.start_service(self.state, clock)
        self.t = clock
        return time_of_dept

    def finish_serving(self, clock):
        customer = self.current_customer
        self.current_customer = None
        self.free = True
        self.time_active += (clock - self.t)
        self.t = None
        return customer

    def is_free(self):
        return self.free

    def get_utilization(self, clock):
        return self.time_active / clock

class ServerList(object):
    def __init__(self, k, state):
        self.servers = [Server(state) for _ in range(k)]
        self.state = state

    def get_free_server(self):
        server = False
        for s in self.servers:
            if s.is_free():
                server = s
        return server

    def get_average_utilization(self, clock):
        utilizations = [server.get_utilization(clock) for server in self.servers]
        return np.mean(utilizations)


num_customers = 100
customers = [Customer() for _ in range(num_customers)]

clock = 0
event_list = []
for cust in customers:
    cust.arrive(SP, clock)
    time_of_dept = cust.start_service(SP, clock)
    dept_event = create_event(time_of_dept, FROM_SP, {'customer': cust})
    heapq.heappush(event_list, dept_event)

waiting_lines = {R1: [], R2: []}
server_lists = {R1: ServerList(CAPACITIES[R1], R1), R2: ServerList(CAPACITIES[R2], R2)}

while clock < (8 * 60):
    event = heapq.heappop(event_list)
    clock = event[0]
    event_type = event[1]
    event_data = event[2]
    customer = event_data['customer']
    if event_type == FROM_SP:
        next_state = transition(SP)
        customer.end_service(SP, clock)
        if next_state == SP:
            customer.arrive(SP, clock)
            time_of_dept = customer.start_service(SP, clock)
            new_event = create_event(clock + time_of_dept, FROM_SP, {'customer': customer})
            heapq.heappush(event_list, new_event)
        else:
            customer.arrive(next_state, clock)
            next_event_type = NEXT_STATE_TO_EVENT[next_state]
            sl = server_lists[next_state]
            free_server = sl.get_free_server()
            if free_server:
                next_event_time = free_server.start_serving(customer, clock)
                new_event = create_event(next_event_time + clock, next_event_type,
                                         {'customer': customer, 'server': free_server})
                heapq.heappush(event_list, new_event)
            else:
                waiting_line = waiting_lines[next_state]
                waiting_line.append(customer)
    elif event_type == FROM_R1:
        server = event_data['server']
        server.finish_serving(clock)
        waiting_line = waiting_lines[R1]

        if waiting_line:
            new_customer = waiting_line.pop(0)
            service_time = server.start_serving(new_customer, clock)
            departure_time = clock + service_time
            departure_event = create_event(departure_time, FROM_R1, {'customer': new_customer, 'server': server})
            heapq.heappush(event_list, departure_event)
        next_state = transition(R1)
        customer.end_service(R1, clock)
        if next_state == SP:
            customer.arrive(SP, clock)
            time_of_dept = customer.start_service(SP, clock)
            new_event = create_event(clock + time_of_dept, FROM_SP, {'customer': customer})
            heapq.heappush(event_list, new_event)
        else:
            customer.arrive(next_state, clock)
            next_event_type = NEXT_STATE_TO_EVENT[next_state]
            sl = server_lists[next_state]
            free_server = sl.get_free_server()
            if free_server:
                next_event_time = free_server.start_serving(customer, clock)
                new_event = create_event(next_event_time + clock, next_event_type,
                                         {'customer': customer, 'server': free_server})
                heapq.heappush(event_list, new_event)
            else:
                waiting_line = waiting_lines[next_state]
                waiting_line.append(customer)
    elif event_type == FROM_R2:
        server = event_data['server']
        server.finish_serving(clock)
        waiting_line = waiting_lines[R2]

        if waiting_line:
            new_customer = waiting_line.pop(0)
            service_time = server.start_serving(new_customer, clock)
            departure_time = clock + service_time
            departure_event = create_event(departure_time, FROM_R2, {'customer': new_customer, 'server': server})
            heapq.heappush(event_list, departure_event)
        next_state = transition(R2)
        customer.end_service(R2, clock)
        if next_state == SP:
            customer.arrive(SP, clock)
            time_of_dept = customer.start_service(SP, clock)
            new_event = create_event(clock + time_of_dept, FROM_SP, {'customer': customer})
            heapq.heappush(event_list, new_event)
        else:
            customer.arrive(next_state, clock)
            next_event_type = NEXT_STATE_TO_EVENT[next_state]
            sl = server_lists[next_state]
            free_server = sl.get_free_server()
            if free_server:
                next_event_time = free_server.start_serving(customer, clock)
                new_event = create_event(next_event_time + clock, next_event_type,
                                         {'customer': customer, 'server': free_server})
                heapq.heappush(event_list, new_event)
            else:
                waiting_line = waiting_lines[next_state]
                waiting_line.append(customer)


times_r1 = []
times_r2 = []
times_sp = []


for cust in customers:
    w = cust.get_average_waiting_times()
    times_r1.append(w[R1])
    times_r2.append(w[R2])
    times_sp.append(w[SP])

# plt.hist(times_r1)
# plt.hist(times_r1)
# plt.hist(times_sp)
# plt.show()


print(np.mean(times_r1))
print(np.mean(times_r2))
print(np.mean(times_sp))






