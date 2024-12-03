from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_id):
    try:
        # Fetch the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        # Combine the transcript into a single string
        lyrics = "\n".join([t['text'] for t in transcript])
        return lyrics
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

# Example usage
video_id = "YQHsXMglC9A"  # Replace with the YouTube video ID
lyrics = get_youtube_transcript(video_id)
print("Extracted Lyrics:\n", lyrics)


import requests

def search_youtube_video(track_name, artist_name, api_key):
    """Search for a YouTube video using track and artist name."""
    base_url = "https://www.googleapis.com/youtube/v3/search"
    query = f"{track_name} {artist_name}"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'key': api_key,
        'maxResults': 1  # Get the top result
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results['items']:
            video_id = results['items'][0]['id']['videoId']
            video_title = results['items'][0]['snippet']['title']
            return video_id, video_title
        else:
            print("No results found.")
            return None, None
    else:
        print("YouTube API error:", response.status_code, response.text)
        return None, None

# Example usage
api_key = "AIzaSyCkWxMdc5vk42sHGsH6hzLBvCTuITAGej4"  # Replace with your YouTube Data API Key
track_name = "Rolling in the Deep"
artist_name = "Adele"

video_id, video_title = search_youtube_video(track_name, artist_name, api_key)
if video_id:
    print(f"Video ID: {video_id}")
    print(f"Video Title: {video_title}")
else:
    print("No video found.")
