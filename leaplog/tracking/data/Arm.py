# -*- coding: utf-8 -*-

from .Entity import Entity
from .Basis import Basis
from .Vector import Vector

class Arm(Entity):

    __slots__ = [ 'basis', 'direction', 'elbow_position', 'wrist_position',
                  'width' ]
    _table_ = 'arms'

    @classmethod
    def of(cls, leap_arm):
        
        basis = Basis.of(leap_arm.basis)
        direction = Vector.of(leap_arm.direction)
        elbow_position = Vector.of(leap_arm.elbow_position)
        wrist_position = Vector.of(leap_arm.wrist_position)
        width = leap_arm.width
        
        return cls(basis, direction, elbow_position, wrist_position, width)

    def __init__(self, basis, direction, elbow, wrist, width, id=None):
        # type: ()
        super(Arm, self).__init__(id)
        self.basis = basis
        self.direction = direction
        self.elbow_position = elbow
        self.wrist_position = wrist
        self.width = width
