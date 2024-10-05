from confluent_kafka.admin import AdminClient, NewTopic


SERVERS = "localhost:9092,localhost:9093,localhost:9094"

def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1, servers=SERVERS):
    admin_client = AdminClient({"bootstrap.servers": servers})
    topic = NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    try:
        fs = admin_client.create_topics([topic])
        top = fs[topic_name]
        try:
            top.result()
            print(f"Topic '{topic_name}' created successfully.")
        except Exception as e:
            print(f"Failed to create topic '{topic_name}': {e}")
    except Exception as e:
        print(f"Failed to create topic '{topic_name}': {e}")


