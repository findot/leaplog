# -*- coding: utf-8 -*-

from .Entity import Entity


class Vector(Entity):

    __slots__ = [ 'x', 'y', 'z', 'pitch', 'yaw', 'roll' ]
    _table_ = 'vectors'

    @classmethod
    def of(cls, leap_vector):
        x = leap_vector.x
        y = leap_vector.y
        z = leap_vector.z
        pitch = leap_vector.pitch
        yaw = leap_vector.yaw
        roll = leap_vector.roll

        return cls(x, y, z, pitch, yaw, roll)


    def __init__(self, x, y, z, pitch, yaw, roll, id=None):
        # typê: (Leap.Vector) -> Vector
        super(Vector, self).__init__(id)
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
