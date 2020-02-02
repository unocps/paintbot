#!/usr/bin/env python

from descriptions import NavigateToWallPrimitiveDescription
from geometry_msgs.msg import Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from skiros2_common.core.primitive import PrimitiveBase
from tf.transformations import quaternion_from_euler
import actionlib
import math
import rospy

_ACTION_DIST = 0.5
_WALL_THICKNESS = 0.05

def _normalize_angle(theta):
    if theta < -math.pi:
        theta += 2 * math.pi
    if theta > math.pi:
        theta -= 2 * math.pi
    return theta

class NavigateToWallPrimitive(PrimitiveBase):
    def createDescription(self):
        self.setDescription(NavigateToWallPrimitiveDescription(), self.__class__.__name__)

    def onInit(self):
        self.mb_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.mb_client.wait_for_server()

    def onStart(self):
        wall_facing = self.params['wall_facing'].value
        self.x = self.params['wall_x'].value + ((_ACTION_DIST + _WALL_THICKNESS) * math.cos(wall_facing))
        self.y = self.params['wall_y'].value + ((_ACTION_DIST + _WALL_THICKNESS) * math.sin(wall_facing))
        self.yaw = _normalize_angle(wall_facing - math.pi)

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = self.x
        goal.target_pose.pose.position.y = self.y
        goal.target_pose.pose.orientation = Quaternion(*quaternion_from_euler(0, 0, self.yaw))

        # TODO: Figure out how to set up callbacks
        self.mb_client.send_goal(goal)
        # wait = mb_client.wait_for_result()
        # result = mb_client.get_result()

    def execute(self):
        # if self.moving:
        #     return self.step('Moving arm to zero position')
        return self.success('Navigating to ({}, {}) @ {}'.format(self.x, self.y, self.yaw))

    def onPreempt(self):
        # TODO: Stop motion
        return self.success('Navigation preempted')
