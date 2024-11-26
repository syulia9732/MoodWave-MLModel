# pip install spotipy pandas

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# Spotify API 인증
CLIENT_ID = '8bad33795b9241f3876baf946041b13e'  # Replace with your Spotify Client ID
CLIENT_SECRET = '17acde4c11784220991c4079da4149bf'  # Replace with your Spotify Client Secret

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 검색 파라미터
START_YEAR = 2014
END_YEAR = 2024
LANGUAGE = 'en'  # Note: Spotify API does not provide direct language filtering.

# 데이터 저장 경로
CSV_FILE_PATH = "songs/preprocessed/songs_to_be_added.csv"

# 컬럼명
columns = ['track_id', 'track_name', 'artist_name', 'release_year', 'mode', 'tempo', 'duration_ms']

# 데이터 저장 리스트
song_data = []

def get_audio_features(track_id):
    """Fetch audio features for a track ID."""
    try:
        features = sp.audio_features(track_id)[0]
        return features
    except Exception as e:
        print(f"Error fetching audio features for track {track_id}: {e}")
        return None

def fetch_tracks(year):
    """Fetch tracks for a specific year."""
    query = f"year:{year}"  # Filter by year
    results = sp.search(q=query, type='track', limit=50, offset=0)

    for track in results['tracks']['items']:
        track_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        release_date = track['album']['release_date']
        release_year = int(release_date.split('-')[0])

        # Get audio features
        features = get_audio_features(track_id)
        if features:
            song_data.append([
                track_id,
                track_name,
                artist_name,
                release_year,
                features['mode'],
                features['tempo'],
                features['duration_ms']
            ])

def main():
    print(f"Fetching songs from {START_YEAR} to {END_YEAR}...")
    for year in range(START_YEAR, END_YEAR + 1):
        print(f"Fetching songs for year {year}...")
        try:
            fetch_tracks(year)
            time.sleep(1)  # Avoid hitting rate limits
        except Exception as e:
            print(f"Error fetching songs for year {year}: {e}")

    # Save to CSV
    print(f"Saving data to {CSV_FILE_PATH}...")
    df = pd.DataFrame(song_data, columns=columns)
    df.to_csv(CSV_FILE_PATH, index=False)
    print(f"Data saved successfully to {CSV_FILE_PATH}")

if __name__ == "__main__":
    main()


# header = ["ID", "Song Name", "Artist Name", "Album Cover", "Features"]


# sample_data = [
#     "00Ausvcr9Dp9vsgS5zvXm4",  # ID
#     "Sample Song",  # Song Name
#     "Sample Artist",  # Artist Name
#     "https://example.com/album_cover.jpg",  # Album Cover URL
#     '{"tempo": 120, "mode": "major"}'  # Features as JSON string
# ]

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
