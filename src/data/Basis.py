# -*- coding: utf-8 -*-

from .Entity import Entity
from .Vector import Vector


class Basis(Entity):

    __slots__ = [ 'x', 'y', 'z', 'origin' ]

    def __init__(self, leap_matrix):
        # type: (Leap.Matrix) -> Basis
        self.x = Vector(leap_matrix.x_basis)
        self.y = Vector(leap_matrix.y_basis)
        self.z = Vector(leap_matrix.z_basis)
        self.origin = Vector(leap_matrix.origin)
    