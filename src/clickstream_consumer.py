from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("ClickstreamConsumer") \
    .getOrCreate()

# Kafka Configuration
kafka_topic = "clickstream-events"
kafka_bootstrap_servers = "localhost:9092"

# Define Clickstream Schema
clickstream_schema = StructType() \
    .add("user_id", IntegerType()) \
    .add("session_id", IntegerType()) \
    .add("timestamp", IntegerType()) \
    .add("action", StringType()) \
    .add("product_id", IntegerType())

# Read Stream from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Convert Kafka Value to String and Parse JSON
clickstream_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), clickstream_schema).alias("data")) \
    .select("data.*")

# Perform Aggregation (Example: Count Actions)
action_counts = clickstream_df.groupBy("action").count()

# Write Output to Console (For Development)
query = action_counts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
