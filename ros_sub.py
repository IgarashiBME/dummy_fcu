#! /usr/bin/env python

# Calculate absolute orientation from trajectory 
# using GNSS UTM cordinate date

import rospy
import time
import numpy as np

from mavros_msgs.msg import Mavlink

def subs(message):
    if message.msgid != 30 and message.msgid != 31 and message.msgid != 32 and message.msgid != 33 and message.msgid != 105 and message.msgid != 141 and message.msgid != 83 and message.msgid != 2 and message.msgid != 147 and message.msgid != 24 and message.msgid != 74 and message.msgid != 111 and message.msgid != 140 and message.msgid != 85 and message.msgid != 245 and message.msgid != 1 and message.msgid != 230 and message.msgid != 241 and message.msgid != 242 and message.msgid != 76 and message.msgid != 0:
        print message.msgid

def shutdown():
    rospy.loginfo("subscribe_node was terminated")

def listener():
    rospy.init_node('mavros_subscriber')
    rospy.on_shutdown(shutdown)
    rospy.Subscriber('mavlink/from', Mavlink, subs) # ROS callback function
    rospy.spin()

if __name__ == '__main__':
    listener()
