#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def navigate():
    rospy.init_node('navigation')
    pub = rospy.Publisher('/paintbot/diff_drive_controller/cmd_vel', Twist)
    rate = rospy.Rate(2)

    while not rospy.is_shutdown():
        twist = Twist()
        twist.angular.z = -1
        pub.publish(twist)

        rate.sleep()

if __name__ == '__main__':
    try:
        navigate()
    except rospy.ROSInterruptException:
        pass
