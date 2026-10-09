from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


ROOT_DIR = Path(__file__).resolve().parents[2]
SILVER_PATH = ROOT_DIR / "data" / "lakehouse" / "silver_sales"


def get_spark():
    return (
        SparkSession.builder
        .master("local[*]")
        .appName("RetailStreamAIInsights")
        .getOrCreate()
    )


def load_sales():
    spark = get_spark()
    return spark.read.parquet(str(SILVER_PATH))


def get_summary():
    sales = load_sales()

    total_sales = sales.agg(
        F.round(F.sum("total_amount"), 2).alias("total_sales")
    ).first()["total_sales"]

    return {
        "record_count": sales.count(),
        "order_count": sales.select("order_id").distinct().count(),
        "total_sales": float(total_sales),
        "category_sales": (
            sales.groupBy("category")
            .agg(F.round(F.sum("total_amount"), 2).alias("total_sales"))
            .orderBy(F.desc("total_sales"))
            .toPandas()
        ),
        "region_sales": (
            sales.groupBy("region")
            .agg(F.round(F.sum("total_amount"), 2).alias("total_sales"))
            .orderBy(F.desc("total_sales"))
            .toPandas()
        ),
    }