# -*- coding: utf-8 -*-

from os.path import realpath, dirname

app_root = dirname(dirname(dirname(realpath(__file__))))
db_path = '{0}/data.db'.format(app_root)