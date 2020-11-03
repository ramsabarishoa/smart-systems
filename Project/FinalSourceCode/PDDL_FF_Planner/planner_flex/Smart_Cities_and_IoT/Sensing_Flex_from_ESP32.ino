#include <ESP8266WiFi.h> 
#include <PubSubClient.h>

#define MAX_MSG_LEN (128)

// Wifi configuration
const char* ssid = "Meghana";
const char* password = "4eustchlan4";

const char *serverHostname = "test.mosquitto.org";
const char *topic = "flex_values";

const int FLEX_PIN = A0;
const float VCC = 4.98;
const float R_DIV = 47500.0;

const float STRAIGHT_RESISTANCE = 37300.0;
const float BEND_RESISTANCE = 90000.0;

char flex[10];

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

  Serial.begin(115200);
  pinMode(FLEX_PIN, INPUT);
  connectWifi();
  client.setServer(serverHostname, 1883);
  //client.setCallback(callback);
}

void loop() {
    if (!client.connected()) {
      connectMQTT();
    }
    // this is ESSENTIAL!
    client.loop();
    // idle
    delay(500);
    
    int flexADC = analogRead(FLEX_PIN);
    float flexV = flexADC * VCC / 1023.0;
    float flexR = R_DIV * (VCC / flexV - 1.0);
    Serial.println("Resistance: " + String(flexR) + " ohms");
    float angle = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE, 0, 90.0); Serial.println("Bend: " + String(angle) + " degrees");
    dtostrf(angle,7, 3,flex);
    Serial.print(flex);
    client.publish(topic,flex);
    Serial.println();
    delay(1000);
}

void connectWifi() {
  delay(10);
  // Connecting to a WiFi network
  Serial.printf("\nConnecting to %s\n", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected on IP address ");
  Serial.println(WiFi.localIP());
}

void connectMQTT() {
  while (!client.connected()) {
    String clientId = "ESP8266-";
    clientId += String(random(0xffff), HEX);
    Serial.printf("MQTT connecting as client %s...\n", clientId.c_str());
    if (client.connect(clientId.c_str())) {
      Serial.println("MQTT connected");
      client.subscribe(topic);
      //client.publish(topic, "hello from ESP8266");
    } else {
      Serial.printf("MQTT failed, state %s, retrying...\n", client.state());
      delay(2500);
    }
  }
}
