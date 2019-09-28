#!/usr/bin/env python

from gazebo_msgs.msg import ModelStates
import geometry_msgs
import math
import rospy

class Task:
    def __init__(self, name, dest):
        self.name = name
        self.dest = dest

tasks = [
    Task('GET_PAINT', (2, 1)),
    Task('APPLY_PAINT', (-1, -1))
]
pose = None

def update_pose(msg):
    global pose
    pose = msg.pose[msg.name.index('paintbot')]

def plan():
    rospy.init_node('planning')

    rate = rospy.Rate(2)
    model_states_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, update_pose)
    nav_pub = rospy.Publisher('/paintbot/nav', geometry_msgs.msg.Point, queue_size=10)
    task_i = 0

    while not rospy.is_shutdown():
        # if at_dest(task_i):
        #     task_i = (task_i + 1) % len(tasks)
        # else:
        dest = geometry_msgs.msg.Point()
        dest.x = tasks[task_i].dest[0]
        dest.y = tasks[task_i].dest[1]
        nav_pub.publish(dest)

        rate.sleep()

if __name__ == '__main__':
    try:
        plan()
    except rospy.ROSInterruptException:
        pass
