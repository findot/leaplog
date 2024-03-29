# -*- coding: utf-8 -*-

from .Entity import Entity

class Frame(Entity):

    __slots__ = [ 'action', 'whence' ]
    _table_ = 'frames'

    def __init__(self, action, whence, id=None):
        # type: (Action, int, Leap.Frame) -> Action
        super(Frame, self).__init__(id)
        self.action = action
        self.whence = whence
