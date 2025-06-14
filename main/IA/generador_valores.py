import numpy as np
import pandas as pd

# Asegura reproducibilidad
np.random.seed(42)

# Simular presión alta (sin lluvia)
pres_alta = np.random.normal(1025, 5, 100)
lluvia_alta = np.zeros(100)

# Simular presión media (mezcla de lluvia y no lluvia)
pres_media = np.random.normal(1006, 3, 100)
lluvia_media = np.random.binomial(1, 0.4, 100)

# Simular presión baja (lluvia frecuente)
pres_baja = np.random.normal(985, 5, 100)
lluvia_baja = np.ones(100)

# Concatenar todos los datos
presion = np.concatenate([pres_alta, pres_media, pres_baja])
lluvia = np.concatenate([lluvia_alta, lluvia_media, lluvia_baja])

# Crear DataFrame
df = pd.DataFrame({
    'presion_hpa': np.round(presion, 2),
    'lluvia': lluvia.astype(int)
})

# Guardar como CSV con punto decimal y sin separador de miles
df.to_csv('datos_presion_lluvia.csv', index=False)

print("✅ Archivo 'datos_presion_lluvia.csv' generado correctamente.")
print(df.head())
