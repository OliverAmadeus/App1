#if defined(ESP32)

#include <WiFi.h>
#include <WiFiMulti.h>
#include <ESPmDNS.h>
#include <WebServer.h>
#include <Update.h>
WiFiMulti wifiMulti;
WebServer server(80);

#elif defined(ESP8266)

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266mDNS.h>
#include <ESP8266WebServer.h>

ESP8266WiFiMulti wifiMulti;
ESP8266WebServer server(80);

#endif
#include "data.h"
#include <Wire.h>

const uint32_t TiempoEsperaWifi = 5000;


const int bitPins[] = {25, 26, 27, 4, 16, 17, 5, 18}; // Define los pines digitales de salida
//const int bitPins[] = {38, 38, 38, 38, 38, 38, 38, 38}; // Define los pines digitales de salida
int decimalNumber = 255; // El número decimal de 8 bits que deseas convertir

int val = 255;
int sen1 = 33;
int sen = 0;

int pwmPin = 12;//12
int pwmPin1 = 14;//14
int pwmValue = 0;
int pwmValue1 = 0;
///////////////////////////////////
int pino_sensor = 34;
int menor_valor;
int valor_lido;
int menor_valor_acumulado = 0;
int ZERO_SENSOR = 0;
float corrente_pico;
float corrente_eficaz;
double maior_valor=0;
double corrente_valor=0;

  float sensibilidad=0.66; //Ajuste de la sensibilidad para sensor de 30 Amperes
  float I=0.00;
  float ajuste = 0.05;
////////////////////////////////////
int pino_sensorv = 32;
int valor_voltaje = 0;
int voltaje = 0;
////////////////////////7
void handleSetPWM() {
  if (server.hasArg("pwmValue")) {
    pwmValue = server.arg("pwmValue").toInt();
    ledcWrite(0, pwmValue);
  }
  server.send(200, "text/plain", "PWM Value set to: " + String(pwmValue));
}
void mensajePwm() {
  String  response = "<html><body>";
  response += "<form method='POST' action='/setPWM'>";
  response += "Valor PWM: <input type='number' name='pwmValue' min='0' max='255' value='" + String(pwmValue) + "'><br>";
  response += "<input type='submit' value='Enviar'>";
  response += "</form>";
  response += "</body></html>";
  server.send(200, "text/html", response);  
}


void mensajeBase() {
 // server.send(200, "text/plain", "Hola desde el ESP");
  
  int value1 = sen;
  int value2 = menor_valor;
  int value3 = valor_voltaje;
  int value4 = val;

    float value5 = corrente_pico;

  float value6 = I;
 
  String response = String(value1) + "," + String(value2)+ "," +String(value3) + "," + String(value4) + String(value5)+ "," + String(value6); 
  server.send(200,"text/plain",response);


}


void PaginaSimple() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/html", Pagina);
}

void PaginaSimple1() {
  IPAddress localIP = WiFi.localIP();
  String iplocal = String(localIP[0]) + "." + String(localIP[1]) + "." + String(localIP[2]) + "." + String(localIP[3]);              
  server.send(200, "text/plain", iplocal );
}

void ActualizarPaso1() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/html", (Update.hasError()) ? "FAIL" : "OK");
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


void setup() {
  Serial.begin(115200);
    for (int i = 0; i < 8; i++) {
    pinMode(bitPins[i], OUTPUT); // Configura los pines como salidas
  }
  delay(200);
  Serial.println("Iniciando Servidor...");
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);
  if (WiFi.waitForConnectResult() == WL_CONNECTED) {
    MDNS.begin(nombre);
    server.on("/", mensajeBase);
    server.on("/update", HTTP_GET, PaginaSimple);
    server.on("/actualizar", HTTP_POST, ActualizarPaso1, ActualizarPaso2);
    server.on("/valor", PaginaSimple1);
    server.begin();
    MDNS.addService("http", "tcp", 80);
    Serial.printf("Listo!\nAbre http://%s.local en navegador\n", nombre);
    Serial.print("o en la IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Eror en Wifi");
  }

  pinMode(pwmPin, OUTPUT);
  int frecuencia = 10000; // 10 kHz
  int resolucion = 8;     // Resolución de 8 bits (0-255)
  ledcSetup(0, frecuencia, resolucion);


  // Asocia el canal PWM con el pin
  ledcAttachPin(pwmPin, 0);
  ledcAttachPin(pwmPin1, 1);

    pinMode(pino_sensor,INPUT);
delay(3000);
 //Fazer o AUTO-ZERO do sensor
Serial.println("Fazendo o Auto ZERO do Sensor...");
 /*
 ZERO_SENSOR = analogRead(pino_sensor); 
 for(int i = 0; i < 10000 ; i++){
 valor_lido = analogRead(pino_sensor); 
 ZERO_SENSOR = (ZERO_SENSOR +  valor_lido)/2; 
 delayMicroseconds(1);  
 }
 Serial.print("Zero do Sensor:");
 Serial.println(ZERO_SENSOR);
 delay(3000);

 */
