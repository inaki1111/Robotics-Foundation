#!/usr/bin/env python
import rospy
import numpy as np
import std_msgs.msg


type = rospy.get_param('/type', "step")
velocity = rospy.get_param('/velocity', 0.0)
t = 0

velocity = velocity * 255


# Stop Condition
def stop():
    # Setup the stop message (can be the same as the control message)
    print("Stopping")


if __name__ == '__main__':
    # Initialise and Setup node
    rospy.init_node("input")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    pub = rospy.Publisher('/cmd_pwm', std_msgs.msg.Float32, queue_size=10)
    print("Motor controller is running")
    while not rospy.is_shutdown():

        if velocity > 255:
            velocity = 255

        elif velocity <= -255:
            velocity = -255

        if type == "step":
            pwm = velocity
            pub.publish(pwm)

        elif type == "sin":
            pwm = ((velocity/2) * np.sin(rospy.get_time())) + (velocity/2)
            pub.publish(pwm)

        elif type == "square":
            pwm = 255 * np.sign(np.sin(rospy.get_time())+(velocity/255))
            if(pwm < 0):
                pwm = 0

            pub.publish(pwm)

        else:
            pwm = 0
            pub.publish(pwm)

        t = t + 1

        rospy.loginfo("PWM: %f", pwm)
        rospy.loginfo("Velocity: %f", velocity)
        rospy.loginfo("Type: %s", type)
        rospy.loginfo("Time: %f", rospy.get_time())
        rate.sleep()
