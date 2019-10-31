# -*- coding: utf-8 -*-

import sqlite3


class Entity(object):

    __slots__ = [ 'saved', 'id' ]
    
    _insert_query_ = None
    _connection_ = None
    _cursor_ = None

    @classmethod
    def bootstrap(cls, db_path):
        # type: (str) -> None
        cls._connection_ = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )

    @classmethod
    def cursor(cls):
        # type: () -> sqlite3.Cursor
        if cls._connection_ is None:
            raise RuntimeError('Entity wasn\'t initialized.')
        if cls._cursor_ is None:
            cls._cursor_ = cls._connection_.cursor()
        return cls._cursor_

    @classmethod
    def commit(cls):
        return cls._connection_.commit()

    @classmethod
    def rollback(cls):
        return cls._connection_.rollback()

    @classmethod
    def _insert_(cls):
        # type: () -> str
        if cls._insert_query_ is None:
            name = cls._table_
            keys = ','.join(cls.__slots__)
            values = ','.join(['?'] * len(cls.__slots__))
            cls._insert_query_ = '''
            INSERT INTO {0} ({1}) VALUES ({2})
            '''.format(name, keys, values)
        return cls._insert_query_

    def __init__(self):
        self.saved = False
        self.id = None

    def save(self):
        # type: () -> int
        if not self.saved:
            slots = type(self).__slots__
            attrs = [getattr(self, slot) for slot in slots]
            for i, attr in enumerate(attrs):
                if isinstance(attr, Entity):
                    attrs[i] = attr.save()

            self.cursor().execute(
                self._insert_(),
                tuple(attrs)
            )

            self.id = self.cursor().lastrowid
            self.saved = True        
        
        return self.id
