# -*- coding: utf-8 -*-

from multiprocessing import Queue, Process
from time import time
from .tracking import Tracker, Logger, Message
from tracking.data import Action


class System(object):

    ACTION_NUMBER = 10

    def __init__(self):
        self.experiment_start   = time()
        self.subject_registered = False
        self.experiment_running = False

        self.subject            = None
        self.action             = None
        self.action_number      = 0
        self.action_running     = False

        self._control_queue     = Queue()
        self._order_queue       = Queue()
        self._logging_queue     = Queue()

        self.tracker            = Tracker(
            self._control_queue,
            self._order_queue,
            self._logging_queue
        )
        self.logger             = Logger(
            self._logging_queue
        )

    def register_subject(self, subject):
        self.subject = subject
        self.subject_registered = True

    def start_experiment(self):
        if self.experiment_running:
            raise RuntimeError('An experiment is in progress!')
        if self.subject is None:
            raise RuntimeError('No subject specified!')
        
        self.action = Action(self.subject, self.action_number, None)

        self.tracker.start()
        self.logger.start()
        
        self._order_queue.put((Message.START, self.subject))
        self.experiment_running = True


    def stop_experiment(self):
        self._order_queue.put((Message.STOP, None))
        self.tracker.join()

        self.experiment_running = False
        self.current_action = None
        self.subject = None


    def start_action(self):
        if self.action_running:
            raise RuntimeError('A recording is in progress!')
        self.action.record_time = time()
        self._order_queue.put((Message.START, self.action))
        self.action_running = True
        print(self.action)

    def stop_action(self):
        if not self.action_running:
            raise RuntimeError('No recording in progress!')
        self._order_queue.put((Message.STOP, self.action))
        self.action_running = False

    def next_action(self):
        if self.action_running:
            raise RuntimeError('A recording is in progress!')
        self.action_number += 1
        self.action = Action(self.subject, self.action_number, None)
        
    def remake_action(self):
        pass

    def save_action(self):
        if self.action_running:
            raise RuntimeError('A recording is in progress!')
        self._order_queue.put((Message.SAVE, self.action))



    @property
    def status(self):
        subject = self.subject.to_dict() if self.subject else None
        action = self.action.to_dict() if self.action else None
        status = {
            'subject_registered': self.subject_registered,
            'experiment_running': self.experiment_running,
            'experiment_start': self.experiment_start,
            'subject': subject,
            'action': action,
            'action_running': self.action_running,
            'actions_left': self.ACTION_NUMBER - self.action_number,
            'error': self.error
        }

        return status

    @property
    def error(self):
        try:
            return str(self._control_queue.get_nowait())
        except:
            return None
