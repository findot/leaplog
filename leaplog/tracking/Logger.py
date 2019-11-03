# -*- coding: utf-8 -*-

import sqlite3
from multiprocessing import Process
from time import time
from .data import *
from .Message import Message
from utils import db_path


class Logger(Process):

    __slots__ = [ 'frames', 'messenger', 'running', 'subject', 'action' ]

    def __init__(self, messenger):
        # type: (Queue) -> Logger
        super(Logger, self).__init__()
        self.frames = []
        self.messenger = messenger
        self.running = False
        self.subject = None
        self.action = None

    def run(self):
        # type: () -> None
        Entity.bootstrap(db_path)
        print('Starting log')

        messages = []
        while True:
            while not self.messenger.empty():
                messages.append(self.messenger.get())

            while not len(messages) == 0:
                order, payload = messages.pop()
            
                if order == Message.FRAME:
                    self.frames.append(payload)

                elif order == Message.START:
                    if isinstance(payload, Subject) and not self.subject == payload:
                        self.subject = payload
                    elif isinstance(payload, Action) and not self.action == payload:
                        self.action = payload

                elif order == Message.SAVE:
                    self.save()
                
                elif order == Message.NEXT:
                    self.action = payload
                    self.running = True

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
        self.action.subject = self.subject
        if not self.subject.saved:
            print("Saving subject")
            self.subject.save()

        if not self.action.saved:
            print("Saving action")
            self.action.save()

        try:
        
            for frame, hands in self.frames:
                frame.action = self.action
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
