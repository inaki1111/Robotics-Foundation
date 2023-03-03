#!/usr/bin/env python
import rospy
import math
import time 
from std_msgs.msg import Float32

def funcsen(x, amplitud, frecuencia, desfase):
	value = amplitud * math.sin(frecuencia * x + desfase)
    	return value



if __name__=='__main__':
    inicio = time.time()
    pub2=rospy.Publisher("/time",Float32, queue_size=10)
    pub=rospy.Publisher("/signal",Float32, queue_size=10)
    rospy.init_node("signal_generator")
    rate = rospy.Rate(20)
    x = 1
    amplitud = 1
    frecuencia = 10
    desfase = 0

    while not rospy.is_shutdown():
	x = x + .01
	value = funcsen(x,amplitud, frecuencia, desfase)
       	rospy.loginfo(value)
       	pub.publish(value)
	final = time.time()
	tiempo = final - inicio
	rospy.loginfo(tiempo)
	pub2.publish(tiempo)
       	rate.sleep()
