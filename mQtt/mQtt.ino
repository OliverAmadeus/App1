// Creado ChepeCarlos de ALSW
// Tutorial Completo en https://nocheprogramacion.com
// Canal Youtube https://youtube.com/alswnet?sub_confirmation=1

#if defined(ESP32)

#include <WiFi.h>
#include <ESPmDNS.h>
#include <WebServer.h>
#include <Update.h>

WebServer server(80);

#elif defined(ESP8266)

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266mDNS.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

#endif


#include <HTTPClient.h>
#include <PubSubClient.h>
#include "data.h"

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
int value = 0;
int habilitar = 0;
int arreglo[16] = {1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18};
int values[16];
double promedio = 0;
int cont = 0;
const char* publishTopic = "kaworu/temp";     // Tópico para publicar
const char* message = "b'25','25','25','25','25','25','25','25','25','25'";   
const char* mqtt_user = ""; // Usuario, si es necesario
const char* mqtt_pass = ""; // Contraseña, si es necesario
void PaginaSimple() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/html", Pagina);
}

void ActualizarPaso1() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/plain", (Update.hasError()) ? "FAIL" : "OK");
  ESP.restart();
}

void ActualizarPaso2() {
  HTTPUpload& upload = server.upload();
  if (upload.status == UPLOAD_FILE_START) {
    Serial.setDebugOutput(true);
#if defined(ESP8266)
    WiFiUDP::stopAll();
#endif
    Serial.printf("Actualizanddo: %s\n", upload.filename.c_str());
    uint32_t maxSketchSpace = (ESP.getFreeSketchSpace() - 0x1000) & 0xFFFFF000;
    if (!Update.begin(maxSketchSpace)) {
      Update.printError(Serial);
    }
  } else if (upload.status == UPLOAD_FILE_WRITE) {
    if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
      Update.printError(Serial);
    }
  } else if (upload.status == UPLOAD_FILE_END) {
    if (Update.end(true)) {
      Serial.printf("Actualizacion Exitosa: %u\nReiniciando...\n", upload.totalSize);
    } else {
      Update.printError(Serial);
    }
    Serial.setDebugOutput(false);
  } else {
    Serial.printf("Problema con la Actualizacion (Talves problema con la coneccion); Estado=%d\n", upload.status);
  }
  yield();
}


void irradiancia(String &response) {
    int values[16];
    int arreglo[16] = { /* valores de los pines */ };
    float promedio = 0;

    // Leer los valores analógicos
    for (int i = 0; i < 16; i++) {
        values[i] = analogRead(arreglo[i]);
    }

    // Calcular el promedio
    for (int i = 0; i < 16; i++) {
        promedio += values[i];
    }
    promedio /= 16;

    // Construir la respuesta
    response = "";
    for (int i = 0; i < 16; i++) {
        response += "Valor " + String(i + 1) + ": " + String(values[i]) + "\n";
    }
    response += "Promedio: " + String(promedio);
}

void irradianciaPost() {
    String response;
    irradiancia(response);
    server.send(200, "text/plain", response);
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("Iniciando Servidor...");
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);
  if (WiFi.waitForConnectResult() == WL_CONNECTED) {
    MDNS.begin(nombre);
    server.on("/update", HTTP_GET, PaginaSimple);
    server.on("/actualizar", HTTP_POST, ActualizarPaso1, ActualizarPaso2);
    server.on("/irradiancia", irradianciaPost);
    server.begin();
    MDNS.addService("http", "tcp", 80);
    Serial.printf("Listo!\nAbre http://%s.local en navegador\n", nombre);
    Serial.print("o en la IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Eror en Wifi");
  }

  client.setServer(mqtt_server, 1883);


}

void loop() {

while(cont <= 6000){
  cont = cont+1;
  server.handleClient();
#if defined(ESP8266)
  MDNS.update();
#endif
  delay(2);
}

  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("ESP32", mqtt_user, mqtt_pass)) {
        Serial.println("Reconectado al servidor MQTT");
      } else {
        delay(5000);
      }
    }
  }

  client.loop(); // Asegúrate de que las funciones MQTT se ejecuten

  // Publicar un mensaje en un topic
  String response;
  irradiancia(response);
  client.publish("esp32/test", response.c_str()); 

  delay(5000); // Publicar cada 5 segundos
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado");
}



