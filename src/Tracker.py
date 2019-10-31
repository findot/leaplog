# -*- coding: utf-8 -*-

import sqlite3
import time
from datetime import datetime
from .data import *


class Tracker(object):

    __slots__ = [ 'frames', 'action' ]

    def __init__(self, action):
        self.action = action
        self.frames = []

    def track(self, leap_frame):
        whence = time.mktime(datetime.now().timetuple()) - self.action.record_time
        frame = Frame(self.action, whence)
        hands = [ self._track_hand(frame, hand) for hand in leap_frame.hands ]
        self.frames.append((frame, hands))

    def _track_hand(self, frame, leap_hand):
        hand = Hand(frame, leap_hand)
        fingers = []
        for leap_finger in leap_hand.fingers:
            finger = Finger(hand, leap_finger)
            leap_bones = [ leap_finger.bone(t.value) for t in Bone.Type ]
            bones = map(
                lambda leap_bone: Bone(finger, leap_bone),
                leap_bones
            )
            fingers.append((finger, bones))
        return hand, fingers

    def save(self):
        try:
        
            for frame, hands in self.frames:
                for hand, fingers in hands:
                    for finger, bones in fingers:
                        for bone in bones:
                            bone.save()
                        finger.save()
                    hand.save()
                frame.save()
        
        except sqlite3.Error as e:
            Entity.rollback()
            raise e
        
        Entity.commit()
