# Similar structure, just change the building name
from kafka import KafkaProducer
import time
import random
import json

def generate_building_data(building_name, kafka_topic, kafka_server='localhost:9092'):
    producer = KafkaProducer(
        bootstrap_servers=kafka_server,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        while True:
            data = {
                'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'BuildingName': building_name,
                'PowerUsageKwh': round(random.uniform(0.5, 10.0), 2),
                'CostUsd': round(random.uniform(0.1, 2.0), 2),
                'MaxPowerKwh': round(random.uniform(10.0, 20.0), 2),
                'MinPowerKwh': round(random.uniform(0.1, 1.0), 2),
                'AveragePowerKwh': round(random.uniform(2.0, 8.0), 2)
            }
            producer.send(kafka_topic, data)
            print(f"[{building_name}] Produced: {data}")
            time.sleep(.1)  # Simulate real-time data generation
    except KeyboardInterrupt:
        print(f"Stopping producer for {building_name}...")
    finally:
        producer.close()
