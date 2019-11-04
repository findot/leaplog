# -*- coding: utf-8 -*-

import Leap
from time import time, sleep
from os import getpid
from multiprocessing import Process, Queue
from .Message import Message
from .data import Subject, Action, Frame, Hand, Finger, Bone


class Tracker(Process):

    __slots__ = [ 'control', 'controller', 'commander', 'messenger',
                  'in_progress', 'subject', 'action', 'recording' ]

    def __init__(self, control, commander, messenger, logger):
        # type: (Leap.Controller, Queue, Queue) -> Tracker
        super(Tracker, self).__init__()

        self.control    = control
        self.commander  = commander
        self.messenger  = messenger

        self.in_progress = False
        self.subject    = None
        
        self.action     = None
        self.recording = False
        self.last_frame_id = 0

        self.logger = logger

    def poll(self):
        if not self.recording:
            return self.commander.get()
        try:
            order, payload = self.commander.get_nowait()
        except:
            order = payload = None
        return order, payload

    def run(self):
        # type: (Logger, Subject) -> None
        controller = Leap.Controller()
        self.logger.warn("TRACKER - Connecting to leap motion device...")
        while not controller.is_connected:
            if self.control.empty():
                self.control.put('Leap Motion Device is not ready')
            sleep(0.1)
        self.logger.warn('TRACKER - OK')

        self.logger.info('TRACKER - Starting track')
        while True:
            try:
                assert controller.is_connected
                order, payload = self.poll()
                
                if order == Message.TERMINATE:
                    self.logger.info('TRACKER - Terminating')
                    self.messenger.put((Message.TERMINATE, None))
                    return

                elif order is None and self.recording:
                    frame, hands = self.leap_data(controller)
                    if frame is None:
                        continue
                    self.messenger.put((Message.FRAME, (frame, hands)))

                elif order == Message.START:
                    if isinstance(payload, Subject):
                        self.subject = payload
                        self.in_progress = True
                        self.messenger.put((Message.START, self.subject))
                    elif isinstance(payload, Action):
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
                    if isinstance(payload, Action):
                        self.messenger.put((Message.STOP, self.action))
                        self.recording = False
                    elif isinstance(payload, Subject):
                        self.messenger.put((Message.STOP, self.subject))
                        self.in_progress = False
                        break

                elif order == Message.REMAKE:
                    if self.recording:
                        raise RuntimeError('A recording is in progress!')
                    self.messenger.put((Message.REMAKE, self.action))  

                elif order == Message.SAVE:
                    self.messenger.put((Message.SAVE, payload))

                else:
                    raise RuntimeError('Unknown message {0}!'.format(order))  
            
            except Exception as e:
                self.logger.warning('TRACKER - ' + str(e))
                self.control.put(e)

        self.logger.info('TRACKER - Terminating')

    def leap_data(self,controller):
        # type: (Action) -> (Frame, [Hand])
        whence = time() - self.action.record_time
        leap_frame = controller.frame()
        if leap_frame.id == self.last_frame_id:
            return None,None    
        self.last_frame_id = leap_frame.id
        frame = Frame(self.action, whence)

        hands = []        
        for leap_hand in leap_frame.hands:
            hand = Hand.of(frame, leap_hand)
            fingers = []
            for leap_finger in leap_hand.fingers:
                finger = Finger.of(hand, leap_finger)
                leap_bones = [ leap_finger.bone(t.value) for t in Bone.Type ]
                bones = map(
                    lambda leap_bone: Bone.of(finger, leap_bone),
                    leap_bones
                )
                fingers.append((finger, bones))
            hands.append((hand, fingers))

        return frame, hands

    @property
    def ready(self):
        return self.controller.is_connected
