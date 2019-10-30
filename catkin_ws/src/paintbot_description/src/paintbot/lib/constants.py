#!/usr/bin/env python

ITERATION_RATE_HZ = 10

TOPIC_ARM_SERVICE = '/paintbot/arm_controller/follow_joint_trajectory'
TOPIC_DIFF_DRIVE = '/paintbot/diff_drive_controller/cmd_vel'
TOPIC_MODEL_STATES = '/gazebo/model_states'
TOPIC_NAV = '/paintbot/nav'
TOPIC_NOTIFY = '/paintbot/notify'
TOPIC_PAINT = '/paintbot/paint'

NOTIFY_ACT_COMPLETE = 'act_complete'
NOTIFY_AT_DEST = 'at_dest'
ACT_PAINT_APPLY = 'paint_apply'
ACT_PAINT_LOAD = 'paint_load'
