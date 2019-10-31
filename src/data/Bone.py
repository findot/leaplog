# -*- coding: utf-8 -*-

from .Entity import Entity


class Bone(Entity):

    __slots__ = [ 'basis', 'position', 'center', 'type', 'length', 'width' ] 

    _insert_ = '''
    INSERT INTO bones (basis, position, center, type, length, width) VALUES (
        ?, ?, ?, ?, ?, ?
    )
    '''    

    def __init__(self, basis, position, center, type, length, width):
        # type: (Basis, Vector, Vector, int, float, float) -> Bone
        self.basis = basis.id
        self.position = position.id
        self.center = center.id
        self.type = type
        self.length = length
        self.width = width
