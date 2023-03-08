#!/usr/bin/env python
import rospy
import numpy as np

from pid_control.msg import motor_output
from pid_control.msg import motor_input
from pid_control.msg import set_point


#Setup parameters, vriables and callback functions here (if required)
control_signal = 0.0
reference1 = 0.0
prev_error = 0.0
integral_term = 0.0
motor_o = 0
reference = 0
motor =0
reference_t = 0.0
motor_signal = 0

e=[0.0,0.0,0.0]
#e[0] error actual    e[1] error anterior    e[2] error dos veces anterior
u=[0.0,0.0]
#u[0] salida actual    u[1] salida anterior
Ts = 0.002 
#periodo de muestreo

#ganancias del modelo discreto
kp = rospy.get_param("/proportional",0.0)
ki = rospy.get_param("/integral",0.0)
kd = rospy.get_param("/derivative",0.0)

l=4

K1=kp + Ts*ki + kd/Ts
K2=-kp - 2.0*kd/Ts
K3=kd/Ts

# definir la funcuion de callback 
 

def callback_reference(msg):
  global reference, reference_t
  reference = msg.reference
  reference_t = msg.time

def callback_motor_output(msg):
  global motor_o
  motor_o = msg.output
  



#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':

    #Initialise and Setup node
    rospy.init_node("controller")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)
    rospy.Subscriber("/set_point", set_point, callback_reference)
    rospy.Subscriber("/motor_output", motor_output, callback_motor_output)
    motor_input_pub = rospy.Publisher("/motor_input", motor_input, queue_size=10)
    
    
    #Definir el error inicial
    prev_error = 0
    integral_term = 0



    print("The Controller is Running")
    #Run the node
    while not rospy.is_shutdown():

        #Write your code here
        e[0]=reference - motor_o
        u[0]=K1*e[0]+K2*e[1]+K3*e[2]+u[1]
        e[2]=e[1]
        e[1]=e[0]
        u[1]=u[0]

        if(u[0]>l):
          u[0]=l
        if(u[0]<-l):
          u[0]=-l

        
        #rospy.loginfo(control_signal)
        
        
        motor_i = motor_input()
        motor_i.input = u[0]
        motor_i.time = rospy.get_time()
        motor_input_pub.publish(motor_i)
        
      
        rospy.loginfo("Entrada motor: %f", motor_i.input)
        rospy.loginfo("Referencia: %f", reference)
        rospy.loginfo("Salida del motor: %f", motor_o)
        rospy.loginfo("Error: %f", e[0])
        rospy.loginfo("Salida del controlador: %f", u[0])
        rospy.loginfo("Valores del PID: %f, %f, %f", kp, ki, kd)
        rate.sleep()

