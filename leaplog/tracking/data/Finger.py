# -*- coding: utf-8 -*-

from .Entity import Entity


class Finger(Entity):

    __slots__ = [ 'hand', 'type' ]
    _table_ = 'fingers'

    def __init__(self, hand, leap_finger):
        super(Finger, self).__init__()
        self.hand = hand
        self.type = leap_finger.type
