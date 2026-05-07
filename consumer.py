from confluent_kafka import Consumer
import json

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "text-analyzer-group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)
consumer.subscribe(["text-events"])

print("Waiting for Kafka messages...")

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print("Consumer error:", msg.error())
        continue

    data = json.loads(msg.value().decode("utf-8"))

    text = data["text"]
    words = text.split()

    positive_words = ["good", "great", "excellent", "happy", "awesome"]
    negative_words = ["bad", "sad", "angry", "poor", "worst"]

    positive_count = sum(word.lower() in positive_words for word in words)
    negative_count = sum(word.lower() in negative_words for word in words)

    sentiment = "Neutral"

    if positive_count > negative_count:
        sentiment = "Positive"
    elif negative_count > positive_count:
        sentiment = "Negative"

    result = {
        "input_text": text,
        "word_count": len(words),
        "character_count": len(text),
        "positive_words": positive_count,
        "negative_words": negative_count,
        "sentiment": sentiment
    }

    print("Processed Kafka Message:")
    print(result)