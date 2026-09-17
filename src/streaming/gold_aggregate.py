from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct, round, sum


ROOT_DIR = Path(__file__).resolve().parents[2]
SILVER_PATH = ROOT_DIR / "data" / "lakehouse" / "silver_sales"
GOLD_CATEGORY_PATH = ROOT_DIR / "data" / "lakehouse" / "gold_sales_by_category"
GOLD_REGION_PATH = ROOT_DIR / "data" / "lakehouse" / "gold_sales_by_region"


def main():
    spark = SparkSession.builder.appName("RetailStreamGoldMetrics").getOrCreate()

    sales = spark.read.parquet(str(SILVER_PATH))

    sales_by_category = (
        sales.groupBy("category")
        .agg(
            round(sum("total_amount"), 2).alias("total_sales"),
            countDistinct("order_id").alias("order_count"),
        )
        .orderBy("total_sales", ascending=False)
    )

    sales_by_region = (
        sales.groupBy("region")
        .agg(
            round(sum("total_amount"), 2).alias("total_sales"),
            countDistinct("order_id").alias("order_count"),
        )
        .orderBy("total_sales", ascending=False)
    )

    sales_by_category.write.mode("overwrite").parquet(str(GOLD_CATEGORY_PATH))
    sales_by_region.write.mode("overwrite").parquet(str(GOLD_REGION_PATH))

    print("Gold metrics completed.")
    print("\nSales by category:")
    sales_by_category.show()

    print("\nSales by region:")
    sales_by_region.show()

    spark.stop()


if __name__ == "__main__":
    main()