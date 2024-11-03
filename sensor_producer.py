# Producer (sensor_producer.py)
from kafka import KafkaProducer
import json
import time
import random
import numpy as np

# Configure the producer
producer = KafkaProducer(
    bootstrap_servers='164.92.76.15:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Wind direction options
WIND_DIRECTIONS = ['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE']

def generate_sensor_data():
    # Temperature: Normal distribution with mean 25°C and std dev 5
    # Clipped to [0, 110]
    temp = np.clip(np.random.normal(25, 5), 0, 110)
    temp = round(temp, 2)
    
    # Humidity: Normal distribution with mean 60% and std dev 10
    # Clipped to [0, 100]
    humidity = int(np.clip(np.random.normal(60, 10), 0, 100))
    
    # Wind direction: Random choice
    wind = random.choice(WIND_DIRECTIONS)
    
    return {
        "temperatura": temp,
        "humedad": humidity,
        "direccion_viento": wind
    }

def main():
    print("Starting Weather Station Producer...")
    try:
        while True:
            # Generate and send data
            data = generate_sensor_data()
            producer.send('21153', value=data)
            print(f"Sent: {data}")
            
            # Wait random time between 15-30 seconds
            wait_time = random.uniform(5, 10)
            time.sleep(wait_time)
            
    except KeyboardInterrupt:
        print("\nStopping producer...")
        producer.close()

if __name__ == "__main__":
    main()