from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "AI Text Analyzer API Running"}

@app.post("/analyze")
def analyze_text(input_data: TextInput):

    text = input_data.text

    words = text.split()

    word_count = len(words)
    char_count = len(text)

    positive_words = ["good", "great", "excellent", "happy", "awesome"]
    negative_words = ["bad", "sad", "angry", "poor", "worst"]

    positive_count = sum(word.lower() in positive_words for word in words)
    negative_count = sum(word.lower() in negative_words for word in words)

    sentiment = "Neutral"

    if positive_count > negative_count:
        sentiment = "Positive"
    elif negative_count > positive_count:
        sentiment = "Negative"

    return {
        "input_text": text,
        "word_count": word_count,
        "character_count": char_count,
        "positive_words": positive_count,
        "negative_words": negative_count,
        "sentiment": sentiment
    }