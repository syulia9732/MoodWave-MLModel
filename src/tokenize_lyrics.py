# pip install transformers torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load Pre-trained Model
tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")

# Read Input Lyrics from a File
with open("lyrics.txt", "r") as file:
    lyrics = file.read()
    
# Tokenize and Analyze Lyrics
inputs = tokenizer(lyrics, return_tensors="pt", truncation=True, padding=True)
outputs = model(**inputs)
predictions = outputs.logits.softmax(dim=-1)

# Emotion-to-Color Mapping
emotion_to_color = {
    "admiration": "#FFD700",  # Gold
    "amusement": "#FFFF00",  # Yellow
    "anger": "#FF0000",      # Red
    "annoyance": "#FFA500",  # Orange
    "approval": "#90EE90",   # Light Green
    "caring": "#FFC0CB",     # Pink
    "confusion": "#808080",  # Gray
    "curiosity": "#008080",  # Teal
    "desire": "#FF69B4",     # Hot Pink
    "disappointment": "#778899",  # Blue-Gray
    "disapproval": "#556B2F",    # Olive Green
    "disgust": "#006400",        # Dark Green
    "embarrassment": "#FA8072",  # Salmon
    "excitement": "#FFFF33",     # Bright Yellow
    "fear": "#800080",           # Purple
    "gratitude": "#87CEEB",      # Sky Blue
    "grief": "#000080",          # Navy Blue
    "joy": "#FFA07A",            # Bright Orange
    "love": "#FF1493",           # Red-Pink
    "nervousness": "#DDA0DD",    # Light Purple
    "optimism": "#32CD32",       # Lime Green
    "pride": "#4169E1",          # Royal Blue
    "realization": "#00FFFF",    # Cyan
    "relief": "#ADD8E6",         # Light Blue
    "remorse": "#800020",        # Burgundy
    "sadness": "#00008B",        # Dark Blue
    "surprise": "#E6E6FA",       # Lavender
    "neutral": "#FFFFFF",        # White
}

# Predicted Emotions (Example)
predicted_emotions = []




# Map Predictions to Emotions
emotion_labels = ["admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"]
predicted_emotions = [emotion_labels[i] for i in predictions[0].topk(2).indices]

# Map Emotions to Colors
colors = [emotion_to_color[emotion] for emotion in predicted_emotions]
print(f"Predicted Colors: {colors}")


print(f"Predicted Emotions: {predicted_emotions}")
