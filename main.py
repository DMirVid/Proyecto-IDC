from machine import Pin, ADC, I2C, unique_id
import dht
from bmp180 import BMP180
import time
from umqtt.simple import MQTTClient
import json
import network
import ubinascii

# --- Configuración WiFi ---
SSID = 'Xiaomi 12T'
PASSWORD = 'cy3avdk9q4u2j5c'

def conectar_wifi():
    print("Activando WiFi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    max_wait = 10
    while max_wait > 0 and wlan.status() != 3:
        print("Estado WiFi:", wlan.status())
        max_wait -= 1
        time.sleep(1)

    if wlan.status() != 3:
        print("❌ No se pudo conectar. Estado final:", wlan.status())
        raise RuntimeError('network connection failed')
    else:
        print("✅ Conectado a WiFi")
        print("IP:", wlan.ifconfig()[0])
    return wlan

# --- Configuración MQTT ---
mqtt_server = 'test.mosquitto.org'
client_id = ubinascii.hexlify(unique_id()).decode()
topic_pub = 'idc/estacion_meteorologica/datos'

def mqtt_connect():
    print("🔌 Conectando a MQTT...")
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.connect()
    print("✅ Conectado a MQTT Broker:", mqtt_server)
    return client

def reconnect_mqtt():
    print("♻️ Reintentando conexión MQTT...")
    time.sleep(5)
    return mqtt_connect()

# --- Inicialización sensores ---
anemometro = Pin(15, Pin.IN, Pin.PULL_DOWN)
ldr = ADC(Pin(28))
sensor = dht.DHT22(Pin(14))
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
bmp = BMP180(i2c)
bmp.oversample_sett = 2
bmp.sea_level_pressure = 101325

# --- Pulsos del anemómetro ---
pulsos = 0
tiempo_inicio = time.ticks_ms()

def contar_pulsos(pin):
    global pulsos
    pulsos += 1

anemometro.irq(trigger=Pin.IRQ_RISING, handler=contar_pulsos)

# --- Conectar WiFi y MQTT ---
conectar_wifi()
try:
    client = mqtt_connect()
except OSError:
    client = reconnect_mqtt()

# --- Diccionario de datos ---
datos = {'viento': 0.0, 'ldr': 0, 'temperatura': 0, 'humedad': 0.0, 'presion': 0, 'altitud': 0}

# --- Bucle principal ---
while True:
    time.sleep(0.5)

    tiempo_final = time.ticks_ms()
    tiempo_transcurrido = (tiempo_final - tiempo_inicio) / 1000  # segundos
    velocidad = pulsos * 2.4 / tiempo_transcurrido
    print("Pulsos:", pulsos)
    print("Velocidad estimada:", velocidad, "km/h")

    datos['viento'] = velocidad
    pulsos = 0
    tiempo_inicio = time.ticks_ms()

    # Lectura de LDR
    valor = ldr.read_u16()
    print("Luz:", valor)
    datos['ldr'] = valor

    # Lectura de DHT
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("Temperatura:", temp, "°C")
        print("Humedad:", hum, "%")
        datos['temperatura'] = temp
        datos['humedad'] = hum
    except OSError as e:
        print("Error al leer el sensor DHT:", e)

    # Lectura de presión/altitud
    bmp.measure()
    presion = bmp.pressure / 100
    altitud = bmp.altitude
    if (altitud < 0):
        altitud = 0
    print("Presión:", presion, "hPa")
    print("Altitud aproximada:", round(altitud, 2), "m")
    datos['altitud'] = altitud
    datos['presion'] = presion

    # Publicación en MQTT
    try:
        client.publish(topic_pub, json.dumps(datos))
        print("📡 Datos enviados al broker MQTT")
    except OSError as e:
        print("❌ Error publicando MQTT:", e)
        try:
            client.disconnect()
        except:
            pass
        client = reconnect_mqtt()

