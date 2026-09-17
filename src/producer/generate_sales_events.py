import csv
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


ROOT_DIR = Path(__file__).resolve().parents[2]
PRODUCTS_PATH = ROOT_DIR / "data" / "reference" / "products.csv"
STORES_PATH = ROOT_DIR / "data" / "reference" / "stores.csv"
OUTPUT_PATH = ROOT_DIR / "data" / "sample" / "sales_events.jsonl"


def load_csv(file_path):
    with open(file_path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def create_sales_event(product, store):
    quantity = random.randint(1, 4)
    unit_price = float(product["unit_price"])

    return {
        "event_id": str(uuid4()),
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        "order_id": f"ORD{random.randint(10000, 99999)}",
        "customer_id": f"CUST{random.randint(1000, 9999)}",
        "store_id": store["store_id"],
        "region": store["region"],
        "product_id": product["product_id"],
        "category": product["category"],
        "quantity": quantity,
        "unit_price": unit_price,
        "total_amount": round(quantity * unit_price, 2),
    }


def main():
    random.seed(42)

    products = load_csv(PRODUCTS_PATH)
    stores = load_csv(STORES_PATH)

    events = [
        create_sales_event(random.choice(products), random.choice(stores))
        for _ in range(20)
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")

    print(f"Created {len(events)} synthetic sales events.")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()