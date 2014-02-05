

def emit(event, values):
    pass

class EventLoop(object):

    def __init__(self):
        self.registry = {}
        self.queue = []

    def register(self, event, callback):
        if event not in self.registry:
            self.registry[event] = []
        self.registry[event].append(callback)

    def run(self):
        while True:
            event, value = self.queue.pop()
            if event not in self.registry:
                print("Invalid event encountered %s with values %r!" %
                      (event, value))
                continue
            for listener in self.registry[event]:
                listener(event, value)
