#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Objetos de los sensores
Adafruit_ADS1115 ads;             // ADC ADS1115
Adafruit_MPU6050 mpu;             // Acelerómetro MPU6050

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // Inicializar ADS1115
  if (!ads.begin()) {
    Serial.println("No se encontró el ADS1115. Verifica conexión.");
    while (1);
  }
  ads.setGain(GAIN_TWOTHIRDS);  // ±6.144 V

  // Inicializar MPU6050
  if (!mpu.begin()) {
    Serial.println("No se encontró el MPU6050. Verifica conexión.");
    while (1);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);   // ±2g (default)
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);        // ±250°/s (default)
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);     // Filtro digital

  Serial.println("Sensores inicializados correctamente.");
  Serial.println("Vpiezo ; AccelX ; AccelY ; AccelZ");
}

void loop() {
  int16_t raw_piezo = ads.readADC_Differential_0_1();
  float voltage_piezo = raw_piezo * 0.0001875;  // GAIN_TWOTHIRDS → 0.1875 mV/bit

  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  mpu.getEvent(&accel, &gyro, &temp);

  Serial.print(voltage_piezo, 4); // Multiplicado por dos por el divisor resistor
  Serial.print(";");
  Serial.print(accel.acceleration.x, 2);
  Serial.print(";");
  Serial.print(accel.acceleration.y, 2);
  Serial.print(";");
  Serial.print(accel.acceleration.z, 2);
  Serial.println("");
  
}
