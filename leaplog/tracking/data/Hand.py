# -*- coding: utf-8 -*-

from .Entity import Entity
from .Frame import Frame
from .Arm import Arm
from .Basis import Basis
from .Vector import Vector

class Hand(Entity):

    __slots__ = [ 'frame', 'arm', 'is_left', 'is_right', 'basis', 'direction',
                  'palm_normal', 'palm_position', 'palm_velocity',
                  'wrist_position', 'confidence', 'time_visible',
                  'sphere_center', 'sphere_radius' ]
    _table_ = 'hands'

    def __init__(self, frame, leap_hand):
        # type: (Frame, Leap.Hand) -> Hand
        super(Hand, self).__init__()
        self.frame          = frame
        self.arm            = Arm(leap_hand.arm)
        self.is_left        = leap_hand.is_left
        self.is_right       = leap_hand.is_right
        self.basis          = Basis(leap_hand.basis)
        self.direction      = Vector(leap_hand.direction)
        self.palm_normal    = Vector(leap_hand.palm_normal)
        self.palm_position  = Vector(leap_hand.palm_position)
        self.palm_velocity  = Vector(leap_hand.palm_velocity)
        self.wrist_position = Vector(leap_hand.wrist_position)
        self.confidence     = leap_hand.confidence
        self.time_visible   = leap_hand.time_visible
        self.sphere_center  = Vector(leap_hand.sphere_center)
        self.sphere_radius  = leap_hand.sphere_radius