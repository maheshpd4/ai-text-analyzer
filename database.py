import sqlite3

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

connection.commit()

print("Database and table created successfully")

connection.close()