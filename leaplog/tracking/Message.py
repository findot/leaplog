# -*- coding: utf-8 -*-

from enum import Enum


class Message(Enum):

    START = 0
    NEXT = 1
    STOP = 2
    SAVE = 3
    REMAKE = 4
    FRAME = 5
    TERMINATE = 6