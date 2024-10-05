from producer.kafka_create_topic import create_kafka_topic
from producer.kafka_producer import feed_tweets
from stream.classify_tweets import handle_stream


SERVERS = "localhost:9092,localhost:9093,localhost:9094"

# Create Kafka topics
create_kafka_topic('trump_tweets', 2, 3, SERVERS)
create_kafka_topic('kamala_tweets', 2, 3, SERVERS)

# Start the stream
feed_tweets()

# Handle the stream and classify the tweets
handle_stream()


