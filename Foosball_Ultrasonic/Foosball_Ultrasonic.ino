/**
   Description: Uses the Arduino as a Slave sensor for both Red and Blue sensors. The Master takes in the inputs and decides what to do with them.
   Final Version: Does NOT send newline character at the end of payload.
*/
#include <Wire.h>
#include <stdio.h>

// defines pins numbers
const int trigPinRED = 8;
const int echoPinRED = 10;
const int trigPinBLUE = 11;
const int echoPinBLUE = 12;

int time = millis();

// distance
long durationRED;
int distanceRED;
long durationBLUE;
int distanceBLUE;

// serial print strings
String R = "R";
String B = " B";

void setup() {
  pinMode(trigPinRED, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPinRED, INPUT); // Sets the echoPin as an Input
  pinMode(trigPinBLUE, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPinBLUE, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication
}
void loop() {
  //red distance
  digitalWrite(trigPinRED, LOW);
  // Clears the trigPin  digitalWrite(trigPin, LOW);
  delayMicroseconds(1);
  digitalWrite(trigPinRED, HIGH);
  // Sets the trigPin on HIGH state for 10 micro seconds  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinRED, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  durationRED = pulseIn(echoPinRED, HIGH);
  // Calculating the distance
  distanceRED = (durationRED * 0.034) / 2;

  //blue distance
  digitalWrite(trigPinBLUE, LOW);
  // Clears the trigPin  digitalWrite(trigPin, LOW);
  delayMicroseconds(1);
  digitalWrite(trigPinBLUE, HIGH);
  // Sets the trigPin on HIGH state for 10 micro seconds  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinBLUE, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  durationBLUE = pulseIn(echoPinBLUE, HIGH);
  // Calculating the distance
  distanceBLUE = (durationBLUE * 0.034) / 2;
  
  //string formatting
  char send[10];
  sprintf(send, "R%04dB%04d", distanceRED, distanceBLUE);
  //print the payload
  Serial.print(send);
}