menor_valor = 4095;
 
  for(int i = 0; i < 10000 ; i++){
  valor_lido = analogRead(pino_sensor);
  if(valor_lido < menor_valor){
  menor_valor = valor_lido;    
  }
  delayMicroseconds(1);  
  }
  ZERO_SENSOR = menor_valor; //2883
  Serial.print("Zero do Sensor:");
  Serial.println(ZERO_SENSOR);
  delay(3000);

  pinMode(pino_sensor,INPUT);



}

void loop() {
  server.handleClient();

#if defined(ESP8266)
  MDNS.update();
#endif
sen = analogRead(sen1);

//if (sen < 1015 && val > 0 ){
if (sen < 1015 && val > 0 ){
  val = val - 1;
}

//if (sen > 1020 && val < 255 ){
if (sen > 1020 && val < 255 ){
  val = val + 1;
}
  decimalNumber =  val;
  ledcWrite(1, 63);
  digitalWrite(bitPins[0], (decimalNumber & 0x01)); // Establece el valor del primer pin
  digitalWrite(bitPins[1], (decimalNumber & 0x02) >> 1); // Establece el valor del segundo pin
  digitalWrite(bitPins[2], (decimalNumber & 0x04) >> 2); // Establece el valor del tercer pin
  digitalWrite(bitPins[3], (decimalNumber & 0x08) >> 3); // Establece el valor del cuarto pin
  digitalWrite(bitPins[4], (decimalNumber & 0x10) >> 4); // Establece el valor del quinto pin
  digitalWrite(bitPins[5], (decimalNumber & 0x20) >> 5); // Establece el valor del sexto pin
  digitalWrite(bitPins[6], (decimalNumber & 0x40) >> 6); // Establece el valor del séptimo pin
  digitalWrite(bitPins[7], (decimalNumber & 0x80) >> 7); // Establece el valor del octavo pin
Serial.println(sen);
Serial.println(decimalNumber);

delay(100);



  menor_valor = 4095;
 
  for(int i = 0; i < 1600 ; i++){
  valor_lido = analogRead(pino_sensor);
  if(valor_lido < menor_valor){
  menor_valor = valor_lido;    
  }
  delayMicroseconds(10);  
  }

  
  Serial.print("Menor Valor:");
  Serial.println(menor_valor);

  //Transformar o maior valor em corrente de pico
  corrente_pico = ZERO_SENSOR - menor_valor; // Como o ZERO do sensor é 2,5 V, é preciso remover este OFFSET. Na leitura Analógica do ESp32 com este sensor, vale 2800 (igual a 2,5 V).
  corrente_pico = corrente_pico*0.805; // A resolução mínima de leitura para o ESp32 é de 0.8 mV por divisão. Isso transforma a leitura analógica em valor de tensão em [mV}
  corrente_pico = corrente_pico/185;   // COnverter o valor de tensão para corrente de acordo com o modelo do sensor. No meu caso, esta sensibilidade vale 185mV/A
                                      // O modelo dele é ACS712-05B. Logo, precisamos dividir o valor encontrado por 185 para realizar esta conversão                                       
  
  Serial.print("Corrente de Pico:");
  Serial.print(corrente_pico);
  Serial.print(" A");
  Serial.print(" --- ");
  Serial.print(corrente_pico*1000);
  Serial.println(" mA");
  
 
  //Converter para corrente eficaz  
  corrente_eficaz = corrente_pico/85;
  Serial.print("Corrente Eficaz:");
  Serial.print(corrente_eficaz);
  Serial.print(" A");
  Serial.print(" --- ");
  Serial.print(corrente_eficaz*1000);
  Serial.println(" mA");
  

    valor_voltaje = analogRead(pino_sensorv);
  voltaje = map(valor_voltaje, 0, 4095, 0, 60);


     I=promedio_I(500);//Promedio de 500 muestras para mejorar la presición(llamamos a la función promedio_I()
  Serial.print("Intencidad: ");
  if(I>=0.01){//Filtro para eliminar pequeñas oscilasciones(ruido)
  I= ((I*1)+ajuste),2;
  Serial.println(I);//Imprime el valor de la corriente consumida
 
  delay(100); 
  }else{
  Serial.println("0.00");
I = 0.00; 

  delay(100);   
  }
}


float promedio_I(int muestras_I)
{
  float sensorA0;
  float intencidad=0;
  for(int i=0;i<muestras_I;i++)
  {
    sensorA0 = analogRead(34) * (5.0 / 4095.0);//Leemos el sensor de corriente
    intencidad=intencidad+(sensorA0-2.5)/sensibilidad; //Calculo para obtener el valor de la corriente
  }
  intencidad=intencidad/muestras_I;//dividimos por 500 
  return(intencidad);
}
