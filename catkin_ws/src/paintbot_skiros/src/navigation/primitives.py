#!/usr/bin/env python

from descriptions import NavigateToWallPrimitiveDescription
from geometry_msgs.msg import Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from skiros2_common.core.primitive import PrimitiveBase
from tf.transformations import euler_from_quaternion, quaternion_from_euler
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
        wall_loc = self.params['Destination'].value
        wall_facing = euler_from_quaternion([
                0.0,
                0.0,
                wall_loc.getProperty('skiros:OrientationZ').value,
                wall_loc.getProperty('skiros:OrientationW').value
            ])[2]
        self.x = wall_loc.getProperty('skiros:PositionX').value + ((_ACTION_DIST + _WALL_THICKNESS) * math.cos(wall_facing))
        self.y = wall_loc.getProperty('skiros:PositionY').value + ((_ACTION_DIST + _WALL_THICKNESS) * math.sin(wall_facing))
        self.yaw = _normalize_angle(wall_facing - math.pi)
        self.status = 1

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = self.x
        goal.target_pose.pose.position.y = self.y
        goal.target_pose.pose.orientation = Quaternion(*quaternion_from_euler(0, 0, self.yaw))
        self.mb_client.send_goal(goal, self.done_callback)

        return True

    def execute(self):
        if self.status == 1:
            return self.step('Navigating to ({}, {}) @ {}'.format(self.x, self.y, self.yaw))
        elif self.status == 3:
            return self.success('Reached ({}, {}) @ {}'.format(self.x, self.y, self.yaw))
        return self.fail('Unable to navigate to ({}, {}) @ {}'.format(self.x, self.y, self.yaw))

    def onPreempt(self):
        self.mb_client.cancel_goal()
        return self.success('Navigation preempted')

    def done_callback(self, status, result):
        self.status = status
