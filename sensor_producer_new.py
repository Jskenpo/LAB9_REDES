from kafka import KafkaProducer
import random
import numpy as np
import struct
import time 

# Configuración del productor
producer = KafkaProducer(
    bootstrap_servers='164.92.76.15:9092',
    value_serializer=lambda v: v  # Enviar los datos binarios sin transformar
)

# Lista de direcciones de viento posibles
WIND_DIRECTIONS = ['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE']

# Codificación de datos a 3 bytes
def encode_message(temp, humidity, wind_direction):
    # Redondear temperatura para ajustarla a 14 bits
    temp_int = int(temp * 100)  # Asumiendo temperatura en el rango de 0 a 110.00 (se guarda sin decimales)
    humidity_int = int(humidity)  # Humedad en el rango de 0 a 100
    wind_int = WIND_DIRECTIONS.index(wind_direction)  # Convertir dirección de viento a índice (0 a 7)

    # Construir los 3 bytes
    packed_data = (temp_int << 10) | (humidity_int << 3) | wind_int
    return struct.pack('>I', packed_data)[1:]  # Mantén solo los últimos 3 bytes

# Función que genera datos simulados de los sensores
def generate_sensor_data():
    temp = np.clip(np.random.normal(25, 5), 0, 110)
    humidity = int(np.clip(np.random.normal(60, 10), 0, 100))
    wind = random.choice(WIND_DIRECTIONS)
    return temp, humidity, wind

# Función principal que envía los datos generados a Kafka
def main():
    print("Starting Weather Station Producer...")
    try:
        while True:
            # Generar datos del sensor y codificarlos en 3 bytes
            temp, humidity, wind = generate_sensor_data()
            encoded_message = encode_message(temp, humidity, wind)
            
            # Enviar el mensaje codificado (3 bytes)
            producer.send('21153', value=encoded_message)
            print(f"Sent: Encoded Message={encoded_message.hex()}, Temp={temp}°C, Humidity={humidity}%, Wind={wind}")
            
            time.sleep(random.uniform(5, 10))
            
    except KeyboardInterrupt:
        print("\nStopping producer...")
        producer.close()

if __name__ == "__main__":
    main()
