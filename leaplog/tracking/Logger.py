# -*- coding: utf-8 -*-

import sqlite3
from multiprocessing import Process
from time import time
from .data import *
from .Message import Message
from utils import db_path


class Logger(Process):

    __slots__ = [ 'frames', 'messenger', 'running', 'subject', 'action' ]

    def __init__(self, messenger, logger):
        # type: (Queue) -> Logger
        super(Logger, self).__init__()
        self.frames = []
        self.messenger = messenger
        self.logger = logger
        self.running = False
        self.subject = None
        self.action = None

    def run(self):
        # type: () -> None
        self.logger.info('LOGGER - Bootstraping database connection...')
        Entity.bootstrap(db_path)
        self.logger.info('LOGGER - OK')
        
        self.logger.info('LOGGER - Starting log')
        while True:
            order, payload = self.messenger.get()
        
            if order == Message.TERMINATE:
                self.logger.info('LOGGER - Terminating')
                self.discard()
                return

            elif order == Message.FRAME:
                self.logger.debug('LOGGER - Received frame')
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

        self.logger.info('LOGGER - Terminating log')

    def save(self):
        # type: () -> None
        self.logger.warn('LOGGER - SAVING...')
        self.action.subject = self.subject
        if not self.subject.saved:
            self.logger.info("LOGGER - Saving subject")
            self.subject.save()

        if not self.action.saved:
            self.logger.info("LOGGER - Saving action")
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
        self.logger.warn('LOGGER - OK')

    def discard(self):
        # type: () -> None
        self.logger.info('LOGGER - Discarding %d frames' % len(self.frames))
        Entity.rollback()
        self.frames = []
