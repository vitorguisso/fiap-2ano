#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

#define DHTPIN 4
#define DHTTYPE DHT22
#define BUTTON_PIN 2

const char* ssid = "Wokwi-GUEST";
const char* password = "";

const char* mqtt_server = "broker.emqx.io";
const int mqtt_port = 1883;
const char* topic = "cardioia/sensores";

// ==========================
// SIMULAÇÃO DE WIFI
// ==========================
bool wifiSimulado = true;
unsigned long ultimoToggleWifi = 0;

// ==========================
// INTERVALOS
// ==========================
const unsigned long READ_INTERVAL = 10000;

// ==========================
// CONFIGURAÇÃO BPM
// ==========================
const int BPM_BASE = 70;
const int BPM_INCREMENTO_POR_CLIQUE = 5;
const int BPM_MAXIMO = 180;

// ==========================
// OBJETOS
// ==========================
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

// ==========================
// ESTRUTURA DE CACHE
// ==========================
struct Reading {
  float temp;
  float hum;
  int bpm;
  unsigned long ts;
};

Reading cache[50];
int cacheCount = 0;

// ==========================
// VARIÁVEIS
// ==========================
unsigned long lastRead = 0;
unsigned long lastButtonPress = 0;

bool lastButtonState = HIGH;

int beatCount = 0;
int currentBPM = BPM_BASE;

// =====================================================
// SETUP
// =====================================================
void setup() {

  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  dht.begin();

  Serial.println("\n=== CARDIOIA INICIADO ===");

  if (wifiSimulado) {
    setup_wifi();
    client.setServer(mqtt_server, mqtt_port);
  }
}

// =====================================================
// LOOP
// =====================================================
void loop() {

  simularConexaoWifi();

  handleButton();

  if (wifiSimulado) {

    if (WiFi.status() != WL_CONNECTED) {
      setup_wifi();
    }

    if (!client.connected()) {
      reconnect();
    }

    client.loop();
  }

  if (millis() - lastRead > READ_INTERVAL) {

    readSensors();

    lastRead = millis();
  }
}

// =====================================================
// SIMULAÇÃO DE CONEXÃO WIFI
// =====================================================
void simularConexaoWifi() {

  unsigned long agora = millis();

  // alterna ONLINE/OFFLINE a cada 30 segundos
  if (agora - ultimoToggleWifi >= 30000) {

    wifiSimulado = !wifiSimulado;

    ultimoToggleWifi = agora;

    if (wifiSimulado) {

      Serial.println("\n=== WIFI SIMULADO: ONLINE ===");

    } else {

      Serial.println("\n=== WIFI SIMULADO: OFFLINE ===");
    }
  }
}

// =====================================================
// LEITURA DO BOTÃO
// =====================================================
void handleButton() {

  bool buttonState = digitalRead(BUTTON_PIN);

  unsigned long now = millis();

  if (buttonState == LOW && lastButtonState == HIGH) {

    if (now - lastButtonPress > 80) {

      beatCount++;

      lastButtonPress = now;

      Serial.print("Clique detectado | Total na janela: ");

      Serial.println(beatCount);
    }
  }

  lastButtonState = buttonState;
}

// =====================================================
// LEITURA DOS SENSORES
// =====================================================
void readSensors() {

  float t = dht.readTemperature();

  float h = dht.readHumidity();

  if (isnan(t) || isnan(h)) {

    Serial.println("Erro ao ler DHT22");

    return;
  }

  // ==========================
  // LÓGICA BPM
  // ==========================
  if (beatCount == 0) {

    currentBPM = BPM_BASE;

  } else if (beatCount >= 1 && beatCount <= 2) {

    currentBPM = 0;

  } else if (beatCount >= 3 && beatCount <= 4) {

    currentBPM = 40;

  } else {

    currentBPM = BPM_BASE + (beatCount * BPM_INCREMENTO_POR_CLIQUE);

    if (currentBPM > BPM_MAXIMO) {

      currentBPM = BPM_MAXIMO;
    }
  }

  beatCount = 0;

  Reading r = {t, h, currentBPM, millis()};

  // ==========================
  // ENVIO OU CACHE
  // ==========================
  if (wifiSimulado && client.connected()) {

    publishData(r, false);

  } else {

    saveToCache(r);
  }
}

// =====================================================
// SALVAR NO CACHE
// =====================================================
void saveToCache(const Reading& r) {

  if (cacheCount < 50) {

    cache[cacheCount++] = r;

    Serial.print("OFFLINE → salvando no cache: ");

    Serial.print(cacheCount);

    Serial.println("/50");

  } else {

    Serial.println("Cache cheio → dado descartado");
  }
}

// =====================================================
// PUBLICAR MQTT
// =====================================================
void publishData(const Reading& r, bool isCached) {

  bool hipotermia = r.temp < 35.0;

  bool febre = r.temp >= 38.0;

  bool alertaBPM = r.bpm > 120;

  bool sinalAusente = r.bpm == 0;

  bool bradicardia = r.bpm > 0 && r.bpm < 50;

  String status = "normal";

  if (sinalAusente) {

    status = "sinal_ausente";

  } else if ((hipotermia || febre) && alertaBPM) {

    status = "alerta_critico";

  } else if (hipotermia) {

    status = "hipotermia";

  } else if (febre) {

    status = "febre";

  } else if (alertaBPM) {

    status = "taquicardia";

  } else if (bradicardia) {

    status = "bradicardia";
  }

  DynamicJsonDocument doc(256);

  doc["temperatura"] = r.temp;
  doc["umidade"] = r.hum;
  doc["bpm"] = r.bpm;
  doc["timestamp"] = r.ts;
  doc["cached"] = isCached;

  doc["hipotermia"] = hipotermia;
  doc["febre"] = febre;
  doc["alerta_bpm"] = alertaBPM;
  doc["bradicardia"] = bradicardia;
  doc["sinal_ausente"] = sinalAusente;

  doc["status_paciente"] = status;

  String payload;

  serializeJson(doc, payload);

  if (client.publish(topic, payload.c_str())) {

    Serial.print("MQTT → ");

    Serial.println(payload);

  } else {

    Serial.println("Erro MQTT → salvando no cache");

    saveToCache(r);
  }
}

// =====================================================
// ENVIAR CACHE
// =====================================================
void sendCache() {

  if (cacheCount == 0) {
    return;
  }

  Serial.print("Sincronizando cache: ");

  Serial.println(cacheCount);

  for (int i = 0; i < cacheCount; i++) {

    publishData(cache[i], true);

    delay(200);
  }

  cacheCount = 0;

  Serial.println("Cache enviado com sucesso");
}

// =====================================================
// WIFI
// =====================================================
void setup_wifi() {

  Serial.print("Conectando Wi-Fi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");
  }

  Serial.println("\nWi-Fi conectado");
}

// =====================================================
// MQTT
// =====================================================
void reconnect() {

  while (!client.connected()) {

    Serial.print("Conectando MQTT... ");

    String clientId = "CardioIA-";

    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {

      Serial.println("OK");

      if (cacheCount > 0) {

        sendCache();
      }

    } else {

      Serial.print("Erro: ");

      Serial.println(client.state());

      delay(5000);
    }
  }
}