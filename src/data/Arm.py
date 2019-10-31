# -*- coding: utf-8 -*-

from .Entity import Entity
from .Basis import Basis
from .Vector import Vector

class Arm(Entity):

    __slots__ = [ 'basis', 'direction', 'elbow_position', 'wrist_position',
                  'width' ]

    def __init__(self, leap_arm):
        # type: ()
        super(Arm, self).__init__()
        self.basis = Basis(leap_arm.basis)
        self.direction = Vector(leap_arm.direction)
        self.elbow_position = Vector(leap_arm.elbow_position)
        self.wrist_position = Vector(leap_arm.wrist_position)
        self.width = width
