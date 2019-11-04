# -*- coding: utf-8 -*-

from .Entity import Entity


class Action(Entity):

    __slots__ = [ 'subject', 'reference', 'record_time' ]
    _table_ = 'actions'

    def __init__(self, subject, reference, record_time, id=None):
        # type: (Subject, int, int) -> Action
        super(Action, self).__init__(id)
        self.subject = subject
        self.reference = reference
        self.record_time = record_time

    def to_dict(self):
        return {
            'reference': self.reference,
            'record_time': self.record_time
        }

    def __eq__(self, other):
        if not isinstance(other, Action):
            return False
        return self.reference == other.reference
