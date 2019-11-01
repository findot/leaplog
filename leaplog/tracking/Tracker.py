# -*- coding: utf-8 -*-

import Leap
from time import time, sleep
from multiprocessing import Queue
from .Message import Message
from .data import Subject, Action, Frame, Hand, Finger, Bone


class Tracker(object):

    __slots__ = [ 'controller', 'commander', 'messenger', 'recording' ]

    def __init__(self, commander, messenger):
        # type: (Leap.Controller, Queue, Queue) -> Tracker
        self.controller = Leap.Controller()
        self.commander  = commander
        self.messenger  = messenger
        self.recording  = False

    def track(self, subject):
        # type: (Logger, Subject) -> None
        print('Awaiting Leap Motion device...')
        while not self.controller.is_connected:
            sleep(0.5)
        print('Device is connected.')
        
        action = None
        while True:
            try:
                order, payload = self.commander.get_nowait()
            except Queue.Empty:
                order = payload = None
            
            if order is None and self.recording:
                record = self.poll(action)
                self.messenger.put((Message.FRAME, record))

            elif order == Message.START:
                self.recording = True
                self.messenger.put((Message.START, subject))

            elif order == Message.NEXT:
                if self.recording:
                    self.messenger.put((Message.SAVE, action))
                action = Action(subject, payload, time())
                self.messenger.put((Message.START, action))
            
            elif order == Message.STOP:
                if self.recording:
                    self.messenger.put((Message.SAVE, action))
                self.messenger.put((Message.STOP, None))
                self.recording = False
                break

            elif order == Message.REMAKE and self.recording:
                self.messenger.put((Message.REMAKE, action))  

            else:
                raise RuntimeError('Unknown message {0}!'.format(order))  
        
        print('Terminating recording')

    def poll(self, action):
        # type: (Action) -> (Frame, [Hand])
        whence = time() - action.record_time
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
