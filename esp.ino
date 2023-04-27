
#include <ESP8266WiFi.h>

String apiKey = "Y2FRM1453YBHKQYF";     //  Enter your Write API key from ThingSpeak WBAC8OE213AX94FI

const char *ssid =  "jaseem iphone";
const char *pass =  "qwertyuio@";
const char* server = "api.thingspeak.com";

WiFiClient client;
String values, sensor_data;


void setup()
{
  Serial.begin(115200);
  delay(10);

  Serial.println("Connecting to ");     // replace with your wifi ssid and wpa2 key
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print("...");
  }
  Serial.println("");
  Serial.println("WiFi connected");

}
void loop() {
  bool Sr = false;
  while (Serial.available()) {
    sensor_data = Serial.readString();
    Sr = true;
  }
  delay(1000);
  if (Sr == true) {
    values = sensor_data;
    //get comma indexes from values variable
    int fristCommaIndex = values.indexOf(',');
    int secondCommaIndex = values.indexOf(',', fristCommaIndex + 1);
    int thirdCommaIndex = values.indexOf(',', secondCommaIndex + 1);
    int fourthCommaIndex = values.indexOf(',', thirdCommaIndex + 1);
    //get sensors data from values variable by  spliting by commas and put in to variables
    String difference = values.substring(0, fristCommaIndex);
    String flowRate = values.substring(fristCommaIndex + 1, secondCommaIndex);
    String flowRate1 = values.substring(secondCommaIndex + 1, thirdCommaIndex);
    String A = values.substring(thirdCommaIndex + 1, fourthCommaIndex);

    if (client.connect(server, 80))
    {
      String postStr = apiKey;
      postStr += "&field1=";
      postStr += String(difference);
      postStr += "&field2=";
      postStr += String(flowRate);
      postStr += "&field3=";
      postStr += String(flowRate1);
      postStr += "&field4=";
      postStr += String(A);
      postStr += "\r\n\r\n";

      client.print("POST /update HTTP/1.1\n");
      client.print("Host: api.thingspeak.com\n");
      client.print("Connection: close\n");
      client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
      client.print("Content-Type: application/x-www-form-urlencoded\n");
      client.print("Content-Length: ");
      client.print(postStr.length());
      client.print("\n\n");
      client.print(postStr);
      //Serial.println("%. Send to Thingspeak.");
    }
    client.stop();

    //Serial.println("Waiting...");
    // thingspeak needs minimum 15 sec delay between updates
    delay(1000);
  }
}
