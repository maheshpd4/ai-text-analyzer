from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer
import json
import logging
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI()

import os

producer_config = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
}

producer = Producer(producer_config)

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(input_data: TextInput):

    try:

        text = input_data.text

        if not text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty")

        message = {
            "text": text
        }

        producer.produce(
            topic="text-events",
            value=json.dumps(message)
        )

        producer.flush()

        logging.info(f"Message published to Kafka: {message}")

        return {
            "status": "SUCCESS",
            "message": "Text published to Kafka topic",
            "data": message
        }

    except Exception as e:
        logging.exception("Kafka publish failed")
        raise HTTPException(status_code=500, detail=str(e))