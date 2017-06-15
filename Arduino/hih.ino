#include <Wire.h>

const uint8_t sensor = 0x27;

uint8_t meas[4];

uint8_t status;
uint16_t _temperature;
uint16_t _humidity;

int temperature;
int humidity;

void setup()
{
  Wire.begin();
  Serial.begin(9600);
}

void loop()
{ 
  do {
    measure();
  } while (status != 0); // Status 1 means stale data.
  
  String msg = "Temperature:\t" + (String)temperature + "\nHumidity:\t" + (String)humidity + "\n";
  Serial.print(msg);
  
  delay(1000);
}

void measure()
{
  Wire.beginTransmission(sensor);
  Wire.endTransmission();
  
  // Datasheet says the measurement cycle is ~36.65ms
  delay(50);
  
  Wire.requestFrom((int)sensor, 4);
  
  while (Wire.available() == 0);

  meas[0] = Wire.read();
  meas[1] = Wire.read();
  meas[2] = Wire.read();
  meas[3] = Wire.read();
  
  Wire.endTransmission();
  
  status = meas[0] >> 6;
  _humidity = (uint16_t)(((meas[0] & 0x3f) << 8) | meas[1]);
  _temperature = (uint16_t)((meas[2] << 6) | (meas[3] >> 2));
  
  humidity = (float)_humidity / (pow(2, 14) - 2) * 100;
  temperature = (float)_temperature / (pow(2, 14) - 2) * 165 - 40;
}
