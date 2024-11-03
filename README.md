# Laboratorio 9: Estación Meteorológica IoT

Este laboratorio implementa una simulación de una estación meteorológica utilizando Apache Kafka para la comunicación entre sensores y visualización de datos en tiempo real.

## Descripción
El sistema simula una estación meteorológica que recolecta datos de:
- Temperatura (0-110°C)
- Humedad Relativa (0-100%)
- Dirección del Viento (N, NO, O, SO, S, SE, E, NE)

Los datos son generados cada 15-30 segundos y enviados a través de un servidor Kafka, donde posteriormente son consumidos y visualizados en tiempo real mediante gráficas.

## Requisitos Previos
- Python 3.x
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar o descargar los archivos del proyecto
2. Instalar las dependencias necesarias:
```bash
pip install kafka-python numpy matplotlib
```

## Estructura del Proyecto
```
LAB9_REDES/
│
├── sensor_producer.py    # Simulador de sensores (Productor)
├── sensor_consumer.py    # Visualizador de datos (Consumidor)
└── README.md            # Este archivo
```

## Configuración
- Servidor Kafka: lab9.alumchat.lol (164.92.76.15:9092)
- Topic Kafka: 21153 (número de carné)

## Uso

1. Iniciar el consumidor (visualizador) en una terminal:
```bash
python sensor_consumer.py
```

2. Iniciar el productor (sensores) en otra terminal:
```bash
python sensor_producer.py
```

### Componentes

#### Productor (sensor_producer.py)
- Simula los sensores de la estación meteorológica
- Genera datos aleatorios siguiendo distribuciones normales para mayor realismo
- Envía datos cada 15-30 segundos al servidor Kafka

#### Consumidor (sensor_consumer.py)
- Recibe los datos en tiempo real
- Muestra tres gráficas actualizadas en tiempo real:
  1. Temperatura (línea roja)
  2. Humedad (línea azul)
  3. Dirección del viento (puntos verdes)
- Mantiene un historial de las últimas 50 lecturas

## Características
- Visualización en tiempo real
- Datos simulados con distribuciones realistas
- Sistema distribuido usando Apache Kafka
- Gráficas interactivas con matplotlib
- Manejo de errores robusto
- Interfaz gráfica intuitiva

## Solución de Problemas

### Errores Comunes

1. Error de conexión a Kafka:
   - Verificar que el servidor Kafka esté funcionando
   - Comprobar la conexión a Internet
   - Verificar que el puerto 9092 no esté bloqueado

2. Error en las gráficas:
   - Asegurarse de tener todas las dependencias instaladas
   - Reiniciar el consumidor
   - Verificar que el productor esté enviando datos

## Notas Adicionales
- Los datos se actualizan cada 15-30 segundos
- Las gráficas muestran las últimas 50 lecturas
- La temperatura sigue una distribución normal centrada en 25°C
- La humedad sigue una distribución normal centrada en 60%
- La dirección del viento se selecciona aleatoriamente

## Contribuidores
- José Santisteban
- Jennifer Toxcon

## Licencia
Este proyecto es parte del curso CC3067 Redes de la Universidad del Valle de Guatemala.