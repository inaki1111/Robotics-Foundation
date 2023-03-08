/*
 * rosserial Subscribe to a topic cmd_pwm to recieve the velocity of the motor
 * 
 */

#include <ros.h>
#include <std_msgs/Float32.h>


//Encoder #1
const int pinCanalA=2;
const int pinCanalB=4;

//Control Motor 1
const int motorPin1=11;
const int motorPin2=10;



// Variables para el cálculo de la velocidad
volatile int encoderPos = 0;
volatile unsigned long lastMicros = 0;
volatile float rpm = 0.0;

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

ros::Subscriber<std_msgs::Float32> sub("/motor_input", &callback_motor_velocity);



std_msgs::Float32 str_msg;
ros::Publisher chatter("motor_output", &str_msg);


void setup()
{
  attachInterrupt(digitalPinToInterrupt(pinCanalA),countPulses,RISING);
  pinMode(pinCanalA,INPUT);
  pinMode(pinCanalB,INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(motorPin1,OUTPUT);
  pinMode(motorPin2,OUTPUT);
  nh.initNode();
  nh.advertise(chatter);
  nh.subscribe(sub);
}

void loop()
{
    // Calcular la velocidad en RPM
  unsigned long currentMicros = micros();
  float elapsedTime = (currentMicros - lastMicros) / 1000000.0; // tiempo transcurrido en segundos
  rpm = (encoderPos * 60.0) / (elapsedTime * 12.0); // 12 es el número de pulsos por vuelta del encoder

  // Reiniciar el contador de pulsos y el temporizador
  encoderPos = 0;
  lastMicros = currentMicros;
  str_msg.data = hello;
  
  chatter.publish( &str_msg );
  nh.spinOnce();
  delay(500);
}


void countPulses() {
  // Leer el estado del canal B del encoder
  int bState = digitalRead(pinCanalB);

  // Incrementar o decrementar el contador de pulsos en función del estado de los canales A y B
  if (bState == LOW) {
    encoderPos++;
  } else {
    encoderPos--;
  }
}