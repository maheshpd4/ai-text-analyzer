import json

# Get input from user
text = input("Enter text: ")

# Split words
words = text.split()

# Counts
word_count = len(words)
char_count = len(text)

# Positive and negative word lists
positive_words = ["good", "great", "excellent", "happy", "awesome"]
negative_words = ["bad", "sad", "angry", "poor", "worst"]

# Calculate sentiment counts
positive_count = sum(word.lower() in positive_words for word in words)
negative_count = sum(word.lower() in negative_words for word in words)

# Determine sentiment
sentiment = "Neutral"

if positive_count > negative_count:
    sentiment = "Positive"
elif negative_count > positive_count:
    sentiment = "Negative"

# Print results
print("\n--- Analysis Result ---")
print("Word Count:", word_count)
print("Character Count:", char_count)
print("Positive Words:", positive_count)
print("Negative Words:", negative_count)
print("Sentiment:", sentiment)

# Prepare JSON result
result = {
    "input_text": text,
    "word_count": word_count,
    "character_count": char_count,
    "positive_words": positive_count,
    "negative_words": negative_count,
    "sentiment": sentiment
}

# Save JSON output
with open("output.json", "w") as file:
    json.dump(result, file, indent=4)

print("\nResults saved successfully to output.json")