# -*- coding: utf-8 -*-

import Leap
from time import time, sleep
from multiprocessing import Queue
from .Message import Message
from .data import Subject, Action, Frame, Hand, Finger, Bone


class Tracker(object):

    __slots__ = [ 'controller', 'commander', 'messenger', 'in_progress',
                  'subject', 'action', 'recording' ]

    def __init__(self, commander, messenger):
        # type: (Leap.Controller, Queue, Queue) -> Tracker
        self.controller = Leap.Controller()
        self.commander  = commander
        self.messenger  = messenger
        
        self.in_progress = False
        self.subject    = None
        
        self.action     = None
        self.recording = False

    @property
    def ready(self):
        self.controller.frame()
        return self.controller.is_connected

    def poll(self):
        if not self.recording:
            return self.commander.get()
        try:
            order, payload = self.commander.get_nowait()
        except:
            order = payload = None
        return order, payload

    def track(self):
        # type: (Logger, Subject) -> None
        if not self.ready:
            raise RuntimeError('Leap Motion device is not connected')
        
        print('Starting track')

        while True:
            order, payload = self.poll()
            
            if order is None and self.recording:
                record = self.leap_data()
                self.messenger.put((Message.FRAME, record))

            elif order == Message.START:
                if self.subject is None:
                    self.subject = payload
                    self.in_progress = True
                    self.messenger.put((Message.START, self.subject))
                elif self.action is None:
                    self.action = payload
                    self.recording = True
                    self.messenger.put((Message.START, self.action))
                else:
                    raise RuntimeError('Inconsistent message!')

            elif order == Message.NEXT:
                if self.recording:
                    raise RuntimeError('A recording is in progress!')
                self.messenger.put((Message.SAVE, self.action))
                self.action = payload
                self.messenger.put((Message.NEXT, action))

            elif order == Message.STOP:
                if not self.recording and not self.in_progress:
                    raise RuntimeError('No recording in progress!')
                if self.recording:
                    self.messenger.put((Message.STOP, self.action))
                    self.recording = False
                elif self.in_progress:
                    self.messenger.put((Message.STOP, self.subject))
                    self.in_progress = False
                    break

            elif order == Message.REMAKE:
                if self.recording:
                    raise RuntimeError('A recording is in progress!')
                self.messenger.put((Message.REMAKE, self.action))  

            else:
                raise RuntimeError('Unknown message {0}!'.format(order))  
        
        print('Terminating track')

    def leap_data(self):
        # type: (Action) -> (Frame, [Hand])
        whence = time() - self.action.record_time
        leap_frame = self.controller.frame()
        frame = Frame(action, whence)

        hands = []        
        for leap_hand in leap_frame.hands:
            hand = Hand(frame, leap_hand)
            fingers = []
            for leap_finger in leap_hand.fingers:
                finger = Finger(hand, leap_finger)
                leap_bones = [ leap_finger.bone(t.value) for t in Bone.Type ]
                bones = map(
                    lambda leap_bone: Bone(finger, leap_bone),
                    leap_bones
                )
                fingers.append((finger, bones))
            hands.append((hand, fingers))

        return frame, hands
