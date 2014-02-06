import Queue

class EventLoop(object):

    def __init__(self):
        self.registry = {}
        self.queue = Queue.Queue()

    def register(self, event, callback):
        if event not in self.registry:
            self.registry[event] = []
        self.registry[event].append(callback)

    def unregister(self, event, callback):
        self.registry[event].remove(callback)

    def add_event(self, event, value):
        print('add', event, value)
        self.queue.put((event, value))

    def run(self):
        while True:
            event, value = self.queue.get(True)
            if event not in self.registry:
                print("Invalid event encountered %s with values %r!" %
                      (event, value))
            for listener in self.registry[event]:
                print('call', listener, event, value)
                listener(event, value)

if __name__ == '__main__':
    from threading import Thread
    from time import sleep
    from random import random
    class Producer(Thread):
        def __init__(self, ev, i):
            self.ev = ev
            self.i = i
            super(Producer, self).__init__()

        def run(self):
            for i in range(20):
                self.ev.add_event(self.i, i)
                sleep(random())

    class Consumer(Thread):
        def __init__(self, i):
            self.i = i
            self.queue = Queue.Queue()
            super(Consumer, self).__init__()

        def add_event(self, event, value):
            self.queue.put((event, value))

        def run(self):
            for i in range(20):
                print(self.i, self.queue.get(True))

    e = EventLoop()

    prod1 = Producer(e, 'event1')
    prod2 = Producer(e, 'event1')
    prod3 = Producer(e, 'event2')

    cons1 = Consumer('c1')
    cons2 = Consumer('c2')
    cons3 = Consumer('c3')

    e.register('event1', cons1.add_event)
    e.register('event1', cons3.add_event)
    e.register('event2', cons2.add_event)

    cons1.start()
    cons2.start()
    cons3.start()

    prod1.start()
    prod2.start()
    prod3.start()

    e.run()
