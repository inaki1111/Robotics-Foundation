/*
 * rosserial PubSub Example
 * Prints "hello world!" and toggles led
 */

#include <ros.h>
#include <std_msgs/Float32.h>



//Encoder #1
const int pinCanalA=2;
const int pinCanalB=4;

//Control Motor 1
const int motorPin1=11;
const int motorPin2=10;


float dt=0.02;
float tiempo=0;
float contador=0;
float pos=0;
float pos_ant=0;
float vel=0;
float VMotor=0;
float valorM=0;

String refstring="";
float referencia=0;

ros::NodeHandle  nh;

float x = 0;
float absx;

//void messageCb( const std_msgs::Empty& toggle_msg){
//  digitalWrite(13, HIGH-digitalRead(13));   // blink the led
//}


void callback_motor_velocity(const std_msgs::Float32& msg){
    x = msg.data;
    if (x > 0){
      absx = abs(x);
      analogWrite(motorPin1,absx);
      analogWrite(motorPin2,0);
      nh.loginfo("Hacia atras");
    }
    else if (x<0){
      absx = abs(x);
      analogWrite(motorPin1,0);
      analogWrite(motorPin2,absx);
      nh.loginfo("Hacia delante"); 
    }
    else {
      analogWrite(motorPin1,0);
      analogWrite(motorPin2,0);
      nh.loginfo("No se mueve");      
    }

    nh.loginfo("callback");
}

std_msgs::Float32 test;

ros::Subscriber<std_msgs::Float32> sub("/cmd_pwm", &callback_motor_velocity);



//std_msgs::String str_msg;
//ros::Publisher chatter("chatter", &str_msg);

//char hello[13] = "hello world!";

void setup()
{
  //attachInterrupt(digitalPinToInterrupt(pinCanalA),Encoder,RISING);
  pinMode(pinCanalA,INPUT);
  pinMode(pinCanalB,INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(motorPin1,OUTPUT);
  pinMode(motorPin2,OUTPUT);
  nh.initNode();
  //nh.advertise(chatter);
  nh.subscribe(sub);
}

void loop()
{
  //str_msg.data = hello;
  
  //chatter.publish( &str_msg );
  nh.spinOnce();
  delay(500);
}
