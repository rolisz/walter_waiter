import Queue
from threading import Thread, Event
from time import sleep


class EventLoop(object):


    def __init__(self):
        self.registry = {}
        self.threads = {}
        self.queue = Queue.Queue()
        self.run_flag = Event()
        self.run_flag.set()


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
            if self.threads[name].add_event not in self.registry[event]:
                self.registry[event].append(self.threads[name].add_event)


    def unregister(self, event, name):
        ev_thr = self.threads[name].add_event
        print('unregister', event, name, ev_thr, self.registry[event])
        if ev_thr in self.registry[event]:
            self.registry[event].remove(ev_thr)
            print(self.registry[event])


    def add_event(self, event, value):
        self.queue.put((event, value))


    def run(self):
        for name in self.threads:
            self.threads[name].start()
        while True:
            try:
                event, value = self.queue.get(True, 20)
                if event == 'unregister':
                    self.unregister(*value)
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

    def __init__(self, ev):
        self.ev = ev
        self.run_flag = ev.run_flag
        super(EventEmitter, self).__init__()

    def emit(self, event, values=None):
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
        event = None
        value = None
        while True:
            try:
                event, value = self.queue.get(False)
            except Queue.Empty:
                #try:
                #    if event is not None:
                #        self.queue.put((event, value))
                #except AttributeError:
                #    print("Unfound attribute %s" % event)
                break

    def run(self):
        while self.run_flag.is_set():
            try:
                event, value = self.queue.get(True, 2)
                getattr(self, event)(value)
            except Queue.Empty:
                pass

class DecisionMaker(EventEmitter, EventConsumer):

    def __init__(self, ev):
        EventEmitter.__init__(self, ev)
        EventConsumer.__init__(self)


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
        def __init__(self, ev, i):
            self.i = i
            self.ev = ev
            super(Consumer, self).__init__(ev.run_flag)

        def event1(self, value):
            print('event1', value, self.i)

        def event2(self, value):
            print('event2', value, self.i)
            if value == 10:
                self.ev.unregister('event1', 'c3')
                # self.ev.add_event('unregister', ('event1', 'c3'))

    e = EventLoop()

    e.register("p1", Producer(e, 'event1'))
    e.register("p2", Producer(e, 'event1'))
    e.register("p3", Producer(e, 'event2'))

    e.register('c1', Consumer(e, 'c1'), 'event1')
    e.register('c2', Consumer(e, 'c2'), 'event2')
    e.register('c3', Consumer(e, 'c3'), 'event1')


    e.run()

if __name__ == '__main__':
    main()
