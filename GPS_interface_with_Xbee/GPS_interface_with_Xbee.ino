#include <Printers.h>
#include <XBee.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
/*
   This sample code demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.
   It requires the use of SoftwareSerial, and assumes that you have a
   4800-baud serial GPS device hooked up on pins 4(rx) and 3(tx).
*/
static const int RXPin = 2, TXPin = 3;
static const int RXPin1 = 6, TXPin1 = 5;
static const uint32_t GPSBaud = 4800;
static const uint32_t ZbBaud = 9600;


// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);
SoftwareSerial zb(RXPin1, TXPin1);

XBee xbee = XBee();
XBeeResponse response =XBeeResponse();

ZBRxResponse rx = ZBRxResponse();
uint8_t payload[] = {'H','i'};

  // Specify the address of the remote XBee (this is the SH + SL)
  XBeeAddress64 addr64  = XBeeAddress64(0x00000000,0x00000000);
  // Create a TX Request
  ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
void setup()
{
  Serial.begin(115200);
  ss.begin(GPSBaud);
  zb.begin(ZbBaud);
  xbee.setSerial(zb);
  Serial.println();
  Serial.println(F("Sats Latitude   Longitude    Alt    Distance     Checksum"));
  Serial.println(F("      (deg)      (deg)       (m)  to Charlotte     Fail"));
  Serial.println(F("---------------------------------------------------------------------------------------------------------------------------------------"));




  
}

void loop()
{/*
  xbee.readPacket();
  
  if(xbee.getResponse().isAvailable()){
    xbee.getResponse().getZBRxResponse(rx);
    char* data = (char*)rx.getData();
    Serial.println(data);
  }
*/
  

  // Send your request
  xbee.send(zbTx);
  Serial.println("Sent..");
  delay(1000);
  
/*
  static const double CHARLOTTE_LAT = 35.3281765, CHARLOTTE_LON = -80.7821989;

  printInt(gps.satellites.value(), gps.satellites.isValid(), 5);
   Serial.print(",");
  printFloat(gps.location.lat(), gps.location.isValid(), 11, 6);
  Serial.print(",");
  printFloat(gps.location.lng(), gps.location.isValid(), 12, 6);
  Serial.print(",");
  printFloat(gps.altitude.meters(), gps.altitude.isValid(), 7, 2);
  Serial.print(",");

  unsigned long distanceKmToClt =
    (unsigned long)TinyGPSPlus::distanceBetween(
      gps.location.lat(),
      gps.location.lng(),
      CHARLOTTE_LAT, 
      CHARLOTTE_LON) / 1000;
  printInt(distanceKmToClt, gps.location.isValid(), 9);

  Serial.println();
  
  smartDelay(1000);

  if (millis() > 5000 && gps.charsProcessed() < 10)
    Serial.println(F("No GPS data received: check wiring"));
    */
}

//*****************************************************************************************
// This custom version of delay() ensures that the gps object
// is being "fed".
static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (ss.available())
      gps.encode(ss.read());
  } while (millis() - start < ms);
}

static void printFloat(float val, bool valid, int len, int prec)
{
  if (!valid)
  {
    while (len-- > 1)
      Serial.print('*');
    Serial.print(' ');
  }
  else
  {
    Serial.print(val, prec);
    int vi = abs((int)val);
    int flen = prec + (val < 0.0 ? 2 : 1); // . and -
    flen += vi >= 1000 ? 4 : vi >= 100 ? 3 : vi >= 10 ? 2 : 1;
    for (int i=flen; i<len; ++i)
      Serial.print(' ');
  }
  smartDelay(0);
}

static void printInt(unsigned long val, bool valid, int len)
{
  char sz[32] = "*****************";
  if (valid)
    sprintf(sz, "%ld", val);
  sz[len] = 0;
  for (int i=strlen(sz); i<len; ++i)
    sz[i] = ' ';
  if (len > 0) 
    sz[len-1] = ' ';
  Serial.print(sz);
  smartDelay(0);
}

static void printDateTime(TinyGPSDate &d, TinyGPSTime &t)
{
  if (!d.isValid())
  {
    Serial.print(F("********** "));
  }
  else
  {
    char sz[32];
    sprintf(sz, "%02d/%02d/%02d ", d.month(), d.day(), d.year());
    Serial.print(sz);
  }
  
  if (!t.isValid())
  {
    Serial.print(F("******** "));
  }
  else
  {
    char sz[32];
    sprintf(sz, "%02d:%02d:%02d ", t.hour(), t.minute(), t.second());
    Serial.print(sz);
  }

  printInt(d.age(), d.isValid(), 5);
  smartDelay(0);
}

static void printStr(const char *str, int len)
{
  int slen = strlen(str);
  for (int i=0; i<len; ++i)
    Serial.print(i<slen ? str[i] : ' ');
  smartDelay(0);
}
