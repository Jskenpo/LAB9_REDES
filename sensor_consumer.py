# Importa las librerías necesarias
from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from collections import deque
import datetime
import matplotlib.dates as mdates

# Configura el consumidor de Kafka para recibir datos en tiempo real
consumer = KafkaConsumer(
    '21153',
    bootstrap_servers='164.92.76.15:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest'
)

# Deques para almacenar las últimas 50 lecturas de cada sensor
MAX_POINTS = 50
timestamps = deque(maxlen=MAX_POINTS)
temperatures = deque(maxlen=MAX_POINTS)
humidities = deque(maxlen=MAX_POINTS)
wind_directions = deque(maxlen=MAX_POINTS)

# Configura el estilo y crea la figura para las gráficas
plt.style.use('bmh')
fig = plt.figure(figsize=(15, 10))
fig.suptitle('Weather Station Real-time Data', fontsize=16)

# Configura los ejes y las líneas para la temperatura, humedad y dirección del viento
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
ax3.set_yticklabels(['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE'])
ax3.grid(True)
ax3.legend()

# Formato de las etiquetas de tiempo en el eje X
for ax in [ax1, ax2, ax3]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

# Convierte las direcciones de viento a números para graficar
def wind_direction_to_number(direction):
    return ['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE'].index(direction)

# Función que actualiza las gráficas en cada frame
def update_plot(frame):
    try:
        # Consume el siguiente mensaje de Kafka
        message = next(consumer)
        data = message.value
        
        # Agrega los datos actuales a las listas
        current_time = datetime.datetime.now()
        timestamps.append(current_time)
        temperatures.append(data['temperatura'])
        humidities.append(data['humedad'])
        wind_directions.append(wind_direction_to_number(data['direccion_viento']))
        
        # Actualiza las líneas de temperatura y humedad
        temp_line.set_data(timestamps, temperatures)
        if temperatures:
            ax1.set_ylim(min(temperatures) - 1, max(temperatures) + 1)
        
        humidity_line.set_data(timestamps, humidities)
        if humidities:
            ax2.set_ylim(min(humidities) - 1, max(humidities) + 1)
        
        # Actualiza la gráfica de dirección de viento
        if timestamps and wind_directions:
            wind_scatter.set_offsets(list(zip(mdates.date2num(timestamps), wind_directions)))
        
        # Ajusta los límites del eje X para todas las gráficas
        if len(timestamps) > 0:
            for ax in [ax1, ax2, ax3]:
                ax.set_xlim(mdates.date2num(min(timestamps)), mdates.date2num(max(timestamps)))
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        # Muestra los datos recibidos en la consola
        print(f"Received data: Temp={data['temperatura']}°C, Humidity={data['humedad']}%, Wind={data['direccion_viento']}")
        
    except Exception as e:
        print(f"Error in update_plot: {e}")
    
    return temp_line, humidity_line, wind_scatter

# Función principal que inicia la animación de las gráficas
def main():
    print("Starting Weather Station Consumer...")
    print("Waiting for data...")
    
    ani = FuncAnimation(fig, update_plot, interval=1000, blit=True)
    plt.show()

# Ejecuta el consumidor si es el script principal
if __name__ == "__main__":
    main()
