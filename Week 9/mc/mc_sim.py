import numpy as np 
import heapq

# "markov chain"
A = 'A'
B = 'B'
C = 'C'
TRANSITIONS = {
    A: {
        A: 0.4,
        B: 0.2,
        C: 0.4
    },
    B: {
        A: 0.1,
        B: 0.45,
        C: 0.45
    },

    C: {
        A: 0.4,
        B: 0.4,
        C: 0.2
    }
}

INITIAL_PROBS = {A: 0.5, B: 0.4, C:0.1}


def get_to(current_state):
    prob_dict = TRANSITIONS[current_state]
    next_states = list(prob_dict.keys())
    probs = list(prob_dict.values())
    next_state = np.random.choice(next_states, size=1, replace=False, p=probs)[0]
    return next_state

class Customer(object):
    def __init__(self):
        self.times = {
            A: 0,
            B: 0,
            C: 0
        }
        self.curr_state = np.random.choice(list(INITIAL_PROBS.keys()), p=list(INITIAL_PROBS.values()))[0]
        self.last_time = 0

    def transition(self, next_state, clock):
        self.times[self.curr_state] += clock - self.last_time
        self.last_time = clock
        self.curr_state = next_state

    def get_curr_state(self):
        return self.curr_state

    def get_current_time(self):
        return self.last_time

    def get_times(self, state=None):
        if state is None:
            return self.times
        return self.times[state]



# event types
FROM_A = 0
FROM_B = 1
FROM_C = 2

STATE_TO_EVENT = {
    A: FROM_A,
    B: FROM_B,
    C: FROM_C
}

def create_event(event_time, event_type, data_dict=None):
    if data_dict is None:
        data_dict = {}
    return (event_time, event_type, data_dict)



# times in states
AVG_TIMES = {
    A: 10,
    B: 15,
    C: 5
}


def get_time_in_state(current_state):
    avg_time = AVG_TIMES[current_state]
    draw = np.random.exponential(avg_time)
    return draw


NUM_CUSTOMERS = 1000
customers = [Customer() for _ in range(NUM_CUSTOMERS)]

clock = 0
event_list = []
MAX_SIM_TIME = 1000

for cust in customers:
    current_state = cust.get_curr_state()
    time_of_transition = get_time_in_state(current_state)
    #next_state = get_to(current_state)
    event_type = STATE_TO_EVENT[current_state]
    transition_event = create_event(time_of_transition, event_type, cust)
    heapq.heappush(event_list, transition_event)

while clock < MAX_SIM_TIME:
    curr_event = heapq.heappop(event_list)
    #print(curr_event)
    curr_time = curr_event[0]
    curr_state = curr_event[1]
    curr_cust = curr_event[2]
    clock = curr_time
    # NB not the most elegant way to implement this, but most explicit from
    # a mathematical perspective
    # Think about how the below code could have been better simplified!
    if curr_state == FROM_A:
        next_state = get_to(A)
        next_event_type = STATE_TO_EVENT[next_state]
        time_in_next = get_time_in_state(next_state)
        curr_cust.transition(next_state, clock)
        new_event = create_event(clock + time_in_next, next_event_type, curr_cust)
        heapq.heappush(event_list, new_event)
    elif curr_state == FROM_B:
        next_state = get_to(B)
        next_event_type = STATE_TO_EVENT[next_state]
        time_in_next = get_time_in_state(next_state)
        curr_cust.transition(next_state, clock)
        new_event = create_event(clock + time_in_next, next_event_type, curr_cust)
        heapq.heappush(event_list, new_event)
    elif curr_state == FROM_C:
        next_state = get_to(C)
        next_event_type = STATE_TO_EVENT[next_state]
        time_in_next = get_time_in_state(next_state)
        curr_cust.transition(next_state, clock)
        new_event = create_event(clock + time_in_next, next_event_type, curr_cust)
        heapq.heappush(event_list, new_event)

    #print(event_list)

times_in_a = [cust.get_times(A) for cust in customers]
times_in_b = [cust.get_times(B) for cust in customers]
times_in_c = [cust.get_times(C) for cust in customers]

print(np.mean(times_in_a))
print(np.mean(times_in_b))
print(np.mean(times_in_c))










