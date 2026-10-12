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
## Power BI Sales Analytics Dashboard

Developed an interactive Power BI report using processed retail sales data from the Gold layer of the RetailStream data pipeline.

**Dashboard Features:**
- Total Sales and Total Orders KPI cards
- Sales performance analysis by product category
- Regional sales comparison
- Category slicer for exploring category-level sales results
- Power Query integration with CSV datasets exported from the Gold layer

**Technologies:** Power BI, Power Query, Python, PySpark, Parquet, CSV

The repository includes the Power BI report (`.pbix`) and a dashboard screenshot for preview.

The repository includes a dashboard screenshot for preview.
