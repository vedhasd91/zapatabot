#include <TinyGPS++.h>
#include <Printers.h>
#include <XBee.h>
#include <SoftwareSerial.h>

#define BUFFER 80 
/*
   This sample code demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.
   It requires the use of SoftwareSerial, and assumes that you have a
   4800-baud serial GPS device hooked up on pins 4(rx) and 3(tx).
*/
static const int RXPin = 3, TXPin = 2;
static const int RXPin1 = 6, TXPin1 = 5;
static const uint32_t GPSBaud = 4800;
static const uint32_t ZbBaud = 9600;
char cmd[] = "LOC";
// The TinyGPS++ object
TinyGPSPlus gps;
//buffer for xbee frame
uint8_t payload[BUFFER] = {0};
// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);
SoftwareSerial zb(RXPin1, TXPin1);

char reply[BUFFER] = "";
char *data = "";

XBee xbee = XBee();
XBeeResponse response =XBeeResponse();

ZBRxResponse rx = ZBRxResponse();
// Specify the address of the remote XBee (this is the SH + SL)
XBeeAddress64 addr64  = XBeeAddress64(0x00000000,0x00000000);
  
void setup()
{
  Serial.begin(115200);
  ss.begin(GPSBaud);
  zb.begin(ZbBaud);
  xbee.setSerial(zb);
  Serial.println();
  Serial.println(F("Sats Latitude   Longitude     Alt    Distance   "));
  Serial.println(F("      (deg)      (deg)        (m)    to Charlotte   "));
  Serial.println(F("---------------------------------------------------------------------------------------------------------------------------------------"));  
}

void loop()
{  
  zb.listen();
  xbee.readPacket();
  if(xbee.getResponse().isAvailable()){
    //Very very IMP to check for identifier
    if(xbee.getResponse().getApiId()==ZB_RX_RESPONSE){
      xbee.getResponse().getZBRxResponse(rx);
      data = (char*)rx.getData();
      String rx = String(data);
      Serial.println(rx + " received");
      if(isSameAs(data,cmd)==0){
        ss.listen();
        smartDelay(500);
        printFloat(gps.location.lat(), gps.location.isValid(), 12, 6);
        //delay(1);
        printFloat(gps.location.lng(), gps.location.isValid(), 12, 6);
        //delay(1);
        printFloat(gps.altitude.meters(), gps.altitude.isValid(), 7, 2);
        //delay(1);
        charToBuf(reply,payload);
        ZBTxRequest zbTx = ZBTxRequest(addr64,payload, sizeof(payload));
        xbee.send(zbTx);
        data = "";
        reply[0]='\0';
      }
    }
  }
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
  /* unsigned long distanceKmToClt =
    (unsigned long)TinyGPSPlus::distanceBetween(
      gps.location.lat(),
      gps.location.lng(),
      CHARLOTTE_LAT, 
      CHARLOTTE_LON) / 1000;
  printInt(distanceKmToClt, gps.location.isValid(), 9);
  */
  Serial.println();
  
  if (millis() > 5000 && gps.charsProcessed() < 10)
    Serial.println(F("No GPS data received: check wiring"));
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
  char buf[50]={0};
  char delim[2]=",";
  if(!valid)
  {
    while (len-- > 1)
      Serial.print('*');
    reply[0] = '*';
    reply[1]='\0';
    Serial.print(' ');
  }
  else
  {
    Serial.print(val, prec);
    //sprintf(reply,"%f",val);
    dtostrf(val,7, prec, buf);
    strcat(buf,delim);
    strcat(reply,buf);
    /*int vi = abs((int)val);
    int flen = prec + (val < 0.0 ? 2 : 1); // . and -
    flen += vi >= 1000 ? 4 : vi >= 100 ? 3 : vi >= 10 ? 2 : 1;
    for (int i=flen; i<len; ++i)
      Serial.print(' ');*/
  }
  smartDelay(0);
}

/*
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

*/

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

static void charToBuf(char *str, uint8_t *payload){
  
  for(int i=0;i<BUFFER;i++){
    payload[i]=0x00;
  }
  for(int i=0;i<(strlen(str));i++){
    memcpy(&payload[i],&str[i],sizeof(str[i]));
  }
  
}

static int isSameAs(char *str1, char *str2){
 int i = strlen(str1);
 int j = strlen(str2);
 int k = 0;
 int l = 0;
 
 while( i && j ){
   if(!(str1[k++]==str2[l++]))
     return 1;
   i--;
   j--;
 }
 
 return 0;
 
}
   
  
