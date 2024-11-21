# Consume data from Kafka and save it to SQL Server
from kafka import KafkaProducer, KafkaConsumer
import pyodbc
import json
import time
import random
from threading import Thread

def consume_and_save_data():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id='power_consumption_group',
        auto_offset_reset='earliest'
    )
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO powerconsumption (BuildingName, Timestamp, PowerUsageKwh, CostUsd, MaxPowerKwh, MinPowerKwh, AveragePowerKwh)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        for message in consumer:
            data = message.value
            print(f"Consumed: {data}")
            cursor.execute(
                insert_query,
                data['BuildingName'], data['Timestamp'], data['PowerUsageKwh'],
                data['CostUsd'], data['MaxPowerKwh'], data['MinPowerKwh'], data['AveragePowerKwh']
            )
            conn.commit()
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        conn.close()
        consumer.close()

# Run producer and consumer in parallel
if __name__ == "__main__":
    producer_thread = Thread(target=generate_and_produce_data)
    consumer_thread = Thread(target=consume_and_save_data)
    
    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
