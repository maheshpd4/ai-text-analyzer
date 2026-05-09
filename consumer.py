from confluent_kafka import Consumer
import json
import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

consumer_config = {
    "bootstrap.servers": "kafka-service:9092",
    "group.id": "text-analyzer-group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)
consumer.subscribe(["text-events"])

print("Waiting for Kafka messages...", flush=True)

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print("Consumer error:", msg.error(), flush=True)
        continue

    try:
        data = json.loads(msg.value().decode("utf-8"))

        text = data["text"]
        words = text.split()

        positive_words = ["good", "great", "excellent", "happy", "awesome"]
        negative_words = ["bad", "sad", "angry", "poor", "worst"]

        positive_count = sum(
            word.lower() in positive_words for word in words
        )

        negative_count = sum(
            word.lower() in negative_words for word in words
        )

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

        print("Processed Kafka Message:", flush=True)
        print(result, flush=True)

        connection = sqlite3.connect("sentiment.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT,
                word_count INTEGER,
                character_count INTEGER,
                positive_words INTEGER,
                negative_words INTEGER,
                sentiment TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO sentiment_results (
                input_text,
                word_count,
                character_count,
                positive_words,
                negative_words,
                sentiment
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            result["input_text"],
            result["word_count"],
            result["character_count"],
            result["positive_words"],
            result["negative_words"],
            result["sentiment"]
        ))

        connection.commit()
        connection.close()

        print("Result stored in database", flush=True)

    except Exception as e:
        logging.exception(f"Consumer processing failed: {e}")