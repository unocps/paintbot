#!/usr/bin/env python

from descriptions import NavigateToLocationPrimitiveDescription
from geometry_msgs.msg import Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from skiros2_common.core.primitive import PrimitiveBase
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import actionlib
import math
import rospy
import tf

_ACTION_DIST = 0.5
_WALL_THICKNESS = 0.05

def _normalize_angle(theta):
    if theta < -math.pi:
        theta += 2 * math.pi
    if theta > math.pi:
        theta -= 2 * math.pi
    return theta

class NavigateToLocationPrimitive(PrimitiveBase):
    def createDescription(self):
        self.setDescription(NavigateToLocationPrimitiveDescription(), self.__class__.__name__)

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
        self.dest = (
            wall_loc.getProperty('skiros:PositionX').value + ((_ACTION_DIST + _WALL_THICKNESS) * math.cos(wall_facing)),
            wall_loc.getProperty('skiros:PositionY').value + ((_ACTION_DIST + _WALL_THICKNESS) * math.sin(wall_facing))
        )
        self.pos_prev = None
        self.yaw = _normalize_angle(wall_facing - math.pi)
        self.dist = 0
        self.status = 1

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = self.dest[0]
        goal.target_pose.pose.position.y = self.dest[1]
        goal.target_pose.pose.orientation = Quaternion(*quaternion_from_euler(0, 0, self.yaw))
        self.mb_client.send_goal(goal, self._done_callback)

        self.tf_listener = tf.TransformListener()

        return True

    def execute(self):
        p_delta, o_delta = None, None
        try:
            p, o = self.tf_listener.lookupTransform('odom', 'virtual_base', rospy.Time(0))
            if self.pos_prev:
                self.dist += math.sqrt((self.pos_prev[0] - p[0])**2 + (self.pos_prev[1] - p[1])**2)
            self.pos_prev = p
            p_delta, o_delta = math.sqrt((self.dest[0] - p[0])**2 + (self.dest[1] - p[1])**2), _normalize_angle(self.yaw - euler_from_quaternion(o)[2])
        except:
            pass

        if self.status == 1:
            return self.step('Navigating to {} @ {}'.format(self.dest, self.yaw))
        elif self.status == 3:
            return self.success('Reached {} @ {} [Delta: {}, {}, Dist: {}]'.format(self.dest, self.yaw, p_delta, o_delta, self.dist))
        return self.fail('Unable to navigate to {} @ {}'.format(self.dest, self.yaw), -2)

    def onPreempt(self):
        self.mb_client.cancel_goal()
        return self.success('Navigation preempted')

    def _done_callback(self, status, result):
        self.status = status
