from threading import Thread
from generatedata_building1 import generate_building_data
from generatedata_building2 import generate_building_data as generate_building_data_2
from generatedata_building3 import generate_building_data as generate_building_data_3
from kafka import KafkaConsumer
import pyodbc
import json
import sys

# Kafka and Database Configuration
KAFKA_SERVER = 'localhost:9092'
DB_CONNECTION_STRING = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;DATABASE=building_powerconsumption;'
    'UID=marlo;PWD=Yukithedog;'
)

# Function to Consume Data and Save to Database
def consume_and_save_data(kafka_topic):
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=[KAFKA_SERVER],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id='power_consumption_group',
        auto_offset_reset='earliest'
    )
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO dbo.powerconsumption (Timestamp, BuildingName, PowerUsageKwh, CostUsd, MaxPowerKwh, MinPowerKwh, AveragePowerKwh)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        for message in consumer:
            data = message.value
            print(f"Consumed from {kafka_topic}: {data}")
            cursor.execute(
                insert_query,
                data['Timestamp'], data['BuildingName'], data['PowerUsageKwh'],
                data['CostUsd'], data['MaxPowerKwh'], data['MinPowerKwh'], data['AveragePowerKwh']
            )
            conn.commit()
    except KeyboardInterrupt:
        print(f"Stopping consumer for {kafka_topic}...")
    finally:
        conn.close()
        consumer.close()

# Main Execution
if __name__ == "__main__":
    # Define buildings and topics
    buildings = [
        ('Building 1', 'building1_powerconsumption', generate_building_data),
        ('Building 2', 'building2_powerconsumption', generate_building_data_2),
        ('Building 3', 'building3_powerconsumption', generate_building_data_3)
    ]

    # Create threads for data producers and consumers
    producer_threads = [
        Thread(target=generate_function, args=(building_name, topic, KAFKA_SERVER))
        for building_name, topic, generate_function in buildings
    ]
    consumer_threads = [
        Thread(target=consume_and_save_data, args=(topic,))
        for _, topic, _ in buildings
    ]

    try:
        # Start all threads
        for thread in producer_threads + consumer_threads:
            thread.start()

        # Wait for all threads to complete
        for thread in producer_threads + consumer_threads:
            thread.join()

    except KeyboardInterrupt:
        print("\nMain process interrupted. Stopping all threads...")
        # Perform any cleanup if necessary before exit
        sys.exit(0)
