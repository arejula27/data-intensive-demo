from producer.kafka_create_topic import create_kafka_topic
from producer.kafka_producer import produce_tweets
from stream.classify_tweets import handle_stream

# Create Kafka topics
create_kafka_topic('trump_tweets',2,3,"localhost:9092,localhost:9093,localhost:9094")

# Start the stream
produce_tweets('trump_tweets', "localhost:9092,localhost:9093,localhost:9094")

# Handle the stream and classify the tweets
handle_stream()


