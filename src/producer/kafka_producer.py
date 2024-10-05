import time
from kafka import KafkaProducer
import json
import csv
import concurrent.futures


# Default Kafka server configuration
SERVERS = "localhost:9092,localhost:9093,localhost:9094"


def produce_tweets(topic_name, csv_file, servers=SERVERS):
    producer = KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file, fieldnames=["username", "tweet"], delimiter="\t")

        for row in reader:
            if row["username"] and row["tweet"]:
                message = {
                    "username": row["username"].strip(),
                    "tweet": row["tweet"].strip(),
                }
                producer.send(topic_name, value=message)
                print(f"Sent: {message}")
            else:
                print(f"Skipping malformed row: {row}")
            time.sleep(0.25)

    producer.flush()
    producer.close()


def feed_tweets(topics: list, csv_files: list, servers=SERVERS):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        task_list = []

        # Create the concurrent tasks
        for topic, file in zip(topics, csv_files):
            future = executor.submit(produce_tweets, topic, file, servers)
            task_list.append(future)

        # Wait for the tasks to finish (optional
        concurrent.futures.wait(task_list)
