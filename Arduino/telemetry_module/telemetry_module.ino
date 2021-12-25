#include <dht11.h>

//  Include the required libraries:
#include <Adafruit_Sensor.h>
#include <MQ2.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <SPI.h>
#include <MQ2.h>
#include <Adafruit_BMP280.h>


#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)

dht11 DHT11; // create object of DHT11
#define dhtpin 2 // set the pin to connect to DHT11

StaticJsonBuffer<200> jsonBuffer;
int pin = A2;
MQ2 mq2(pin);


Adafruit_BMP280 bmp; // I2C
//Adafruit_BMP280 bmp(BMP_CS); // hardware SPI
//Adafruit_BMP280 bmp(BMP_CS, BMP_MOSI, BMP_MISO,  BMP_SCK);

// Blick sensor pin
int blick = A0;
int led_pin_1 = 7;
int led_pin_2 = 4;
int threshold = 20;
int fan_pin = 8;
int threshold_temp = 20;
float lpg, co, smoke;
float temperature_g = 0;
float humidity_g = 0;
float pressure_g = 0;
float alt_g = 0;
String str;
int val_blick = 0;

void init_bmp280() {
  //if (!bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID)) {
  if (!bmp.begin()) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                      "try a different address!"));
    while (1) delay(10);
  }

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void get_threshold() {
  int str_len = 0;
  Serial.println("Read");
  while(Serial.available() == 0); 
  String str = Serial.readString();
  StaticJsonBuffer<500> jsonStringBuffer;
  JsonObject& jsonString = jsonStringBuffer.parseObject(str);
  threshold = jsonString["t1"];
  threshold_temp = jsonString["t2"];
  delay(1000);
}

void setup() {

  Serial.begin(9600);
  get_threshold();
  mq2.begin();
  init_bmp280();
  pinMode(led_pin_1, OUTPUT);
  pinMode(led_pin_2, OUTPUT);
  delay(1000);
}

void check_lights() {
  val_blick = analogRead(A0);
  if (val_blick < threshold) {
     digitalWrite(led_pin_1, HIGH);
     digitalWrite(led_pin_2, HIGH);
  }
  else {
     digitalWrite(led_pin_1, LOW);
     digitalWrite(led_pin_2, LOW);
  }

  delay(1000);
}

boolean isValidNumber(String str){
  for(byte i=0;i<str.length();i++) {
    if(isDigit(str.charAt(i))) return true;
  }
  return false;
}

void get_bpm280() {

   temperature_g = bmp.readTemperature();
   pressure_g = bmp.readPressure();
   alt_g = bmp.readAltitude(1013.25);
   delay(2000);
}

void get_mq2() {
  float* values= mq2.read(false); //set it false if you don't want to print the values to the Serial
  
  lpg = values[0];
  co = values[1];
  smoke = values[2];  
  delay(1000);
}

void check_fan() {
  if (temperature_g > threshold_temp) {
    digitalWrite(fan_pin, HIGH);
  } else {
    digitalWrite(fan_pin, LOW);
  }
}

void get_dht11() {
  DHT11.read(dhtpin);// initialize the reading
  humidity_g = DHT11.humidity;// get humidity
  delay(1000);
}

void loop() {
  JsonObject& root = jsonBuffer.createObject();
  get_mq2();
  get_bpm280();
  get_dht11();
  check_fan();

  root["temperature"] = temperature_g;
  root["pressure"] = pressure_g;
  root["humidity"] = humidity_g;  
  root["altitude"] = alt_g;
  root["lpg"] = lpg;
  root["co"] = co;
  root["smoke"] = smoke;
  delay(1000);
  root.printTo(Serial);
  Serial.println();
}
