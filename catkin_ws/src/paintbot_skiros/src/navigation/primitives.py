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
        self.tf_listener = tf.TransformListener()
        self.tf_listener.waitForTransform('world', 'virtual_base', rospy.Time(0), rospy.Duration(5))

        wall_loc = self.params['Destination'].value
        wall_facing = euler_from_quaternion([
                0.0,
                0.0,
                wall_loc.getProperty('skiros:OrientationZ').value,
                wall_loc.getProperty('skiros:OrientationW').value
            ])[2]
        self.dest = (
            (
                wall_loc.getProperty('skiros:PositionX').value + ((_ACTION_DIST + _WALL_THICKNESS) * math.cos(wall_facing)),
                wall_loc.getProperty('skiros:PositionY').value + ((_ACTION_DIST + _WALL_THICKNESS) * math.sin(wall_facing))
            ),
            _normalize_angle(wall_facing - math.pi)
        )
        self.pos_prev = None
        self.dist = 0
        self.status = 1
        self.pose_start = self._get_pose()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = self.dest[0][0]
        goal.target_pose.pose.position.y = self.dest[0][1]
        goal.target_pose.pose.orientation = Quaternion(*quaternion_from_euler(0, 0, self.dest[1]))
        self.mb_client.send_goal(goal, self._done_callback)

        return True

    def execute(self):
        pose = self._get_pose()
        if self.pos_prev:
            self.dist += math.sqrt((self.pos_prev[0] - pose[0][0])**2 + (self.pos_prev[1] - pose[0][1])**2)
        self.pos_prev = pose[0]

        msg = 'Navigating {} to {} [Pose: {}, Dist: {}]'.format(self.pose_start, self.dest, pose, self.dist)
        if self.status == 1:
            return self.step(msg)
        elif self.status == 3:
            return self.success(msg)
        return self.fail(msg, -2)

    def onPreempt(self):
        self.mb_client.cancel_goal()
        return self.success('Navigation preempted')

    def _done_callback(self, status, result):
        self.status = status

    def _get_pose(self):
        try:
            p, o = self.tf_listener.lookupTransform('world', 'virtual_base', rospy.Time(0))
            return ((p[0], p[1]), euler_from_quaternion(o)[2])
        except:
            return None
