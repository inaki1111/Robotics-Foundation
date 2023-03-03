#!/usr/bin/env python
import rospy
import numpy as np
from pid_control.msg import set_point



# Setup Variables, parameters and messages to be used (if required)
mysetpoint =set_point()

value = rospy.get_param("system_reference", 0)

#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("Set_Point_Generator")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

           #Setup Publishers and subscribers here 
    pub = rospy.Publisher("/set_point", set_point, queue_size=10)

    print("The Set Point Genertor is Running")
    init_time = rospy.get_time()
    
    #Run the node
    while not rospy.is_shutdown():

        #Write your code here
        mysetpoint =set_point()
        time = rospy.get_time()-init_time
        signal = np.sin(time)*value
        mysetpoint.reference = signal
        mysetpoint.time = time
        #rospy.loginfo(value)
        pub.publish(mysetpoint)

        rate.sleep()