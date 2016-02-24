#include <XBee.h>
#include <Printers.h>
#include <SoftwareSerial.h>
String message; //string that stores the incoming message
SoftwareSerial softser(10,11); //RX, TX

void setup()
{
  Serial.begin(9600); //set baud rate
  softser.begin(9600);
}

void loop()
{
  if(softser.available())
  {//while there is data available on the serial monitor
    Serial.print(char(softser.read()));//store string from serial command
  }
}
    
