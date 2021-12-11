#include <PZEM004Tv30.h>
#include <ESP8266WiFi.h>
#include <HTTPSRedirect.h>
#include "DebugMacros.h"
#include <NTPClient.h>
#include <WiFiUdp.h>



//**************************PZEM connection pins*********************************
PZEM004Tv30 pzem(12,13); // pzem(rx,tx) 12=D6,13=D7, esp(tx,rx)                                                                                                                                   are connected to (TX,RX) of PZEM module

//************************ Variables corresponding to NTP for timestamps*********
const long utcOffsetInSeconds = 0;
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);
float date_time;

//******Declaration of global variables******************
String sheetTime = "";
String sheetvolt = "";
String sheetcur  = "";
String sheetpowe = "";
String sheetener = "";
String sheetfreq = "";
String sheetpf   = ""; 

// *****************************WiFi SSID and Password***************************
const char* ssid = "dlink_DWR-111";                
const char* password = "1234567890";
//*******************************************************************************

// *****************************Spreadsheet initialization variables*************
const char* host = "script.google.com";
// Google script ID - from publish menu > deploy window
const char* GScriptId = "AKfycbxMPaSs1yP3Xo3Qv-g3TpKIPHgbsKLscENezKRbLYuW84TqVhklGyLj7gJlD9pPbZs";  
const int httpsPort = 443; 
String url = String("/a/iith.ac.in/macros/s/") + GScriptId + "/exec?value=Time";   

// temp_data is the sheet name
String payload_base =  "{\"command\": \"appendRow\", \   
                    \"sheet_name\": \"K45\", \
                       \"values\": "; 
String payload = "";

// PZEM module (with ESP) is the client - Google spreadsheet is the server
HTTPSRedirect* client = nullptr;  

void setup() {
  Serial.begin(9600);
  //***************************** Wifi connecting ******************************
  Serial.print("Connecting to wifi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");  
  }

  //************ Use HTTPSRedirect class to create a new TLS connection**********
  client = new HTTPSRedirect(httpsPort);
  client->setInsecure();
  client->setPrintResponseBody(true);
  client->setContentTypeHeader("application/json");
  Serial.print("Connecting to ");
  Serial.println(host);          //try to connect with "script.google.com"

  //************ Try to connect for a maximum of 5 times then exit
  bool flag = false;
  for (int i = 0; i < 5; i++) {
    int retval = client->connect(host, httpsPort);
    if (retval == 1) {
      flag = true;
      break;
    }
    else
      Serial.println("Connection failed. Retrying...");
  }

  client->GET(url, host);

  // detecting the current time
  timeClient.begin(); // NTP Time client for date and time
}

void loop() {
  timeClient.update();
  date_time=timeClient.getEpochTime(); // Fetch Epoch time from NTP
  
  float volt = pzem.voltage();
  float cur = pzem.current();
  float powe = pzem.power();
  float ener = pzem.energy();
  float freq = pzem.frequency();
  float pf = pzem.pf();

  static int error_count = 0;
  static int connect_count = 0;
  const unsigned int MAX_CONNECT = 20;
  static bool flag = false;

// Data formatting for sending data to strings spreadsheet
  sheetTime = String(date_time);
  sheetvolt = String(volt);
  sheetcur  = String(cur);
  sheetpowe = String(powe);
  sheetener = String(ener);
  sheetfreq = String(freq);
  sheetpf   = String(pf); 
  payload = payload_base+"\"" +sheetTime +"," + sheetvolt + ","+sheetcur+","+sheetpowe+","+sheetener+","+sheetfreq+","+ sheetpf + "\"}";
  Serial.println(payload);

  if (isnan(volt)) {
    volt = 0;
    cur = 0;
    powe = 0;                                                                                               
    ener = 0;
    freq = 0;
    pf = 0;
  }
// Data Updating in spreadhseet
      client->connect(host, httpsPort);
      client->POST(url, host, payload, false);
  delay(500);
}
