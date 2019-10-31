# -*- coding: utf-8 -*-

from .Entity import Entity


class Subject(Entity):

    __slots__ = [ 'firstname', 'lastname' ]

    def __init__(self, firstname, lastname):
        # type: (str, str) -> Subject
        super(Subject, self).__init__()
        self.firstname = firstname
        self.lastname = lastname
