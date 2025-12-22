# ? Forex LSTM Models - Auto-updated

![Last Update](https://img.shields.io/badge/Last%20Update-2025-12-22-blue)
![Status](https://img.shields.io/badge/Status-Active-green)

## ? Modelo EUR/USD LSTM

Modelos LSTM para predicci?n de precios EUR/USD, entrenados con datos hist?ricos de 1 hora.

### ? Estructura del Repositorio

```
forex-models/
??? models/
?   ??? pytorch/
?   ?   ??? eurusd_lstm_pytorch.onnx      # Modelo PyTorch (formato ONNX)
?   ??? tensorflow/
?   ?   ??? eurusd_lstm_tf2onnx.onnx      # Modelo TensorFlow (formato ONNX)
?   ??? scalers/
?   ?   ??? eurusd_scaler_improved.pkl    # Scaler MinMaxScaler
?   ??? config/
?       ??? eurusd_model_config_improved.json  # Configuraci?n del modelo
??? data/
?   ??? EURUSD_1h_data.csv                # Dataset actualizado (10k+ registros)
??? results/
    ??? training_results.png              # Gr?ficas de entrenamiento
```

### ? Actualizaci?n Autom?tica

Este repositorio se actualiza autom?ticamente:
- **Frecuencia:** Domingo a Jueves, 21:00 CET
- **M?todo:** Google Apps Script + Colab
- **?ltima actualizaci?n:** 2025-12-22

### ? Caracter?sticas del Modelo

- **Arquitectura:** LSTM mejorado (3 capas, 256 unidades)
- **Features:** Open, High, Low, Close
- **Secuencia:** 60 per?odos (60 horas)
- **Datos:** EUR/USD 1h desde 2023
- **Formato:** ONNX (compatible con m?ltiples frameworks)

### ? Uso del Modelo

#### Python con ONNX Runtime

```python
import onnxruntime as ort
import numpy as np

# Cargar modelo
session = ort.InferenceSession('models/pytorch/eurusd_lstm_pytorch.onnx')

# Preparar input (60 per?odos, 4 features)
input_data = np.random.randn(1, 60, 4).astype(np.float32)

# Predicci?n
outputs = session.run(None, {'input': input_data})
prediction = outputs[0]
```

### ? M?tricas de Entrenamiento

Ver `results/training_results.png` para gr?ficas detalladas.

### ? Licencia

MIT License - Uso libre para fines educativos y comerciales.

### ? Contribuciones

Este repositorio es auto-generado. Para cambios en el modelo, contacta al mantenedor.

---

**? Auto-generado por Colab Automation Script**  
**? ?ltima actualizaci?n:** 22/12/2025, 3:21:04
