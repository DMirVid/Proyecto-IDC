import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler

# Leer los datos desde archivo .txt tipo CSV
df = pd.read_csv("datos_lluvia.txt")

# Entrada y salida
X = df[['presion_hpa']].values
y = df['lluvia'].values

# Normalizar presión (recomendado para redes neuronales)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Modelo: 2 capas ocultas densas (5 y 3 neuronas)
model = MLPClassifier(hidden_layer_sizes=(5, 3), activation='relu', max_iter=3000, random_state=42)
model.fit(X_scaled, y)

# Evaluación
score = model.score(X_scaled, y)
print("Precisión del modelo:", round(score * 100, 2), "%")

# Extraer pesos y biases
pesos = {
    "W1": model.coefs_[0].tolist(),  # entrada -> capa oculta 1
    "b1": model.intercepts_[0].tolist(),
    "W2": model.coefs_[1].tolist(),  # capa oculta 1 -> capa oculta 2
    "b2": model.intercepts_[1].tolist(),
    "W3": model.coefs_[2].tolist(),  # capa oculta 2 -> salida
    "b3": model.intercepts_[2].tolist(),
    "normalizacion_min": scaler.data_min_.tolist(),
    "normalizacion_max": scaler.data_max_.tolist(),
    "precision": score
}

# Guardar en .txt (como JSON legible)
import json
with open("modelo_entrenado.txt", "w") as f:
    json.dump(pesos, f, indent=4)

print("✅ Pesos y bias guardados en 'modelo_entrenado.txt'")
