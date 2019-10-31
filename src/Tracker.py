# -*- coding: utf-8 -*-

from .data import *
import sqlite3


class Tracker(object):

    __slots__ = [ 'frames' ]

    def __init__(self):
        self.frames = []

    def track(self, leap_frame):
        frame = Frame(leap_frame)
        
        left_hand = None
        left_hand_fingers = []
        right_hand = None
        right_hand_fingers = []

        hands = [ self._track_hand(frame, hand) for hand in leap_frame.hands ]
        
        self.frames.append((frame, hands))

    def _track_hand(self, frame, leap_hand):
        hand = Hand(frame, leap_hand)
        fingers = []
        for leap_finger in leap_hand.fingers:
            finger = Finger(hand, leap_finger)
            leap_bones = [ leap_finger.bone(t.value) for t in Finger.Type ]
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
