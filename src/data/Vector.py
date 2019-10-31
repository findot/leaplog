# -*- coding: utf-8 -*-

from .Entity import Entity


class Vector(Entity):

    __slots__ = [ 'x', 'y', 'z' ]

    _insert_ = '''
    INSERT INTO vectors (x, y, z) VALUES (?, ?, ?);
    '''

    def __init__(self, x, y, z):
        super(Vector, self).__init__()
        self.x, self.y, self.z = x, y, z
