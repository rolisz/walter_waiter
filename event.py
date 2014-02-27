import Queue
from threading import Thread, Event
from time import sleep


class EventLoop(object):

    @profile
    def __init__(self):
        self.registry = {}
        self.threads = {}
        self.queue = Queue.Queue()
        self.run_flag = Event()
        self.run_flag.set()

    @profile
    def register(self, name, thread_obj=None, event=None):
        """
        If called with two parameters, they should be event to listen to and
        the EventConsumer class that will listen to it.
        If called with one parameter, it should be an EventEmitter class.
        """
        if thread_obj is not None:
            self.threads[name] = thread_obj
        if event is not None:
            if event not in self.registry:
                self.registry[event] = []
            self.registry[event].append(self.threads[name].add_event)

    @profile
    def unregister(self, event, name):
        ev_thr = self.threads[name].add_event
        if ev_thr in self.registry[event]:
            self.registry[event].remove(ev_thr)

    @profile
    def add_event(self, event, value):
        self.queue.put((event, value))

    @profile
    def run(self):
        for name in self.threads:
            self.threads[name].start()
        while True:
            try:
                event, value = self.queue.get(True, 20)
                if event not in self.registry:
                    print("Invalid event encountered %s with values %r!" %
                          (event, value))
                for listener in self.registry[event]:
                    # print('call', listener, event, value)
                    listener(event, value)
            except KeyboardInterrupt:
                self.run_flag.clear()
                for thread in self.threads:
                    print(thread)
                    self.threads[thread].join()
                return
            except Queue.Empty:
                pass


class EventEmitter(Thread):
    @profile
    def __init__(self, ev):
        self.ev = ev
        self.run_flag = ev.run_flag
        super(EventEmitter, self).__init__()
    @profile
    def emit(self, event, values=None):
        self.ev.add_event(event, values)


class EventConsumer(Thread):
    @profile
    def __init__(self, flag=None):
        self.queue = Queue.Queue()
        if flag is not None:
            self.run_flag = flag
        super(EventConsumer, self).__init__()

    @profile
    def add_event(self, event, value):
        self.queue.put((event, value))

    @profile
    def sleep(self, time):
        sleep(time)
        event = None
        value = None
        while True:
            try:
                event, value = self.queue.get(False)
            except Queue.Empty:
                try:
                    if event is not None:
                        self.queue.put((event, value))
                except AttributeError:
                    print("Unfound attribute %s" % event)
                break
    @profile
    def run(self):
        while self.run_flag.is_set():
            try:
                event, value = self.queue.get(True, 2)
                getattr(self, event)(value)
            except Queue.Empty:
                pass

class DecisionMaker(EventEmitter, EventConsumer):
    @profile
    def __init__(self, ev):
        EventEmitter.__init__(self, ev)
        EventConsumer.__init__(self)

@profile
def main():
    from time import sleep
    from random import random

    class Producer(EventEmitter):
        def __init__(self, ev, i):
            self.i = i
            super(Producer, self).__init__(ev)

        def run(self):
            for i in range(20):
                if not self.run_flag.is_set():
                    break
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

    e.register("p1", Producer(e, 'event1'))
    e.register("p2", Producer(e, 'event1'))
    e.register("p3", Producer(e, 'event2'))

    e.register('c1', Consumer(e.run_flag, 'c1'), 'event1')
    e.register('c2', Consumer(e.run_flag, 'c2'), 'event2')
    e.register('c3', Consumer(e.run_flag, 'c3'), 'event1')

    e.run()

if __name__ == '__main__':
    main()
