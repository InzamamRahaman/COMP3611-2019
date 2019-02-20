

class Server(object):
    def __init__(self):
        self.time_active = 0
        self.free = True
        self.current_customer = None

    def is_free(self):
        return self.free

    def compute_utilization(self, total_time):
        return self.time_active / float(total_time)

    def start_service(self, customer, curr_time):
        self.time_active += customer.service_time
        self.current_customer = customer
        customer.service_start = curr_time

    def finish_serve(self, curr_time):
        #print('Finish serving')
        #print(curr_time)
        #self.current_customer.service_end = curr_time
        self.free = True
        #self.current_customer = None
