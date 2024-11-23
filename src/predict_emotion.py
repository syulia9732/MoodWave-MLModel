import os
import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load Pre-trained Model
tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")

# Emotion Labels from GoEmotions
emotion_labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity",
    "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear",
    "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization",
    "relief", "remorse", "sadness", "surprise"
]

# Directories
lyrics_folder = "songs/lyrics"
processed_folder = "songs/processed"

# Sample Song Data (in real usage, this would be dynamically populated or read from another source)
song_data = [
    {
        "ID": "00Ausvcr9Dp9vsgS5zvXm4",
        "Song Name": "Sample Song",
        "Artist Name": "Sample Artist",
        "Album Cover": "https://example.com/album_cover.jpg"
    }
]

# Function to check if an ID already exists in the CSV
def id_exists_in_csv(file_path, song_id):
    if not os.path.exists(file_path):
        return False
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["ID"]) == song_id:
                return True
    return False

# Process Each Song
for song in song_data:
    song_id = song["ID"]
    lyrics_path = os.path.join(lyrics_folder, f"{song_id}.txt")

    try:
        # Read lyrics from file
        with open(lyrics_path, "r", encoding="utf-8") as file:
            lyrics = file.read().strip()

        # Predict emotion
        inputs = tokenizer(lyrics, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        predictions = outputs.logits.softmax(dim=-1)

        # Get top predicted emotion
        top_emotion_index = predictions[0].argmax().item()
        top_emotion = emotion_labels[top_emotion_index]

        # Path to the designated emotion file
        emotion_file_path = os.path.join(processed_folder, f"{top_emotion}.csv")

        # Check if the ID already exists
        if id_exists_in_csv(emotion_file_path, song_id):
            print(f"Song ID {song_id} already exists in '{top_emotion}.csv'. Skipping.")
            continue

        # Write to the corresponding emotion file
        file_exists = os.path.exists(emotion_file_path)
        with open(emotion_file_path, mode="a", newline="", encoding="utf-8") as emotion_file:
            writer = csv.writer(emotion_file)
            if not file_exists:
                # Write header if the file does not exist
                writer.writerow(["ID", "Song Name", "Artist Name", "Album Cover"])

            # Write song data
            writer.writerow([song["ID"], song["Song Name"], song["Artist Name"], song["Album Cover"]])

        print(f"Song '{song['Song Name']}' categorized under emotion: {top_emotion}")

    except FileNotFoundError:
        print(f"Lyrics file not found for ID {song_id}")
    except Exception as e:
        print(f"Error processing song ID {song_id}: {e}")
