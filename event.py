import Queue
from threading import Thread, Event
from time import sleep


class EventLoop(object):

    def __init__(self):
        self.registry = {}
        self.threads = set()
        self.queue = Queue.Queue()
        self.run_flag = Event()
        self.run_flag.set()

    def register(self, thread_obj, event=None):
        """
        If called with two parameters, they should be event to listen to and
        the EventConsumer class that will listen to it.
        If called with one parameter, it should be an EventEmitter class.
        """
        if event is not None:
            if event not in self.registry:
                self.registry[event] = []
            self.registry[event].append(thread_obj.add_event)
        self.threads.add(thread_obj)

    def unregister(self, event, callback):
        self.registry[event].remove(callback)

    def add_event(self, event, value):
        self.queue.put((event, value))

    def run(self):
        for thread in self.threads:
            thread.start()
        while True:
            try:
                event, value = self.queue.get(True, 20000)
                if event not in self.registry:
                    print("Invalid event encountered %s with values %r!" %
                          (event, value))
                for listener in self.registry[event]:
                    # print('call', listener, event, value)
                    listener(event, value)
            except KeyboardInterrupt:
                self.run_flag.clear()
                for thread in self.threads:
                    thread.join()


class EventEmitter(Thread):
    def __init__(self, ev):
        self.ev = ev
        self.run_flag = ev.run_flag
        super(EventEmitter, self).__init__()

    def emit(self, event, values):
        self.ev.add_event(event, values)


class EventConsumer(Thread):
    def __init__(self, flag=None):
        self.queue = Queue.Queue()
        if flag is not None:
            self.run_flag = flag
        super(EventConsumer, self).__init__()

    def add_event(self, event, value):
        self.queue.put((event, value))

    def sleep(self, time):
        sleep(time)
        while True:
            try:
                self.queue.get(False)
            except Empty:
                break

    def run(self):
        while self.run_flag.is_set():
            event, value = self.queue.get(True, 20000)
            getattr(self, event)(value)


class DecisionMaker(EventEmitter, EventConsumer):
    def __init__(self, ev):
        EventEmitter.__init__(self, ev)
        EventConsumer.__init__(self)

if __name__ == '__main__':
    from time import sleep
    from random import random

    class Producer(EventEmitter):
        def __init__(self, ev, i):
            self.i = i
            super(Producer, self).__init__(ev)

        def run(self):
            for i in range(20):
                self.emit(self.i, i)
                sleep(random())

    class Consumer(EventConsumer):
        def __init__(self, flag, i):
            self.i = i
            super(Consumer, self).__init__(flag)

        def event1(self, value):
            print('event1', value)

        def event2(self, value):
            print('event2', value)

    e = EventLoop()

    e.register(Producer(e, 'event1'))
    e.register(Producer(e, 'event1'))
    e.register(Producer(e, 'event2'))

    e.register(Consumer(e.run_flag, 'c1'), 'event1')
    e.register(Consumer(e.run_flag, 'c2'), 'event2')
    e.register(Consumer(e.run_flag, 'c3'), 'event1')

    e.run()
