import csv
import os

# Define the file path for the CSV
csv_file_path = "songs/preprocessed/songs_to_be_added.csv"

# Define the header
header = ["ID", "Song Name", "Artist Name", "Album Cover", "Features"]

# Sample data with dynamic lyrics fetching based on ID
sample_data = [
    "00Ausvcr9Dp9vsgS5zvXm4",  # ID
    "Sample Song",  # Song Name
    "Sample Artist",  # Artist Name
    "https://example.com/album_cover.jpg",  # Album Cover URL
    None,  # Placeholder for Lyrics (will be dynamically fetched)
    '{"tempo": 120, "mode": "major"}'  # Features as JSON string
]

# Fetch lyrics from the lyrics folder based on ID
# lyrics_folder_path = "songs/lyrics"
# lyrics_file_path = os.path.join(lyrics_folder_path, f"{sample_data[0]}.txt")  # Use ID to find the file

# try:
#     with open(lyrics_file_path, "r", encoding="utf-8") as lyrics_file:
#         lyrics = lyrics_file.read().strip()  # Read and strip extra whitespace
#         sample_data[4] = lyrics  # Set lyrics in the sample_data
# except FileNotFoundError:
#     print(f"Lyrics file not found for ID {sample_data[0]}")
#     sample_data[4] = "Lyrics not available"  # Fallback if file doesn't exist

# Check if the file already exists
file_exists = os.path.exists(csv_file_path)

# Open the CSV file in append mode
with open(csv_file_path, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write the header only if the file does not exist
    if not file_exists:
        writer.writerow(header)

    # Write the sample data
    writer.writerow(sample_data)

print(f"Sample data successfully added to {csv_file_path}")
