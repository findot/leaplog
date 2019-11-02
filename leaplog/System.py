# -*- coding: utf-8 -*-

from os.path import dirname, realpath

topdir = dirname(dirname(realpath(__file__)))
db_path = '{0}/data.db'.format(topdir)

from multiprocessing import Queue, Process
from time import time
from .tracking import Tracker, Logger, Message
from tracking.data import Action


class System(object):

    ACTION_NUMBER = 10

    def __init__(self):
        self.experiment_start   = time()
        self.experiment_running = False

        self.subject            = None
        self.action             = None
        self.action_number      = 0
        self.action_running     = False

        self._order_queue       = Queue()
        self._logging_queue     = Queue()

        self.tracker            = Tracker(
            self._order_queue,
            self._logging_queue
        )
        self._tracking_worker   = Process(
            target=Tracker.track,
            args=(self.tracker,)
        )
        self.logger             = Logger(
            db_path,
            self._logging_queue
        )
        self._logging_worker    = Process(
            target=Logger.log,
            args=(self.logger,)
        )

    def start_experiment(self):
        if self.experiment_running:
            raise RuntimeError('An experiment is in progress!')
        if self.subject is None:
            raise RuntimeError('No subject specified!')
        
        self.action = Action(self.subject, self.action_number, None)

        self._tracking_worker.start()
        self._logging_worker.start()
        
        self._order_queue.put((Message.START, self.subject))
        
        self.experiment_running = True

    def stop_experiment(self):
        self._order_queue.put((Message.STOP, None))
        self._tracking_worker.join()

        self.experiment_running = False
        self.current_action = None
        self.current_subject = None


    def start_action(self):
        if self.action_running:
            raise RuntimeError('A recording is in progress!')
        self.action.record_time = time()
        self._order_queue.put((Message.NEXT, self.action))

    def stop_action(self):
        if not self.action_running:
            raise RuntimeError('No recording in progress!')
        self._order_queue.put((Message.STOP, self.action))
        self.action_running = False

    def next_action(self):
        if self.action_running:
            raise RuntimeError('A recording is in progress!')
        self.action_number += 1
        self.action = Action(self.current_subject, self.action_number, None)
        self.start_action(next_action)

    def remake_action(self):
        pass


    @property
    def status(self):
        subject = self.subject.to_dict() if self.subject else None
        action = self.action.to_dict() if self.action else None
        status = {
            'experiment_running': self.experiment_running,
            'experiment_start': self.experiment_start,
            'subject': subject,
            'action': action,
            'action_running': self.action_running,
            'actions_left': self.ACTION_NUMBER - self.action_number
        }

        return status
