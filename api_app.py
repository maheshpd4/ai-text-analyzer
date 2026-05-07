from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer
import sqlite3
import json
import logging

app = FastAPI()

# Kafka Config
producer_config = {
    "bootstrap.servers": "localhost:9092"
}

producer = Producer(producer_config)

class TextInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "AI Text Analyzer API Running"}


@app.post("/analyze")
def analyze_text(input_data: TextInput):

    text = input_data.text

    message = {
        "text": text
    }

    producer.produce(
        topic="text-events",
        value=json.dumps(message)
    )

    producer.flush()

    return {
        "status": "SUCCESS",
        "message": "Text published to Kafka topic"
    }


@app.get("/results")
def get_results():

    connection = sqlite3.connect("sentiment.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM sentiment_results
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return {
        "results": rows
    }