import subprocess
import os
import time

# Paths to your Kafka and Zookeeper configuration files
ZOOKEEPER_CONFIG = "C:\\kafka\\config\\zookeeper.properties"
KAFKA_CONFIG = "C:\\kafka\\config\\server.properties"

# Paths to your Kafka bin folder
KAFKA_BIN_PATH = "C:\\kafka\\bin\\windows"

# List of topics
TOPIC_NAMES = ["building1_powerconsumption", "building2_powerconsumption", "building3_powerconsumption"]  # Replace with your actual topic names

def start_zookeeper():
    print("Starting Zookeeper...")
    zookeeper_command = os.path.join(KAFKA_BIN_PATH, "zookeeper-server-start.bat")
    process = subprocess.Popen([zookeeper_command, ZOOKEEPER_CONFIG], shell=True)
    return process

def start_kafka():
    print("Starting Kafka Broker...")
    kafka_command = os.path.join(KAFKA_BIN_PATH, "kafka-server-start.bat")
    process = subprocess.Popen([kafka_command, KAFKA_CONFIG], shell=True)
    return process

def open_producer(topic_name):
    print(f"Opening producer for topic '{topic_name}'...")
    producer_command = f'start cmd /k "{os.path.join(KAFKA_BIN_PATH, "kafka-console-producer.bat")} --broker-list localhost:9092 --topic {topic_name}"'
    subprocess.Popen(producer_command, shell=True)

def open_consumer(topics):
    # Join all topic names into a single comma-separated string without extra spaces
    topic_list = ",".join(topics).strip()
    print(f"Opening a single consumer for topics: {topic_list}...")
    # Start one command prompt to consume from multiple topics
    consumer_command = f'start cmd /k "{os.path.join(KAFKA_BIN_PATH, "kafka-console-consumer.bat")} --bootstrap-server localhost:9092 --topic {topic_list} --from-beginning"'
    subprocess.Popen(consumer_command, shell=True)

if __name__ == "__main__":
    try:
        # Start Zookeeper
        zookeeper_process = start_zookeeper()
        time.sleep(5)  # Wait for Zookeeper to start

        # Start Kafka
        kafka_process = start_kafka()
        time.sleep(5)  # Wait for Kafka to start

        # Loop through each topic and open a producer for each
        #for topic_name in TOPIC_NAMES:
        #   open_producer(topic_name)

        # Open a single consumer for all topics in one command prompt window
        open_consumer(TOPIC_NAMES)

        print("Kafka and Zookeeper are running...")
        print(f"Producers are open for topics: {', '.join(TOPIC_NAMES)}")
        print("Consumer is open for all topics in one window.")
        print("Press Ctrl+C to stop.")

        # Keep the script running to hold the processes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        zookeeper_process.terminate()
        kafka_process.terminate()
        print("Services stopped.")
