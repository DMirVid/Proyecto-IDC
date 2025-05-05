from machine import Pin
import time

# Configura el pin de entrada
anemometro = Pin(15, Pin.IN, Pin.PULL_DOWN)

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
    time.sleep(5)  # mide cada 5 segundos
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
