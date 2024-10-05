from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType
import logging
from pymongo import MongoClient
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORT_KEY = "support"
OPPOSE_KEY = "oppose"

T_SUPPORT_COUNT = 0
T_OPPOSE_COUNT = 0

K_SUPPORT_COUNT = 0
K_OPPOSE_COUNT = 0

client = MongoClient("mongodb://localhost:27017/")
db = client["usa2024"]  # use or create a database named usa2024
trump_db = db["trump"]  # use or create a collection named trump
harris_db = db["harris"]  # use or create a collection named harris


def classify_trump(batch_df: DataFrame, batch_id: int):
    # use map in the current stream batch
    print("Classifying tweets")
    print(batch_df.show(5))
    classified_tweets = batch_df.rdd.map(
        # the map function evaluates the tweets and generates a key-value pair
        # where the key is the sentiment and the value is 1 to count the number of tweets

        lambda row: (SUPPORT_KEY, 1))  # add model evaluation here
    counts = classified_tweets.reduceByKey(lambda x, y: x + y)
    global T_SUPPORT_COUNT, T_OPPOSE_COUNT

    for key, value in counts.collect():
        if key == SUPPORT_KEY:
            T_SUPPORT_COUNT += value
        elif key == OPPOSE_KEY:
            T_OPPOSE_COUNT += value

    # save the counts to MongoDB
    trump_db.insert_one({
        "timestamp": datetime.now(),
        SUPPORT_KEY: T_SUPPORT_COUNT,
        OPPOSE_KEY: T_OPPOSE_COUNT
    })

def classify_kamala(batch_df: DataFrame, batch_id: int):
    # use map in the current stream batch
    print("Classifying tweets")
    print(batch_df.show(5))
    classified_tweets = batch_df.rdd.map(
        # the map function evaluates the tweets and generates a key-value pair
        # where the key is the sentiment and the value is 1 to count the number of tweets

        lambda row: (SUPPORT_KEY, 1))  # add model evaluation here
    counts = classified_tweets.reduceByKey(lambda x, y: x + y)
    global K_SUPPORT_COUNT, K_OPPOSE_COUNT

    for key, value in counts.collect():
        if key == SUPPORT_KEY:
            K_SUPPORT_COUNT += value
        elif key == OPPOSE_KEY:
            K_OPPOSE_COUNT += value

    # save the counts to MongoDB
    harris_db.insert_one({
        "timestamp": datetime.now(),
        SUPPORT_KEY: K_SUPPORT_COUNT,
        OPPOSE_KEY: K_OPPOSE_COUNT
    })

def handle_stream():
    spark = SparkSession.builder \
        .appName("KafkaSparkStreamingJSON") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,"
                "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.mongodb.write.connection.uri",
                "mongodb://127.0.0.1:27017/mydb.usa2024") \
        .getOrCreate()

    df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers",
                "localhost:9092,localhost:9093,localhost:9094") \
        .option("subscribe", "trump_tweets") \
        .load()

    json_schema = StructType() \
        .add("username", StringType()) \
        .add("tweet", StringType())

    df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), json_schema).alias("data")) \
        .select("data.username", "data.tweet")

    query = df.writeStream \
        .foreachBatch(classify_trump) \
        .start()

    query.awaitTermination()
