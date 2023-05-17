const int DEADZONE = 50;

void setup() {
  Serial.begin(115200); // initialize serial communication at 9600 baud
  pinMode(2, INPUT_PULLUP); // set pin 2 as the button pin/input with internal pull-up resistor enabled
}

void loop() {
  int xVal = analogRead(A0); // read analog value from A0 pin
  int yVal = analogRead(A1); // read analog value from A1 pin

  xVal = 1023 - xVal; // invert x-axis

  // apply deadzone to x and y values
  if (xVal > 512 - DEADZONE && xVal < 512 + DEADZONE) {
    xVal = 512;
  }
  if (yVal > 512 - DEADZONE && yVal < 512 + DEADZONE) {
    yVal = 512;
  }

  // read state of pin 2 and set third value to 0 or 1
  int buttonState = digitalRead(2);
  if (buttonState == 0)
    buttonState+=1024;

  // print x, y, and button state values as a tuple
  Serial.print(xVal); // print x value
  Serial.print(", "); // print comma and space separator
  Serial.print(yVal); // print inverted y value to set origin at bottom left corner
  Serial.print(", "); // print comma and space separator
  Serial.print(buttonState-1); // print button state
  Serial.println(' ');



  delay(100); // wait for 100 milliseconds before reading again
}
