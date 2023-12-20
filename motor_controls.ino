#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial HC06(10,11);

//Servo Connections
Servo myservo;
int servo = 6;

//Motor A Connections
int enA = 5;
int in1 = 8;
int in2 = 7;
// Motor B connections
int enB = 3;
int in3 = 9;
int in4 = 4;

int speed;

void setup() {
  HC06.begin(9600);
  Serial.begin(9600);
  myservo.attach(servo);
  // Set all the motor control pins to outputs
	pinMode(enA, OUTPUT);
	pinMode(enB, OUTPUT);
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	pinMode(in3, OUTPUT);
	pinMode(in4, OUTPUT);
	
	// Turn off motors - Initial state
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	digitalWrite(in3, LOW);
	digitalWrite(in4, LOW);

  //myservo.write(210);
}

void loop() {
  //Serial.println("Enter 1 to adjust motor speed or 2 for door: ");
  while (HC06.available() <= 0) {
  }
  Serial.println("received");

  char received = HC06.read();
  
  Serial.println(received);

  switch(received) {

    case '1':
      speedControl(60);
      break;

    case '2':
      speedControl(0);
      break;

    case '3':
      HC06.println(69);
      Serial.println("Opening Door");
      myservo.write(40);
      break;

    case '4':
      HC06.println(69);
      Serial.println("Closing Door");
      myservo.write(210);
      break; 

    case '5':
      if (speed >= 20){
        speedControl(speed-10);
      }
      break;

    case '6':
      if (speed <= 200){
        speedControl(speed+10);
      }
      break; 

    default:
      Serial.println("Invalid");
  }
}

void speedControl(int setSpeed) {
	// Turn on motors
	digitalWrite(in1, LOW);
	digitalWrite(in2, HIGH);
	digitalWrite(in3, LOW);
	digitalWrite(in4, HIGH);
	

	analogWrite(enA, setSpeed);
  analogWrite(enB, setSpeed);
  speed = setSpeed;
}
