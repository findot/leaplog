# -*- coding: utf-8 -*-

from pony.orm import *

class Vector(db.Entity):

    _table_ = 'vectors'

    id      = PrimaryKey(int, auto=True)