# -*- coding: utf-8 -*-

class Box(object):

    __slots__ = ['frame']
    def __init__(self, frame):
        self.frame = frame


import Leap

from multiprocessing import Process, Queue
from time import time, sleep
from .Tracker import Tracker
from .data import *

def produce(queue):
    c = Leap.Controller()
    while not c.is_connected:
        print('Awaiting Leap Motion device connection')
        sleep(0.5)

    i = 0
    while (i < 1000):
        queue.put(Box(c.frame()))    
        i += 1

    queue.put(False)

def consume(queue):
    Entity.bootstrap('data.db')
    # Get subject and action
    s = Subject('Florian', 'Indot')
    a = Action(s, 1, time())
    tracker = Tracker(a)
    
    msg = None
    while msg is not False:
        msg = queue.get()
        if msg is None:
            break
        tracker.track(msg.frame)

    queue.put(None)

def main():
    queue = Queue()
    consumer = Process(target=consume, args=(queue,))
    consumer.start()
    produce(queue)

if __name__ == '__main__':
    main()
