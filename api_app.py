from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer
import sqlite3
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

app = FastAPI()

producer_config = {
    "bootstrap.servers": "kafka-service:9092",
    "client.id": "text-analyzer-api"
}

producer = Producer(producer_config)


class TextInput(BaseModel):
    text: str


def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Kafka delivery failed: {err}")
    else:
        logging.info(
            f"Message delivered to topic={msg.topic()} "
            f"partition={msg.partition()} offset={msg.offset()}"
        )


@app.get("/")
def home():
    return {
        "message": "AI Text Analyzer API Running"
    }


@app.post("/analyze")
def analyze_text(input_data: TextInput):

    try:
        text = input_data.text.strip()

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Input text cannot be empty"
            )

        message = {
            "text": text
        }

        producer.produce(
            topic="text-events",
            value=json.dumps(message).encode("utf-8"),
            callback=delivery_report
        )

        producer.flush(5)

        return {
            "status": "SUCCESS",
            "message": "Text published to Kafka topic",
            "payload": message
        }

    except Exception as e:
        logging.exception("Kafka publish failed")

        raise HTTPException(
            status_code=500,
            detail=f"Kafka publish error: {str(e)}"
        )


@app.get("/results")
def get_results():

    try:
        connection = sqlite3.connect("sentiment.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                input_text,
                word_count,
                character_count,
                positive_words,
                negative_words,
                sentiment
            FROM sentiment_results
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        connection.close()

        results = []

        for row in rows:
            results.append({
                "id": row[0],
                "input_text": row[1],
                "word_count": row[2],
                "character_count": row[3],
                "positive_words": row[4],
                "negative_words": row[5],
                "sentiment": row[6]
            })

        return {
            "total_records": len(results),
            "results": results
        }

    except Exception as e:
        logging.exception("DB read failed")

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )               