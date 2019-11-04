# -*- coding: utf-8 -*-

from enum import Enum

from .Entity import Entity
from .Vector import Vector
from .Basis import Basis


class Bone(Entity):

    __slots__ = [ 'finger', 'basis', 'direction', 'center', 'type', 'length',
                  'width' ] 
    _table_ = 'bones'

    class Type(Enum):
        TYPE_THUMB = 0
        TYPE_INDEX = 1
        TYPE_MIDDLE = 2
        TYPE_RING = 3
        TYPE_PINKY = 4

    @classmethod
    def of(cls, finger, leap_bone):
        finger = finger
        basis = Basis.of(leap_bone.basis)
        direction = Vector.of(leap_bone.direction)
        center = Vector.of(leap_bone.center)
        type   = leap_bone.type
        length = leap_bone.length
        width  = leap_bone.width

        return cls(finger, basis, direction, center, type, length, width)


    def __init__(self, finger, basis, direction, center, type, length, width, id=None):
        # type: (Finger, Leap.Bone) -> Bone
        super(Bone, self).__init__(id)
        self.finger = finger
        self.basis = basis
        self.direction = direction
        self.center = center
        self.type   = type
        self.length = length
        self.width  = width
