# Importa las librerías necesarias
from kafka import KafkaProducer
import json
import time
import random
import numpy as np

# Configura el productor de Kafka para enviar datos al broker
producer = KafkaProducer(
    bootstrap_servers='164.92.76.15:9092',  # Dirección del servidor Kafka
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializa los datos en JSON
)

# Lista de direcciones de viento posibles
WIND_DIRECTIONS = ['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE']

# Función que genera datos simulados de los sensores
def generate_sensor_data():
    # Genera temperatura (float) en un rango [0, 110] con media 25 y desviación estándar 5
    temp = np.clip(np.random.normal(25, 5), 0, 110)
    temp = round(temp, 2)
    
    # Genera humedad (int) en un rango [0, 100] con media 60 y desviación estándar 10
    humidity = int(np.clip(np.random.normal(60, 10), 0, 100))
    
    # Selecciona aleatoriamente una dirección del viento de la lista
    wind = random.choice(WIND_DIRECTIONS)
    
    # Retorna los datos en un diccionario
    return {
        "temperatura": temp,
        "humedad": humidity,
        "direccion_viento": wind
    }

# Función principal que envía los datos generados a Kafka
def main():
    print("Starting Weather Station Producer...")
    try:
        while True:
            # Genera los datos del sensor y los envía al topic '21153'
            data = generate_sensor_data()
            producer.send('21153', value=data)
            print(f"Sent: {data}")
            
            # Espera entre 5 y 10 segundos antes de enviar el próximo mensaje
            wait_time = random.uniform(5, 10)
            time.sleep(wait_time)
            
    except KeyboardInterrupt:
        # Cierra el productor de Kafka al interrumpir la ejecución
        print("\nStopping producer...")
        producer.close()

# Ejecuta el productor si es el script principal
if __name__ == "__main__":
    main()
