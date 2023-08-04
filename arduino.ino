String message;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() {

  if (Serial.available() > 0) {
      message = Serial.readString();
      message.trim();

      if (message.equals("ping")) {
        Serial.println("pong");
      } else {
        Serial.println(message);
      }
  }

  // delay(100);
  // Serial.println("time to go");

}