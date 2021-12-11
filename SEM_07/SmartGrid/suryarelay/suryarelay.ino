/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp8266-relay-module-ac-web-server/
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/

// Import required libraries
#include "ESPAsyncWebServer.h"

#include <PZEM004Tv30.h>
#include <ESP8266WiFi.h>
#include <HTTPSRedirect.h>
#include "DebugMacros.h"
#include <NTPClient.h>
#include <WiFiUdp.h>

// Set to true to define Relay as Normally Open (NO)
#define RELAY_NO    false

// Set number of relays
#define NUM_RELAYS  1


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

// Assign each GPIO to a relay
int relayGPIOs[NUM_RELAYS] = {5};//{5, 4, 14, 12, 13};

// Replace with your network credentials
//const char* ssid = "REPLACE_WITH_YOUR_SSID";
//const char* password = "REPLACE_WITH_YOUR_PASSWORD";

const char* PARAM_INPUT_1 = "relay";  
const char* PARAM_INPUT_2 = "state";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    html {font-family: Arial; display: inline-block; text-align: center;}
    h2 {font-size: 3.0rem;}
    p {font-size: 3.0rem;}
    body {max-width: 600px; margin:0px auto; padding-bottom: 25px;}
    .switch {position: relative; display: inline-block; width: 120px; height: 68px} 
    .switch input {display: none}
    .slider {position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; border-radius: 34px}
    .slider:before {position: absolute; content: ""; height: 52px; width: 52px; left: 8px; bottom: 8px; background-color: #fff; -webkit-transition: .4s; transition: .4s; border-radius: 68px}
    input:checked+.slider {background-color: #2196F3}
    input:checked+.slider:before {-webkit-transform: translateX(52px); -ms-transform: translateX(52px); transform: translateX(52px)}
  </style>
</head>
<body>
  <h2>ESP Web Server</h2>
  %BUTTONPLACEHOLDER%
<script>function toggleCheckbox(element) {
  var xhr = new XMLHttpRequest();
  if(element.checked){ xhr.open("GET", "/update?relay="+element.id+"&state=1", true); }
  else { xhr.open("GET", "/update?relay="+element.id+"&state=0", true); }
  xhr.send();
}</script>
</body>
</html>
)rawliteral";

// Replaces placeholder with button section in your web page
String processor(const String& var){
  //Serial.println(var);
  if(var == "BUTTONPLACEHOLDER"){
    String buttons ="";
    for(int i=1; i<=NUM_RELAYS; i++){
      String relayStateValue = relayState(i);
      buttons+= "<h4>Relay #" + String(i) + " - GPIO " + relayGPIOs[i-1] + "</h4><label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox(this)\" id=\"" + String(i) + "\" "+ relayStateValue +"><span class=\"slider\"></span></label>";
    }
    return buttons;
  }
  return String();
}

String relayState(int numRelay){
  if(RELAY_NO){
    if(digitalRead(relayGPIOs[numRelay-1])){
      return "";
    }
    else {
      return "checked";
    }
  }
  else {
    if(digitalRead(relayGPIOs[numRelay-1])){
      return "checked";
    }
    else {
      return "";
    }
  }
  return "";
}

void setup(){
  // Serial port for debugging purposes
  Serial.begin(9600);

  // Set all relays to off when the program starts - if set to Normally Open (NO), the relay is off when you set the relay to HIGH
  for(int i=1; i<=NUM_RELAYS; i++){
    pinMode(relayGPIOs[i-1], OUTPUT);
    if(RELAY_NO){
      digitalWrite(relayGPIOs[i-1], HIGH);
    }
    else{
      digitalWrite(relayGPIOs[i-1], LOW);
    }
  }
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  // Print ESP8266 Local IP Address
  Serial.println(WiFi.localIP());

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

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html, processor);
  });

  // Send a GET request to <ESP_IP>/update?relay=<inputMessage>&state=<inputMessage2>
  server.on("/update", HTTP_GET, [] (AsyncWebServerRequest *request) {
    String inputMessage;
    String inputParam;
    String inputMessage2;
    String inputParam2;
    // GET input1 value on <ESP_IP>/update?relay=<inputMessage>
    if (request->hasParam(PARAM_INPUT_1) & request->hasParam(PARAM_INPUT_2)) {
      inputMessage = request->getParam(PARAM_INPUT_1)->value();
      inputParam = PARAM_INPUT_1;
      inputMessage2 = request->getParam(PARAM_INPUT_2)->value();
      inputParam2 = PARAM_INPUT_2;
      if(RELAY_NO){
        Serial.print("NO ");
        digitalWrite(relayGPIOs[inputMessage.toInt()-1], !inputMessage2.toInt());
      }
      else{
        Serial.print("NC ");
        digitalWrite(relayGPIOs[inputMessage.toInt()-1], inputMessage2.toInt());
      }
    }
    else {
      inputMessage = "No message sent";
      inputParam = "none";
    }
    Serial.println(inputMessage + inputMessage2);
    request->send(200, "text/plain", "OK");
  });
  // Start server
  server.begin();
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

   if (isnan(volt)) {
    volt = 0;
    cur = 0;
    powe = 0;                                                                                               
    ener = 0;
    freq = 0;
    pf = 0;
  }
  
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

// Data Updating in spreadhseet
      client->connect(host, httpsPort);
      client->POST(url, host, payload, false);
  delay(500);
}
