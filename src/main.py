from producer.kafka_create_topic import create_kafka_topic
from producer.kafka_producer import feed_tweets
from stream.classify_tweets import handle_stream


SERVERS = "localhost:9092,localhost:9093,localhost:9094"
TRUMP_TOPIC = "trump_tweets"
KAMALA_TOPIC = "kamala_tweets"
TRUMP_TWEETS_FILE = "../twitter_scraper/trump_tweets.csv"
KAMALA_TWEETS_FILE = "../twitter_scraper/kamala_tweets.tsv"

if __name__ == "__main__":
    # Create Kafka topics
    create_kafka_topic(TRUMP_TOPIC, 2, 3, SERVERS)
    create_kafka_topic(KAMALA_TOPIC, 2, 3, SERVERS)

    # Start the stream
    feed_tweets(
        [TRUMP_TOPIC, KAMALA_TOPIC], [TRUMP_TWEETS_FILE, KAMALA_TWEETS_FILE], SERVERS
    )

    # Handle the stream and classify the tweets
    handle_stream(TRUMP_TOPIC, KAMALA_TOPIC, SERVERS)
