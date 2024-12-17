import lyricsgenius

def get_lyrics(song_title, artist_name, access_token):
    genius = lyricsgenius.Genius(access_token)

    try:
        song = genius.search_song(title=song_title, artist=artist_name)
        if song:
            return song.lyrics
        else:
            return "Lyrics not found."
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Example usage
access_token = "lDzAKQfbvLpHTyRQdING6F-YBpSgRlVmQKLjyTUGmDaiQa7OsQfnSse8R0AJeNFKk5TQQT7oe6H1dkBlraLehg"  # Replace with your Genius API access token
track_name = "HUMBLE."
artist_name = "Kendrick Lamar"




lyrics = get_lyrics(track_name, artist_name, access_token)
print("Track name:", track_name)
print("Artist name:", artist_name)
print(lyrics)


