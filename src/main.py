# -*- coding: utf-8 -*-

import Leap

from datetime import datetime
import time
from .Tracker import Tracker
from .data import *


def main():

    Entity.bootstrap('data.db')
    c = Leap.Controller()
    if not c.is_connected:
        raise RuntimeError('Leap Motion is not connected')
    s = Subject('Florian', 'Indot')
    a = Action(s, 1, time.mktime( datetime.now().timetuple() ))
    t = Tracker(a)
    
    while len(t.frames) < 1000:
        t.track(c.frame())
    t.save()


if __name__ == '__main__':
    main()
