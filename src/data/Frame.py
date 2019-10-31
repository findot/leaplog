# -*- coding: utf-8 -*-

from .Entity import Entity
from .Hand import Hand

class Frame(Entity):

    __slots__ = [ 'action', 'whence', 'left_hand', 'right_hand' ]
    _ignore_ = [ 'left_hand', 'right_hand' ]

    def __init__(self, action, whence):
        # type: (Action, int, Leap.Frame) -> Action
        super(Frame, self).__init__()
        self.action = action
        self.whence = whence
