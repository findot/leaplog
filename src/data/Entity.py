# -*- coding: utf-8 -*-

import sqlite3


class Entity(object):

    __slots__ = [ 'saved', 'id' ]
    
    _connection_ = None
    _cursor_ = None

    @classmethod
    def init(cls, db_path):
        cls._connection_ = sqlite3.connect(db_path)

    @classmethod
    def cursor(cls):
        if cls._connection_ is None:
            raise RuntimeError('Entity wasn\'t initialized.')
        if cls._cursor_ is None:
            cls._cursor_ = cls._connection_.cursor()
        return cls._cursor_

    def __init__(self):
        self.saved = False
        self.id = None

    def save(self):
        if self.saved:
            return
        
        slots = type(self).__slots__
        attrs = [getattr(self, slot) for slot in slots]
        for i, attr in attrs:
            if isinstance(attr, Entity) and not attr.saved:
                pass # TODO - replace Entity attrs with their ids        

        self.cursor().execute(
            self._insert_,
            tuple(attrs)
        )

        self.id = self.cursor().lastrowid
        self.saved = True
        
        return self.id
