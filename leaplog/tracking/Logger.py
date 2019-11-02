# -*- coding: utf-8 -*-

import sqlite3
from time import time
from .data import *
from .Message import Message
from utils import db_path


class Logger(object):

    __slots__ = [ 'frames', 'messenger', 'running', 'subject', 'action' ]

    def __init__(self, db_path, messenger):
        # type: (Queue) -> Logger
        self.frames = []
        self.messenger = messenger
        self.running = False
        self.subject = None
        self.action = None

    def log(self):
        # type: () -> None
        Entity.bootstrap(db_path)
        print('Starting log')

        while True:
            order, payload = self.messenger.get()
            
            if order == Message.FRAME:
                self.frames.append(payload)

            elif order == Message.START:
                if isinstance(payload, Subject):
                    self.subject = payload
                elif isinstance(payload, Action):
                    self.action = action

            elif order == Message.SAVE:
                self.save()
            
            elif order == Message.NEXT:
                self.action = payload
                self.logging = True

            elif order == Message.STOP:
                if isinstance(payload, Subject):
                    self.save()
                    self.running = False
                    break
                elif isinstance(payload, Action):
                    self.running = False

            elif order == Message.REMAKE:
                self.discard()

        print('Terminating log')

    def save(self):
        # type: () -> None
        self.subject.save()
        self.action.save()

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

    def discard(self):
        # type: () -> None
        Entity.rollback()
        self.frames = []
