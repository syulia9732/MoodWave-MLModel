import os
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from itertools import combinations

# Load Pre-trained Model
tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")

# Mapping emotions to Plutchik's 8 primary emotions
emotion_to_class = {
    "admiration": "trust", "amusement": "joy", "anger": "anger", "annoyance": "anger",
    "approval": "trust", "caring": "trust", "confusion": "surprise", "curiosity": "anticipation",
    "desire": "anticipation", "disappointment": "sadness", "disapproval": "anger", "disgust": "disgust",
    "embarrassment": "sadness", "excitement": "joy", "fear": "fear", "gratitude": "trust",
    "grief": "sadness", "joy": "joy", "love": "joy", "nervousness": "fear", "optimism": "anticipation",
    "pride": "joy", "realization": "surprise", "relief": "joy", "remorse": "sadness",
    "sadness": "sadness", "surprise": "surprise", "neutral": None
}

# Dyad mapping based on Plutchik's model
primary_dyads = {
    ("joy", "trust"): "love", ("trust", "fear"): "submission", ("fear", "surprise"): "alarm",
    ("surprise", "sadness"): "disappointment", ("sadness", "disgust"): "remorse", ("disgust", "anger"): "contempt",
    ("anger", "anticipation"): "aggression", ("anticipation", "joy"): "optimism"
}

secondary_dyads = {
    ("joy", "fear"): "guilt", ("trust", "surprise"): "curiosity", ("fear", "sadness"): "despair",
    ("surprise", "disgust"): "unbelief", ("sadness", "anger"): "envy", ("disgust", "anticipation"): "cynicism",
    ("anger", "joy"): "pride", ("anticipation", "trust"): "hope"
}

tertiary_dyads = {
    ("joy", "surprise"): "delight", ("trust", "sadness"): "sentimentality", ("fear", "disgust"): "shame",
    ("surprise", "anger"): "outrage", ("sadness", "anticipation"): "pessimism", ("disgust", "joy"): "morbidness",
    ("anger", "trust"): "dominance", ("anticipation", "fear"): "anxiety"
}

opposite_dyads = {
    ("joy", "sadness"): "bittersweetness", ("trust", "disgust"): "ambivalence", ("fear", "anger"): "frozenness",
    ("surprise", "anticipation"): "confusion"
}

uniform_dyads = {
    ("anger", "anger"): "anger", ("anticipation", "anticipation"): "anticipation", ("joy", "joy"): "joy",
    ("trust", "trust"): "trust", ("fear", "fear"): "fear", ("surprise", "surprise"): "surprise",
    ("sadness", "sadness"): "sadness", ("disgust", "disgust"): "disgust"
}

# Combine all dyads into a single map
dyad_emotion_map = {**primary_dyads, **secondary_dyads, **tertiary_dyads, **opposite_dyads, **uniform_dyads}

# Emotion to color mapping
emotion_to_color = {
    "admiration": "#FFD700", "amusement": "#FFFF00", "anger": "#FF0000", "annoyance": "#FFA500",
    "approval": "#90EE90", "caring": "#FFC0CB", "confusion": "#808080", "curiosity": "#008080",
    "desire": "#FF69B4", "disappointment": "#778899", "disapproval": "#556B2F", "disgust": "#006400",
    "embarrassment": "#FA8072", "excitement": "#FFFF33", "fear": "#800080", "gratitude": "#87CEEB",
    "grief": "#000080", "joy": "#FFA07A", "love": "#FF1493", "nervousness": "#DDA0DD",
    "optimism": "#32CD32", "pride": "#4169E1", "realization": "#00FFFF", "relief": "#ADD8E6",
    "remorse": "#800020", "sadness": "#00008B", "surprise": "#E6E6FA", "neutral": "#FFFFFF"
}

# Function to classify emotions into 8 classes
def classify_emotions(predicted_emotions):
    primary_emotions = [emotion_to_class[emotion] for emotion in predicted_emotions if emotion in emotion_to_class]
    return primary_emotions

# Function to generate emotion combinations
def generate_emotion_combinations(emotions):
    if len(set(emotions)) == 1:
        return [("uniform", emotions[0])]
    for comb in combinations(emotions, 2):
        if comb in dyad_emotion_map or tuple(reversed(comb)) in dyad_emotion_map:
            dyad_emotion = dyad_emotion_map.get(comb, dyad_emotion_map.get(tuple(reversed(comb))))
            if comb in primary_dyads or tuple(reversed(comb)) in primary_dyads:
                dyad_type = "primary"
            elif comb in secondary_dyads or tuple(reversed(comb)) in secondary_dyads:
                dyad_type = "secondary"
            elif comb in tertiary_dyads or tuple(reversed(comb)) in tertiary_dyads:
                dyad_type = "tertiary"
            elif comb in opposite_dyads or tuple(reversed(comb)) in opposite_dyads:
                dyad_type = "opposite"
            else:
                dyad_type = "unknown"
            return [(dyad_type, dyad_emotion)]
    return []

