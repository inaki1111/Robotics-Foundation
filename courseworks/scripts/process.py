#!/usr/bin/env python
import rospy
import math
import time
from std_msgs.msg import Float32


def callback(data):
  rospy.loginfo(data.data)
  process_signal = math.sin(data.data) * 0.5
  pub.publish(process_signal)

def listener():
    rospy.init_node("process")
    rospy.Subscriber("/signal", Float32, callback)
    global pub
    pub = rospy.Publisher("/proc_signal", Float32, queue_size=10)
    rospy.spin()

if __name__=='__main__':
    listener()
