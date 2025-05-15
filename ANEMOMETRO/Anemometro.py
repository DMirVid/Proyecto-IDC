from machine import Pin, ADC, I2C
import dht
from bmp180 import BMP180
import time

# Configura el pin de entrada
anemometro = Pin(15, Pin.IN, Pin.PULL_DOWN)
ldr = ADC(Pin(28))
sensor = dht.DHT22(machine.Pin(14))

i2c = I2C(1, scl=Pin(21), sda=Pin(20))
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

    # Reiniciar contador
    pulsos = 0
    tiempo_inicio = time.ticks_ms()

    #EMPIEZA LDR
    valor = ldr.read_u16()  # Valor entre 0 (oscuro) y 65535 (mucha luz)
    print("Luz:", str(valor))
    
    #EMPIEZA DHT
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("Temperatura:", temp, "°C")
        print("Humedad:", hum, "%")
    except OSError as e:
        print("Error al leer el sensor:", e)
        
    #EMPIEZA PRESION
        
    bmp.measure()
    presion = bmp.pressure  # en Pa
    altitud = bmp.altitude  # en metros (estimada)
    print("Presión:", presion / 100, "hPa")
    print("Altitud aproximada:", round(altitud, 2), "m")
    
    
