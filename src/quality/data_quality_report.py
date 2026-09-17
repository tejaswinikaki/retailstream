import json
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count


ROOT_DIR = Path(__file__).resolve().parents[2]
SILVER_PATH = ROOT_DIR / "data" / "lakehouse" / "silver_sales"
REPORT_PATH = ROOT_DIR / "data" / "lakehouse" / "quality_report.json"


def main():
    spark = SparkSession.builder.appName("RetailStreamDataQuality").getOrCreate()

    sales = spark.read.parquet(str(SILVER_PATH))

    total_records = sales.count()
    duplicate_event_ids = total_records - sales.dropDuplicates(["event_id"]).count()

    null_counts = sales.select(
        count(when(col("event_id").isNull(), 1)).alias("event_id"),
        count(when(col("order_id").isNull(), 1)).alias("order_id"),
        count(when(col("product_id").isNull(), 1)).alias("product_id"),
        count(when(col("total_amount").isNull(), 1)).alias("total_amount"),
    ).first().asDict()

    report = {
        "total_clean_records": total_records,
        "duplicate_event_ids": duplicate_event_ids,
        "null_counts": null_counts,
        "status": "PASSED" if duplicate_event_ids == 0 and sum(null_counts.values()) == 0 else "REVIEW",
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print("Data quality report:")
    print(json.dumps(report, indent=2))
    print(f"\nSaved report to: {REPORT_PATH}")

    spark.stop()


if __name__ == "__main__":
    main()