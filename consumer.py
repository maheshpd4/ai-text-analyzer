import sqlite3
import json

from confluent_kafka import Consumer


POSITIVE_WORDS = ["good", "great", "excellent", "happy", "awesome"]
NEGATIVE_WORDS = ["bad", "sad", "angry", "poor", "worst"]

consumer_config = {
    "bootstrap.servers": "127.0.0.1:9092",
    "group.id": "text-analyzer-group",
    "auto.offset.reset": "earliest",
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

    positive_count = sum(word.lower() in POSITIVE_WORDS for word in words)
    negative_count = sum(word.lower() in NEGATIVE_WORDS for word in words)

    if positive_count > negative_count:
        sentiment = "Positive"
    elif negative_count > positive_count:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    result = {
        "input_text": text,
        "word_count": len(words),
        "character_count": len(text),
        "positive_words": positive_count,
        "negative_words": negative_count,
        "sentiment": sentiment,
    }

    print("Processed Kafka Message:")
    print(result)

    connection = sqlite3.connect("sentiment.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO sentiment_results (
            input_text,
            word_count,
            character_count,
            positive_words,
            negative_words,
            sentiment
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            result["input_text"],
            result["word_count"],
            result["character_count"],
            result["positive_words"],
            result["negative_words"],
            result["sentiment"],
        ),
    )
    connection.commit()
    connection.close()

    print("Result stored in database")