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

    def __init__(self, finger, leap_bone):
        # type: (Finger, Leap.Bone) -> Bone
        super(Bone, self).__init__()
        self.finger = finger
        self.basis = Basis(leap_bone.basis)
        self.direction = Vector(leap_bone.direction)
        self.center = Vector(leap_bone.center)
        self.type   = leap_bone.type
        self.length = leap_bone.length
        self.width  = leap_bone.width
