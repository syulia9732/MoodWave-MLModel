import 'package:flutter/material.dart';
import 'start_page.dart';

class PlaylistPage extends StatelessWidget {
  const PlaylistPage({super.key});

  @override
  Widget build(BuildContext context) {
    List<Map<String, String>> songs = [
      {"title": "Song 1", "artist": "Artist 1", "cover": "https://via.placeholder.com/150"},
      {"title": "Song 2", "artist": "Artist 2", "cover": "https://via.placeholder.com/150"},
      {"title": "Song 3", "artist": "Artist 3", "cover": "https://via.placeholder.com/150"},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Recommended Playlist'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pushAndRemoveUntil(
              context,
              MaterialPageRoute(builder: (context) => const StartPage()), 
              (route) => false,
            );
          },
        ),
      ),
      body: ListView.builder(
        itemCount: songs.length,
        itemBuilder: (context, index) {
          return ListTile(
            leading: Image.network(songs[index]["cover"]!),
            title: Text(songs[index]["title"]!),
            subtitle: Text(songs[index]["artist"]!),
          );
        },
      ),
    );
  }
}
