#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <Adafruit_Sensor.h>

// Objeto del ADC
Adafruit_ADS1115 ads;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // Inicializar ADS1115
  if (!ads.begin()) {
    Serial.println("No se encontró el ADS1115. Verifica conexión.");
    while (1);
  }

  // Configurar ganancia para ±6.144 V (0.1875 mV por bit)
  ads.setGain(GAIN_TWOTHIRDS);
}

void loop() {
  // Leer A1 respecto a GND (modo no diferencial)
  int16_t raw_piezo = ads.readADC_SingleEnded(0);  // Canal 1 → A1
  int16_t raw_res = ads.readADC_SingleEnded(1);  // Canal 1 → A3


  // Convertir a voltaje (0.1875 mV/bit para GAIN_TWOTHIRDS)
  float voltage_piezo = raw_piezo * 0.0001875;
  float voltage_res = raw_res * 0.0001875;


  Serial.print(voltage_piezo, 4);  // Imprimir voltaje con 4 decimales
  Serial.print(",");
  Serial.print(voltage_res,4);
  Serial.println("");

  delay(500);
}
