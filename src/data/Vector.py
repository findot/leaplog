# -*- coding: utf-8 -*-

from .Entity import Entity


class Vector(Entity):

    __slots__ = [ 'x', 'y', 'z', 'pitch', 'yaw', 'roll' ]
    _table_ = 'vectors'

    def __init__(self, leap_vector):
        # typê: (Leap.Vector) -> Vector
        super(Vector, self).__init__()
        self.x = leap_vector.x
        self.y = leap_vector.y
        self.z = leap_vector.z
        self.pitch = leap_vector.pitch
        self.yaw = leap_vector.yaw
        self.roll = leap_vector.roll
