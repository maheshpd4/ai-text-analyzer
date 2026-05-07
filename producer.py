from confluent_kafka import Producer
import json

producer_config = {
    "bootstrap.servers": "localhost:9092"
}

producer = Producer(producer_config)

message = {
    "text": "This is a great and awesome Kafka learning day"
}

producer.produce(
    topic="text-events",
    value=json.dumps(message)
)

producer.flush()

print("Message sent to Kafka topic: text-events")