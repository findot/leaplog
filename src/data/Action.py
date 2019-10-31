# -*- coding: utf-8 -*-

from .Entity import Entity


class Action(Entity):

    __slots__ = [ 'subject', 'reference', 'record_time' ]

    def __init__(self, subject, reference, record_time):
        # type: (Subject, int, int) -> Action
        super(Action, self).__init__()
        self.subject = subject
        self.reference = reference
        self.record_time = record_time
