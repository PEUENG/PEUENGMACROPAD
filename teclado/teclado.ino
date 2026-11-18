const int buttons[] = {2, 3, 4, 5, 6};
const int NUM_BUTTONS = 5;

int lastState[NUM_BUTTONS] = {
  HIGH, HIGH, HIGH, HIGH, HIGH
};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < NUM_BUTTONS; i++) {
    pinMode(buttons[i], INPUT_PULLUP);
  }
}

void loop() {
  for (int i = 0; i < NUM_BUTTONS; i++) {
    int currentState = digitalRead(buttons[i]);

    if (currentState == LOW && lastState[i] == HIGH) {
      delay(30);

      if (digitalRead(buttons[i]) == LOW) {
        Serial.println(i + 1);
      }
    }

    lastState[i] = currentState;
  }
}
