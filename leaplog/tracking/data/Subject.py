# -*- coding: utf-8 -*-

from .Entity import Entity


class Subject(Entity):

    __slots__ = [ 'firstname', 'lastname' ]
    _table_ = 'subjects'

    def __init__(self, firstname, lastname, id=None):
        # type: (str, str) -> Subject
        super(Subject, self).__init__(id)
        self.firstname = firstname
        self.lastname = lastname

    def to_dict(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname
        }
