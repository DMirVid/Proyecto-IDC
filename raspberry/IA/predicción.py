import json
import paho.mqtt.client as mqtt
from sklearn.preprocessing import MinMaxScaler
import math

# --- Activaciones ---
def relu(x): return max(0, x)
def sigmoid(x): return 1 / (1 + math.exp(-x))

# --- Cargar modelo desde JSON ---
with open("modelo_entrenado.txt") as f:
    modelo = json.load(f)

W1 = modelo['W1'][0]
b1 = modelo['b1']
W2 = modelo['W2']
b2 = modelo['b2']
W3 = modelo['W3']
b3 = modelo['b3']
x_min = modelo['normalizacion_min'][0]
x_max = modelo['normalizacion_max'][0]

def inferir_lluvia(presion_hpa):
    x = (presion_hpa - x_min) / (x_max - x_min)

    # Capa oculta 1
    h1 = [relu(W1[i] * x + b1[i]) for i in range(len(W1))]

    # Capa oculta 2
    h2 = []
    for i in range(len(W2[0])):
        suma = sum(W2[j][i] * h1[j] for j in range(len(W1)))
        h2.append(relu(suma + b2[i]))

    # Capa de salida
    z = sum(W3[i][0] * h2[i] for i in range(len(h2))) + b3[0]
    y = sigmoid(z)
    return y

# --- Callback de MQTT ---
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        presion_pa = payload.get('presion', 0)
        presion_hpa = presion_pa / 100.0

        prob = inferir_lluvia(presion_hpa)
        print(f"📡 Presión: {presion_hpa:.2f} hPa")
        print(f"🔎 Probabilidad de lluvia: {prob:.3f}\n")
    except Exception as e:
        print("❌ Error al procesar mensaje:", e)

# --- Conectar al broker MQTT ---
broker = "test.mosquitto.org"
topic = "idc/estacion_meteorologica/datos"

client = mqtt.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(topic)
print(f"✅ Conectado al broker MQTT y suscrito a '{topic}'")

client.loop_forever()
