const int sensorPin = A0;

int leituraAtual = 0;
int leituraAnterior = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {

  leituraAtual = analogRead(sensorPin);

  int derivada = leituraAtual - leituraAnterior;

  leituraAnterior = leituraAtual;

  Serial.print(leituraAtual);
  Serial.print(" ");
  Serial.println(derivada);

  delay(500);
}