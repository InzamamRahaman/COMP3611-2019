import heapq

class FutureEventList(object):
    def __init__(self):
        self.contents = []

    def __len__(self):
        return len(self.contents)

    def enqueue(self, event):
        heapq.heappush(self.contents, event)

    def dequeue(self):
        return heapq.heappop(self.contents)

    def __bool__(self):
        return bool(self.contents)

    def __repr__(self):
        c = list(map(str, self.contents))
        return '\n'.join(c)

    def __str__(self):
        c = list(map(str, self.contents))
        return '\n'.join(c)



