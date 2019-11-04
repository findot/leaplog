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

    @classmethod
    def of(cls, frame, leap_hand):
        frame          = frame
        arm            = Arm(leap_hand.arm)
        is_left        = leap_hand.is_left
        is_right       = leap_hand.is_right
        basis          = Basis(leap_hand.basis)
        direction      = Vector(leap_hand.direction)
        palm_normal    = Vector(leap_hand.palm_normal)
        palm_position  = Vector(leap_hand.palm_position)
        palm_velocity  = Vector(leap_hand.palm_velocity)
        wrist_position = Vector(leap_hand.wrist_position)
        confidence     = leap_hand.confidence
        time_visible   = leap_hand.time_visible
        sphere_center  = Vector(leap_hand.sphere_center)
        sphere_radius  = leap_hand.sphere_radius

        return cls(frame, arm, is_left, is_right, basis, direction,
                   palm_normal, palm_position, palm_velocity, wrist_position,
                   confidence, time_visible, sphere_center, sphere_radius)

    def __init__(self, frame, arm, is_left, is_right, basis, direction,
                 palm_normal, palm_position, palm_velocity, wrist_position,
                 confidence, time_visible, sphere_center, sphere_radius,
                 id=None):
        # type: (Frame, Leap.Hand) -> Hand
        super(Hand, self).__init__(id)
        self.frame          = frame
        self.arm            = arm
        self.is_left        = is_left
        self.is_right       = is_right
        self.basis          = basis
        self.direction      = direction
        self.palm_normal    = palm_normal
        self.palm_position  = palm_position
        self.palm_velocity  = palm_velocity
        self.wrist_position = wrist_position
        self.confidence     = confidence
        self.time_visible   = time_visible
        self.sphere_center  = sphere_center
        self.sphere_radius  = sphere_radius
