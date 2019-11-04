# -*- coding: utf-8 -*-

from .Entity import Entity
from .Vector import Vector


class Basis(Entity):

    __slots__ = [ 'x', 'y', 'z', 'origin' ]
    _table_ = 'basis'

    @classmethod
    def of(cls, leap_matrix):
        x = Vector.of(leap_matrix.x_basis)
        y = Vector.of(leap_matrix.y_basis)
        z = Vector.of(leap_matrix.z_basis)
        origin = Vector.of(leap_matrix.origin)
    
        return cls(x, y, z, origin)

    def __init__(self, x, y, z, origin, id=None):
        # type: (Leap.Matrix) -> Basis
        super(Basis, self).__init__(id)
        self.x = x
        self.y = y
        self.z = z
        self.origin = origin
    