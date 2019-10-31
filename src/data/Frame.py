# -*- coding: utf-8 -*-

from .Entity import Entity

class Frame(Entity):

    __slots__ = [ 'action', 'whence' ]
    _table_ = 'frames'

    def __init__(self, action, whence):
        # type: (Action, int, Leap.Frame) -> Action
        super(Frame, self).__init__()
        self.action = action
        self.whence = whence
