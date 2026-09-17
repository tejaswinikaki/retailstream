# RetailStream — Real-Time Retail Analytics Pipeline

RetailStream is a local, end-to-end Data Engineering portfolio project that processes synthetic retail sales events in near real time.

## Architecture

```text
Synthetic retail events
        ↓
Python Kafka producer
        ↓
Apache Kafka topic: retail-sales
        ↓
PySpark Bronze ingestion
        ↓
Bronze raw Parquet data
        ↓
Silver cleaned sales data
        ↓
Gold sales metrics + data-quality report