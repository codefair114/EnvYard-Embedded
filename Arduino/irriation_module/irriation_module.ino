// Include the required libraries:

// Include Sensor library
#include <Adafruit_Sensor.h>
// Include JSON library
#include <ArduinoJson.h>
// Include the Servo library 
#include <Servo.h> 

// Declare the Servo pins
int servoPin_1_1 = 3;
int servoPin_1_2 = 5;
int servoPin_2_1 = 6;
int servoPin_2_2 = 9;

// Create a servo objects 
Servo Servo_1_1;
Servo Servo_1_2;
Servo Servo_2_1;
Servo Servo_2_2;

// Signal from the capacitive soil moisture sensors
int sensor_pin_1_1 = A0;
int sensor_pin_1_2 = A1;
int sensor_pin_2_1 = A2;
int sensor_pin_2_2 = A3;

// Digital pins where the relay is plugged in
int pump_1_1 = 4;
int pump_1_2 = 7;
int pump_2_1 = 8;
int pump_2_2 = 12;

// Threshold value to trigger pumps
int threshold_1 = 5;
int threshold_2 = 5;

StaticJsonBuffer<200> jsonBuffer;

void get_threshold() {
  int str_len = 0;
  Serial.println("Read");
  while(Serial.available() == 0); 
  String str = Serial.readString();
  StaticJsonBuffer<500> jsonStringBuffer;
  JsonObject& jsonString = jsonStringBuffer.parseObject(str);
  threshold_1 = jsonString["t1"];
  threshold_2 = jsonString["t2"];
  //Serial.println(threshold_1);
  //Serial.println(threshold_2);
  delay(1000);
}

void setup() {
  Serial.begin(9600);
  delay(1000);
  get_threshold();
  // Setup for the soil moisture sensors
  pinMode(sensor_pin_1_1, INPUT);  
  pinMode(sensor_pin_1_2, INPUT);  
  pinMode(sensor_pin_2_1, INPUT);  
  pinMode(sensor_pin_2_2, INPUT);

  // Setup for water pumps
  pinMode(pump_1_1, OUTPUT);
  pinMode(pump_1_2, OUTPUT);
  pinMode(pump_2_1, OUTPUT);
  pinMode(pump_2_2, OUTPUT);
  digitalWrite(pump_1_1, LOW);
  digitalWrite(pump_1_2, LOW);
  digitalWrite(pump_2_1, LOW);
  digitalWrite(pump_2_2, LOW);

  // Assign servo to pin
  Servo_1_1.attach(servoPin_1_1);
  Servo_1_2.attach(servoPin_1_2);
  Servo_2_1.attach(servoPin_2_1);
  Servo_2_2.attach(servoPin_2_2);

  delay(1000);  //1 second delay
}

void start_servo(Servo Servo_n) {
   //Serial.println("servo on");
   // Make servo go to 0 degrees 
   Servo_n.write(0); 
   delay(1000); 
   // Make servo go to 90 degrees 
   Servo_n.write(90); 
   delay(1000); 
   // Make servo go to 180 degrees 
   Servo_n.write(180); 
   delay(1000);
   //Serial.println("servo off");

}

int control_moisture_water(int sensor_pin, int pump, int threshold, Servo Servo_n) {
  
  int output_value = analogRead(sensor_pin);     //gets the value from the soil moisture sensor
  output_value = map(output_value,550,0,0,100); // this sets the percentage value
  
  delay(10000);
  // If the soil is try then pump out water for 1 second
  if (output_value < threshold) {
    // Start servo first
    start_servo(Servo_n);
    //Serial.println("pump on");
    digitalWrite(pump, HIGH);
    delay(1000);  //run pump for 1 second;
    digitalWrite(pump, LOW);
    //Serial.println("pump off");
    delay(1000); //wait 1 second 
  }
  else {
    digitalWrite(pump, LOW);
    Serial.println("pump off");
    delay(1000); //wait 5 minutes
  }

  return output_value;
}

boolean isValidNumber(String str){
  for(byte i=0;i<str.length();i++) {
    if(isDigit(str.charAt(i))) return true;
  }
  return false;
}

void loop() {
  JsonObject& root = jsonBuffer.createObject();
  int moisture;
  digitalWrite(pump_1_1, LOW);
  digitalWrite(pump_1_2, LOW);
  digitalWrite(pump_2_1, LOW);
  digitalWrite(pump_2_2, LOW);
  delay(1000);

  moisture = control_moisture_water(sensor_pin_1_1, pump_1_1, threshold_1, Servo_1_1);
  root["moisture_1_1"] = moisture;
  
  moisture = control_moisture_water(sensor_pin_1_2, pump_1_2, threshold_1, Servo_1_2);
  root["moisture_1_2"] = moisture;
  
  moisture = control_moisture_water(sensor_pin_2_1, pump_2_1, threshold_2, Servo_2_1);
  root["moisture_2_1"] = moisture;
  
  moisture = control_moisture_water(sensor_pin_2_2, pump_2_2, threshold_2, Servo_2_2);
  root["moisture_2_2"] = moisture;

  root.printTo(Serial);

  Serial.println();
  delay(1000);

}
