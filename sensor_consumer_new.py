from kafka import KafkaConsumer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import struct
import datetime
import matplotlib.dates as mdates
from collections import deque

# Configuración del consumidor
consumer = KafkaConsumer(
    '21153',
    bootstrap_servers='164.92.76.15:9092',
    value_deserializer=lambda x: x  # Recibimos bytes en lugar de JSON
)

# Lista de direcciones de viento posibles
WIND_DIRECTIONS = ['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE']

# Deques para almacenar las últimas 50 lecturas de cada sensor
timestamps = deque(maxlen=50)
temperatures = deque(maxlen=50)
humidities = deque(maxlen=50)
wind_directions = deque(maxlen=50)

# Decodificación de datos de 3 bytes
def decode_message(encoded_message):
    packed_data = struct.unpack('>I', b'\x00' + encoded_message)[0]
    temp_int = (packed_data >> 10) & 0x3FFF
    humidity_int = (packed_data >> 3) & 0x7F
    wind_int = packed_data & 0x07

    # Convertir los valores decodificados a los originales
    temp = temp_int / 100.0  # Volver a escala de punto flotante
    humidity = humidity_int
    wind_direction = WIND_DIRECTIONS[wind_int]
    return temp, humidity, wind_direction

# Función que actualiza las gráficas en cada frame
def update_plot(frame):
    try:
        message = next(consumer)
        temp, humidity, wind = decode_message(message.value)
        
        current_time = datetime.datetime.now()
        timestamps.append(current_time)
        temperatures.append(temp)
        humidities.append(humidity)
        wind_directions.append(wind)

        # Actualizar líneas de gráficos (omitir código gráfico para brevedad)

        print(f"Received: Temp={temp}°C, Humidity={humidity}%, Wind={wind}")

    except Exception as e:
        print(f"Error in update_plot: {e}")

    return temp_line, humidity_line, wind_scatter

# Función principal
def main():
    print("Starting Weather Station Consumer...")
    ani = FuncAnimation(fig, update_plot, interval=1000, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
