# -*- coding: utf-8 -*-

import sqlite3
from time import time
from .data import *
from .Message import Message

class Logger(object):

    __slots__ = [ 'frames', 'messenger', 'logging' ]

    def __init__(self, messenger):
        # type: (Queue) -> Logger
        self.frames = []
        self.messenger = messenger
        self.logging = False

    def log(self):

        subject = None
        action = None

        print('Starting logging')

        while True:
            order, payload = self.messenger.get()
            
            if order == Message.FRAME:
                self.frames.append(payload)

            elif order == Message.START:
                subject = payload

            elif order == Message.SAVE:
                assert payload == action
                action.save()
                action = None
                self.save()
            
            elif order == Message.NEXT:
                if self.logging:
                    action.save()
                    self.save()
                action = payload
                self.logging = True

            elif order == Message.STOP:
                if self.logging:
                    action.save()
                    self.save()
                self.logging = False
                break

            elif order == Message.REMAKE and self.logging:
                assert action == payload
                Entity.rollback()
                self.frames = []

        print('Terminating logging')

    def save(self):
        try:
        
            for frame, hands in self.frames:
                for hand, fingers in hands:
                    for finger, bones in fingers:
                        for bone in bones:
                            bone.save()
                        finger.save()
                    hand.save()
                frame.save()
        
        except sqlite3.Error as e:
            Entity.rollback()
            raise e
        
        Entity.commit()
        self.frames = []
