// ======================================================
// PROJETO PIBIC - LEI DE FARADAY E LENZ
// UESPI - Física
//
// Objetivo:
// Ler o sinal induzido na bobina utilizando o Arduino
// e calcular a derivada discreta do sinal.
//
// A derivada discreta aproxima a taxa de variação
// temporal da tensão induzida.
//
// Quanto mais rápido o fluxo magnético varia,
// maior será a f.e.m. induzida.
//
// Equação relacionada:
//
//      E = -N(dΦ/dt)
//
// ======================================================


// Pino analógico conectado à bobina
const int sensorPin = A0;


// Variável da leitura atual do sinal
int leituraAtual = 0;


// Variável da leitura anterior
int leituraAnterior = 0;



void setup() {

  // Inicializa comunicação serial
  // Baudrate alto para aquisição rápida
  Serial.begin(115200);

}



void loop() {

  // ==========================================
  // LEITURA DO SINAL ANALÓGICO
  // ==========================================

  // Lê tensão da bobina
  // Valores entre 0 e 1023
  leituraAtual = analogRead(sensorPin);



  // ==========================================
  // DERIVADA DISCRETA
  // ==========================================

  // Aproximação da derivada:
  //
  // dV/dt ≈ V(n) - V(n-1)
  //
  // Isso mede o quanto o sinal mudou
  // entre duas amostras consecutivas.
  //
  // Quanto maior a variação,
  // maior a indução eletromagnética.
  //
  int derivada = leituraAtual - leituraAnterior;



  // ==========================================
  // ATUALIZA LEITURA ANTERIOR
  // ==========================================

  // Armazena valor atual
  // para próxima iteração
  leituraAnterior = leituraAtual;



  // ==========================================
  // ENVIO SERIAL
  // ==========================================

  // Envia:
  //
  // leituraAtual derivada
  //
  // Exemplo:
  // 512 3
  // 520 8
  // 490 -30
  //
  // O Python irá separar os dois valores.
  //

  Serial.print(leituraAtual);

  // Espaço separador
  Serial.print(" ");

  // Envia derivada
  Serial.println(derivada);



  // ==========================================
  // CONTROLE DA TAXA DE AMOSTRAGEM
  // ==========================================

  // Delay pequeno para captar
  // variações rápidas do campo magnético.
  //
  // Valores muito altos fazem
  // o Arduino perder os picos.
  //
  delay(2);

}