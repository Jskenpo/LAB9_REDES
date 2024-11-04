from kafka import KafkaConsumer
import struct
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import matplotlib.dates as mdates
from collections import deque


# Configuración del consumidor
consumer = KafkaConsumer(
    '21153',
    bootstrap_servers='164.92.76.15:9092',
    value_deserializer=lambda x: x,  # Recibimos bytes en lugar de JSON
    auto_offset_reset='earliest'     # Configurar a 'earliest' para leer mensajes antiguos
)

print("Consumer initialized and connected to Kafka broker.")

# Lista de direcciones de viento posibles
WIND_DIRECTIONS = ['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE']

# Deques para almacenar las últimas 50 lecturas de cada sensor
timestamps = deque(maxlen=50)
temperatures = deque(maxlen=50)
humidities = deque(maxlen=50)
wind_directions = deque(maxlen=50)

# Configuración de la figura y los ejes
plt.style.use('bmh')
fig = plt.figure(figsize=(15, 10))
fig.suptitle('Weather Station Real-time Data', fontsize=16)

# Configura los ejes para temperatura, humedad y dirección del viento
ax1 = plt.subplot(311)
temp_line, = ax1.plot([], [], 'r-', label='Temperature (°C)')
ax1.set_ylabel('Temperature (°C)')
ax1.grid(True)
ax1.legend()

ax2 = plt.subplot(312)
humidity_line, = ax2.plot([], [], 'b-', label='Humidity (%)')
ax2.set_ylabel('Humidity (%)')
ax2.grid(True)
ax2.legend()

ax3 = plt.subplot(313)
wind_scatter = ax3.scatter([], [], c='g', label='Wind Direction')
ax3.set_ylabel('Wind Direction')
ax3.set_ylim(-1, 8)
ax3.set_yticks(range(8))
ax3.set_yticklabels(WIND_DIRECTIONS)
ax3.grid(True)
ax3.legend()

for ax in [ax1, ax2, ax3]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

print("Matplotlib figure and axes configured.")

# Decodificación de datos de 3 bytes
def decode_message(encoded_message):
    # Verifica que el mensaje tenga 3 bytes de longitud
    if len(encoded_message) != 3:
        print(f"Error: Expected 3 bytes but got {len(encoded_message)} bytes.")
        return None, None, None  # Retorna valores nulos en caso de error
    
    # Decodifica el mensaje si tiene el tamaño correcto
    packed_data = struct.unpack('>I', b'\x00' + encoded_message)[0]  # Añade un byte de 0 al inicio
    temp_int = (packed_data >> 10) & 0x3FFF
    humidity_int = (packed_data >> 3) & 0x7F
    wind_int = packed_data & 0x07

    # Convertir valores decodificados a sus formas originales
    temp = temp_int / 100.0
    humidity = humidity_int
    wind_direction = WIND_DIRECTIONS[wind_int]
    return temp, humidity, wind_direction

# Convierte las direcciones de viento a números para graficar
def wind_direction_to_number(direction):
    return WIND_DIRECTIONS.index(direction)

def update_plot(frame):
    print("Attempting to consume a message...")
    try:
        # Consumir el siguiente mensaje de Kafka
        message = next(consumer)
        print("Message consumed from Kafka.")
        
        # Decodificar el mensaje
        temp, humidity, wind = decode_message(message.value)
        if temp is None or humidity is None or wind is None:
            print("Skipping message due to decoding error.")
            return temp_line, humidity_line, wind_scatter

        # Si la decodificación es exitosa, actualizar datos de gráficos
        current_time = datetime.datetime.now()
        timestamps.append(current_time)
        temperatures.append(temp)
        humidities.append(humidity)
        wind_directions.append(wind_direction_to_number(wind))

        # Actualizar las líneas de gráficos
        temp_line.set_data(timestamps, temperatures)
        humidity_line.set_data(timestamps, humidities)

        if timestamps and wind_directions:
            wind_scatter.set_offsets(list(zip(mdates.date2num(timestamps), wind_directions)))
        
        for ax in [ax1, ax2, ax3]:
            ax.set_xlim(mdates.date2num(min(timestamps)), mdates.date2num(max(timestamps)))
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        print(f"Updated plot with received data: Temp={temp}°C, Humidity={humidity}%, Wind={wind}")

    except StopIteration:
        print("No more messages to consume.")
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
