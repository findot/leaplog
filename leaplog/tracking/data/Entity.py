# -*- coding: utf-8 -*-

import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class EntityMeta(type):

    def __getitem__(cls, key):
        if not isinstance(key, int):
            raise TypeError('Unsupported type for Entity access')
        return cls.select(key)

    def __iter__(cls):
        if not cls._rows_ or cls._updated_:
            cursor = cls.cursor().execute(cls._select_())
            cls._rows_ = cursor.fetchall()
            cls._updated_ = False
            cls._index_ = -1
        return cls
    
    def next(cls):
        if cls._index_ < len(cls._rows_):
            cls._index_ += 1
            return cls(**cls._rows_[cls._index_])
        raise StopIteration


class Entity(object):

    __metaclass__ = EntityMeta

    # ---------------------------------------------------------- STATIC METHODS

    __slots__ = [ 'saved', 'id' ]
    
    _insert_query_  = None
    _select_query_  = None
    _connection_    = None
    _cursor_        = None
    _rows_          = None
    _index_         = -1
    _updated_       = False

    @classmethod
    def bootstrap(cls, db_path):
        # type: (str) -> None
        cls._connection_ = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        cls._connection_.row_factory = dict_factory

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

    @classmethod
    def _select_(cls):
        if cls._select_query_ is None:
            name = cls._table_
            cls._select_query_ = '''
            SELECT * FROM {0}
            '''.format(name)
        return cls._select_query_

    # --------------------------------------------------------- DYNAMIC METHODS

    def __init__(self, id=None):
        self.saved = False
        self.id = None
        if id is not None:
            self.saved = True
            self.id = id

    def save(self):
        # type: () -> int
        if self.saved:
            return self.id

        attrs = [ getattr(self, slot) for slot in type(self).__slots__ ]

        for i, attr in enumerate(attrs):
            if isinstance(attr, Entity):
                attrs[i] = attr.save()

        self.cursor().execute(self._insert_(), tuple(attrs))
        self.id = self.cursor().lastrowid
        self.saved = True        
        
        type(self)._updated_ = True

        return self.id

    def __str__(self):
        return '{0}[{1}]'.format(self.__class__.__name__, self.id)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.id is not None and self.id == other.id
