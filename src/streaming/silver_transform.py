from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp, trim
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)


ROOT_DIR = Path(__file__).resolve().parents[2]
BRONZE_PATH = ROOT_DIR / "data" / "lakehouse" / "bronze_sales"
SILVER_PATH = ROOT_DIR / "data" / "lakehouse" / "silver_sales"


sales_schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("event_timestamp", StringType(), True),
    StructField("order_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("store_id", StringType(), True),
    StructField("region", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("category", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("total_amount", DoubleType(), True),
])


def main():
    spark = SparkSession.builder.appName("RetailStreamSilverTransform").getOrCreate()

    bronze = spark.read.parquet(str(BRONZE_PATH))

    silver = (
        bronze
        .select(
            from_json(col("raw_event"), sales_schema).alias("event"),
            col("kafka_timestamp"),
        )
        .select("event.*", "kafka_timestamp")
        .withColumn("event_timestamp", to_timestamp("event_timestamp"))
        .withColumn("region", trim(col("region")))
        .withColumn("category", trim(col("category")))
        .dropDuplicates(["event_id"])
        .filter(col("event_id").isNotNull())
        .filter(col("quantity") > 0)
        .filter(col("unit_price") > 0)
        .filter(col("total_amount") > 0)
    )

    silver.write.mode("overwrite").parquet(str(SILVER_PATH))

    print(f"Silver transformation completed. Clean records: {silver.count()}")
    print(f"Saved clean data to: {SILVER_PATH}")

    spark.stop()


if __name__ == "__main__":
    main()