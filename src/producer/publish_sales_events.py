import json
from pathlib import Path
from kafka import KafkaProducer


ROOT_DIR = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT_DIR / "data" / "sample" / "sales_events.jsonl"
TOPIC_NAME = "retail-sales"


def main():
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda event: json.dumps(event).encode("utf-8"),
    )

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        for line in file:
            event = json.loads(line)
            producer.send(TOPIC_NAME, event)

    producer.flush()
    producer.close()

    print("Published 20 sales events to Kafka topic: retail-sales")


if __name__ == "__main__":
    main()