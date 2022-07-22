#define btn1 3
#define btn2 5
#define btn3 6
#define btn4 9
void setup() {
  Serial.begin(9600);
  pinMode(btn1, INPUT);
  pinMode(btn2, INPUT);
  pinMode(btn3, INPUT);
  pinMode(btn4, INPUT);
  Serial.println(0);
}

void loop() {
  if (digitalRead(btn1) == HIGH)
  {
    Serial.println(1);
    delay(100);
  }
      else if (digitalRead(btn2) == HIGH)
  {
    Serial.println(2);
    delay(100);
  }
     else if (digitalRead(btn3) == HIGH)
  {
    Serial.println(3);
    delay(100);
  }
     else if (digitalRead(btn4) == HIGH)
  {
    Serial.println(4);
    delay(100);
  }
  else{
    Serial.println(0);
    delay(150);
  }
}
