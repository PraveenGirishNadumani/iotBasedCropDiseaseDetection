// Thingspeak  
String myAPIkey = "ROHTVUQJWEICYR64";  

#include <SoftwareSerial.h>
#include <dht.h>;
SoftwareSerial ESP8266(2, 3); // Rx,  Tx
/* DHT SENSOR SETUP */


#define DHTPIN  A0
#define S0 4
#define S1 5
#define S2 6
#define S3 8
#define sensorOut 9

dht DHT;
//dht dht(DHTPIN, DHTTYPE,11);
int humidity, temperature;
int frequency = 0;
int colorRed,colorGreen,colorBlue;  
long writingTimer = 50; 
long startTime = 0;
long waitTime = 0;


boolean relay1_st = false; 
boolean relay2_st = false; 
unsigned char check_connection=0;
unsigned char times_check=0;
boolean error;

void setup()
{
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);
  Serial.begin(9600); 
  ESP8266.begin(9600); 
  DHT.read11(DHTPIN);
  startTime = millis(); 
  ESP8266.println("AT+RST");
  delay(2000);
  Serial.println("Connecting to Wifi");
   while(check_connection==0)
  {
    Serial.print(".");
  ESP8266.print("AT+CWJAP=\"12345678\",\"12345678\"\r\n");
  ESP8266.setTimeout(5000);
 if(ESP8266.find("WIFI CONNECTED\r\n")==1)
 {
 Serial.println("WIFI CONNECTED");
 break;
 }
 times_check++;
 if(times_check>3) 
 {
  times_check=0;
   Serial.println("Trying to Reconnect..");
  }
  }
    digitalWrite(S0,HIGH);
    digitalWrite(S1,LOW);
}

void loop()
{
  waitTime = millis()-startTime;   
  if (waitTime > (writingTimer*100)) 
  {
    readSensors();
    writeThingSpeak();
    printData();
    startTime = millis();   
  }
}


void readSensors(void)
{
    humidity = DHT.humidity;
    temperature = DHT.temperature;
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
    colorRed = pulseIn(sensorOut, LOW);
    
    digitalWrite(S2,HIGH);
    digitalWrite(S3,HIGH);
    colorGreen = pulseIn(sensorOut, LOW);

    digitalWrite(S2, LOW);
    digitalWrite(S3, HIGH);
    colorBlue = pulseIn(sensorOut, LOW);    
    
}


void writeThingSpeak(void)
{
  startThingSpeakCmd();
  // preparacao da string GET
  String getStr = "GET /update?api_key=";
  getStr += myAPIkey;
  getStr +="&field1=";
  getStr +=String(colorRed);
  getStr +="&field2=";
  getStr +=String(colorGreen);
  getStr +="&field3=";
  getStr +=String(colorBlue);
  getStr +="&field4=";
  getStr += String(temperature);
  getStr +="&field5=";
  getStr += String(humidity);
  getStr += "\r\n\r\n";
  GetThingspeakcmd(getStr); 
  Serial.println("data uploaded");
}

void startThingSpeakCmd(void)
{
  ESP8266.flush();
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += "184.106.153.149"; // api.thingspeak.com IP address
  cmd += "\",80";
  ESP8266.println(cmd);
  Serial.print("Start Commands: ");
  Serial.println(cmd);
 

  if(ESP8266.find("Error"))
  {
    Serial.println("AT+CIPSTART error");
    return;
  }
}

void printData(void)
{
  Serial.print("colorRed:");
  Serial.println(colorRed);
  Serial.print("colorGreen:");
  Serial.println(colorGreen);
  Serial.print("colorBlue:");
  Serial.println(colorBlue);
  Serial.print("temperature=");
  Serial.print(temperature);
  Serial.print("  humidity=");
  Serial.println(humidity);
}

String GetThingspeakcmd(String getStr)
{
  String cmd = "AT+CIPSEND=";
  cmd +=String(getStr.length());
  ESP8266.println(cmd);
  Serial.println(cmd);
  delay(5000);
  Serial.println(ESP8266.println(cmd));
   Serial.println(ESP8266.find(">"));

  if(ESP8266.find("<"))
  {
    ESP8266.print(getStr);
    Serial.println(getStr);
    delay(50);
    String messageBody = "";
    while (ESP8266.available()) 
    {
      String line = ESP8266.readStringUntil('\n');
      if (line.length() == 1) 
      { 
        messageBody = ESP8266.readStringUntil('\n');
      }
    }
    Serial.print("MessageBody received: ");
    Serial.println(messageBody);
    return messageBody;
  }
  else
  {
    ESP8266.println("AT+CIPCLOSE");     
    Serial.println("AT+CIPCLOSE"); 
  } 
}
