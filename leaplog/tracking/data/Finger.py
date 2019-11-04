# -*- coding: utf-8 -*-

from .Entity import Entity


class Finger(Entity):

    __slots__ = [ 'hand', 'type' ]
    _table_ = 'fingers'

    @classmethod
    def of(cls, hand, leap_finger):
        hand = hand
        type = leap_finger.type
        return cls(hand, type)

    def __init__(self, hand, type, id=None):
        super(Finger, self).__init__(id)
        self.hand = hand
        self.type = type