# Load the CSV file from Preprocessed folder
preprocessed_csv_path = "songs/preprocessed/songs_to_be_added.csv"
df_preprocessed = pd.read_csv(preprocessed_csv_path)

# Loop through all text files in lyrics folder
lyrics_folder = "songs/lyrics"
processed_folder = "songs/processed"
for filename in os.listdir(lyrics_folder):
    if filename.endswith(".txt"):
        # Extract video_id from filename
        video_id = filename.split(".")[0]

        # Load lyrics
        with open(os.path.join(lyrics_folder, filename), "r", encoding="utf-8") as file:
            lyrics = file.read()

        # Tokenize and Analyze Lyrics
        inputs = tokenizer(lyrics, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        predictions = outputs.logits.softmax(dim=-1)

        # Map Predictions to Emotions
        emotion_labels = [
            "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire",
            "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
            "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness",
            "surprise", "neutral"
        ]

        # Select top 2 predicted emotions
        predicted_emotions = [emotion_labels[i] for i in predictions[0].topk(2).indices]
        print(f"Predicted Emotions: {predicted_emotions}")

        # Classify predicted emotions into Plutchik's 8 primary classes
        classified_emotions = classify_emotions(predicted_emotions)
        print(f"Classified Emotions: {classified_emotions}")

        # Generate emotion combinations based on primary classes
        emotion_combinations = generate_emotion_combinations(classified_emotions)
        print(f"Emotion Combinations: {emotion_combinations}")

        # Map Dyads results to 28 primary emotions
        dyad_to_emotion_map = {
            "love": "love", "submission": "caring", "alarm": "fear", "disappointment": "disappointment",
            "remorse": "remorse", "contempt": "disapproval", "aggression": "anger", "optimism": "optimism",
            "guilt": "remorse", "curiosity": "curiosity", "despair": "grief", "unbelief": "confusion",
            "envy": "annoyance", "cynicism": "disapproval", "pride": "pride", "hope": "optimism",
            "delight": "excitement", "sentimentality": "admiration", "shame": "embarrassment", "outrage": "anger",
            "pessimism": "sadness", "morbidness": "disgust", "dominance": "pride", "anxiety": "nervousness",
            "bittersweetness": "sadness", "ambivalence": "confusion", "frozenness": "fear", "confusion": "confusion",
            # Uniform emotions mapped to themselves
            "anger": "anger", "anticipation": "optimism", "joy": "joy", "trust": "admiration",
            "fear": "fear", "surprise": "surprise", "sadness": "sadness", "disgust": "disgust"
        }

        # Modify the logic for determining the final emotion
        final_emotion = None
        if emotion_combinations:
            # Map Dyads results to 28 primary emotions
            dyad_emotion = emotion_combinations[0][1]  # # Dyads result emotion
            final_emotion = dyad_to_emotion_map.get(dyad_emotion, "neutral")  # Map to one of the 28 primary emotions
        else:
            # If there are no Dyads results, use the last primary emotion
            final_emotion = classified_emotions[-1]

        print(f"Final Emotion: {final_emotion} (Color: {emotion_to_color.get(final_emotion, '#000000')})")

        # Use Final Emotion as Determined Final Emotion
        determined_final_emotion = final_emotion
        print(f"Determined Final Emotion: {determined_final_emotion}")

        # Find the video information in the preprocessed DataFrame
        video_info = df_preprocessed[df_preprocessed['video_id'] == video_id]

        if not video_info.empty:
            # Extract the necessary columns
            video_data = video_info[['video_id', 'track_name', 'artist_name', 'release_year', 'duration_ms']]

            # Determine the processed CSV file path based on the final emotion
            processed_csv_path = os.path.join(processed_folder, f"{determined_final_emotion}.csv")

            # Append the video data to the corresponding emotion CSV file
            if os.path.exists(processed_csv_path):
                df_processed = pd.read_csv(processed_csv_path)
            else:
                df_processed = pd.DataFrame(columns=video_data.columns)

            # Debugging Log: Checking Final Emotion Path
            print(f"Saving to Path: {processed_csv_path}")

            df_processed = pd.concat([df_processed, video_data], ignore_index=True)

            # Drop duplicates and save the updated DataFrame back to the CSV file
            df_processed = df_processed.drop_duplicates(subset=['video_id'], keep='first')
            df_processed.to_csv(processed_csv_path, index=False)

            # Remove the lyrics text file after processing
            os.remove(os.path.join(lyrics_folder, filename))

            # Remove the corresponding row from the preprocessed DataFrame
            df_preprocessed = df_preprocessed[df_preprocessed['video_id'] != video_id]

# Save the updated preprocessed DataFrame
df_preprocessed.to_csv(preprocessed_csv_path, index=False)

print("Lyrics processing complete. Processed files have been updated with duplicates removed.")
