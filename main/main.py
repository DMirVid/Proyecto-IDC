from machine import Pin, ADC, I2C
import dht
from bmp180 import BMP180
import time
from umqtt.simple import MQTTClient
import json
import network

# Configura el pin de entrada
anemometro = Pin(15, Pin.IN, Pin.PULL_DOWN)
ldr = ADC(Pin(28))
sensor = dht.DHT22(Pin(14))

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
bmp = BMP180(i2c)
bmp.oversample_sett = 2
bmp.sea_level_pressure = 101325

# Variables para contar pulsos
pulsos = 0
tiempo_inicio = time.ticks_ms()

# Función de interrupción
def contar_pulsos(pin):
    global pulsos
    pulsos += 1

# Configura interrupción
anemometro.irq(trigger=Pin.IRQ_RISING, handler=contar_pulsos)


#conectarse a una red wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('wifi', 'password')

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
#Conectarse con broker mqtt
mqtt_server = 'test.mosquitto.org'
client_id = 'idc'
topic_pub = 'idc/estación_metereológica/datos'

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   time.sleep(5)
   machine.reset()
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

# Diccionario donde guardar los datos 
# Se convertira a json para mqtt
datos ={'viento': 0.0, 'ldr': 0, 'temperatura': 0, 'humedad': 0.0, 'presion': 0, 'altitud': 0}

# Bucle principal
while True:
    time.sleep(0.5)  # mide cada 0.5 segundos
    tiempo_final = time.ticks_ms()
    tiempo_transcurrido = (tiempo_final - tiempo_inicio) / 1000  # en segundos
    
    # Calcula velocidad del viento (requiere calibración)
    # Ejemplo: 1 pulso = 2.4 km/h (depende del modelo)
    velocidad = pulsos * 2.4 / tiempo_transcurrido
    
    print("Pulsos:", pulsos)
    print("Velocidad estimada:", velocidad, "km/h")

    datos['viento'] = velocidad

    # Reiniciar contador
    pulsos = 0
    tiempo_inicio = time.ticks_ms()

    #EMPIEZA LDR
    valor = ldr.read_u16()  # Valor entre 0 (oscuro) y 65535 (mucha luz)
    print("Luz:", str(valor))

    datos['ldr'] = valor

    #EMPIEZA DHT
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("Temperatura:", temp, "°C")
        print("Humedad:", hum, "%")

        datos['temperatura'] = temp
        datos['humedad'] = hum
    except OSError as e:
        print("Error al leer el sensor:", e)
        
    #EMPIEZA PRESION
        
    bmp.measure()
    presion = bmp.pressure  # en Pa
    altitud = bmp.altitude  # en metros (estimada)
    print("Presión:", presion / 100, "hPa")
    print("Altitud aproximada:", round(altitud, 2), "m")
    
    datos['altitud'] = altitud
    datos['presion'] = presion

    #Mandamos los datos al broker
    client.publish(topic_pub, json.dumps(datos))
