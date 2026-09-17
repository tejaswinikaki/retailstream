from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


ROOT_DIR = Path(__file__).resolve().parents[2]
BRONZE_PATH = ROOT_DIR / "data" / "lakehouse" / "bronze_sales"
CHECKPOINT_PATH = ROOT_DIR / "data" / "lakehouse" / "checkpoints" / "bronze_sales"


def main():
    spark = (
        SparkSession.builder
        .appName("RetailStreamBronzeIngestion")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
        )
        .getOrCreate()
    )

    kafka_events = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "retail-sales")
        .option("startingOffsets", "earliest")
        .load()
    )

    bronze_events = kafka_events.select(
        col("key").cast("string").alias("key"),
        col("value").cast("string").alias("raw_event"),
        col("timestamp").alias("kafka_timestamp"),
    )

    query = (
        bronze_events.writeStream
        .format("parquet")
        .option("path", str(BRONZE_PATH))
        .option("checkpointLocation", str(CHECKPOINT_PATH))
        .outputMode("append")
        .trigger(availableNow=True)
        .start()
    )

    query.awaitTermination()
    spark.stop()

    print("Bronze ingestion completed.")
    print(f"Saved raw events to: {BRONZE_PATH}")


if __name__ == "__main__":
    main()