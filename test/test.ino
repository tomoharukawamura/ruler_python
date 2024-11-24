#include <Arduino.h>

int val = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Hello World");
}

void loop() {
  val++;
  if (val == 15) {
    Serial.println("finish_loop");
  } else if (val % 2 ==0) {
    Serial.println(val);
  } else {
    Serial.println("None");
  }
  delay(1000);
}