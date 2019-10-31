# -*- coding: utf-8 -*-

from .Entity import Entity


class Basis(Entity):

    __slots__ = [ 'x', 'y', 'z' ]

    _insert_ = '''
    INSERT INTO basis (x, y, z) VALUES (?, ?, ?)
    '''

    def __init__(self, x, y, z):
        # type: (Vector, Vector, Vector) -> Basis
        self.x, self.y, self.z = x.id, y.id, z.id
    