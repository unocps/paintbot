#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
import geometry_msgs
import math
import rospy

ORIENT_EPSILON = 0.1

pose = None
orient = None
dest = None

def update_state(msg):
    global pose, orient
    i = msg.name.index('paintbot')
    pose = msg.pose[i].position
    o = msg.pose[i].orientation
    orient = euler_from_quaternion([o.x, o.y, o.z, o.w])[2]

def update_dest(msg):
    global dest
    dest = msg

def at_dest():
    if pose:
        dist = math.sqrt(((pose.x - dest.x) ** 2) + ((pose.y - dest.y) ** 2))
        return dist < 0.1
    return false

def adjust_orientation(pub):
    theta = math.atan2(dest.y, dest.x) - orient
    while abs(theta) > ORIENT_EPSILON:
        twist = geometry_msgs.msg.Twist()
        twist.angular.z = -1 if theta < 0 else 1
        pub.publish(twist)
        theta = math.atan2(dest.y, dest.x) - orient

def navigate():
    rospy.init_node('navigation')

    rate = rospy.Rate(2)
    model_states_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, update_state)
    nav_sub = rospy.Subscriber('/paintbot/nav', geometry_msgs.msg.Point, update_dest)
    pub = rospy.Publisher('/paintbot/diff_drive_controller/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)

    while not rospy.is_shutdown():
        if pose and dest and orient and not at_dest():
            adjust_orientation(pub)
            # TODO: Move
        rate.sleep()

if __name__ == '__main__':
    try:
        navigate()
    except rospy.ROSInterruptException:
        pass
