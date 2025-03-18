import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:csv/csv.dart';
import 'package:url_launcher/url_launcher.dart';
import 'start_page.dart';

class PlaylistPage extends StatefulWidget {
  final String selectedEmotion; // Required parameter for selected emotion

  const PlaylistPage({super.key, required this.selectedEmotion});

  @override
  _PlaylistPageState createState() => _PlaylistPageState();
}

class _PlaylistPageState extends State<PlaylistPage> {
  List<Map<String, String>> songs = [];
  bool isLoading = true;
  String errorMessage = '';
  late String accessToken; // Spotify API Access Token

  @override
  void initState() {
    super.initState();
    print('Selected Emotion: ${widget.selectedEmotion}');
    fetchAccessToken().then((_) => fetchSongs());
  }

  // Fetch Access Token from Spotify API
  Future<void> fetchAccessToken() async {
    const clientId = 'f7f0d7ce99c94fc2a29b6cb4cb570b0b'; // Your Client ID
    const clientSecret = '3bed7ba359e1421db4c17ba797f17683'; // Your Client Secret
    const authUrl = 'https://accounts.spotify.com/api/token';

    final response = await http.post(
      Uri.parse(authUrl),
      headers: {
        'Authorization':
            'Basic ${base64Encode(utf8.encode('$clientId:$clientSecret'))}',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {'grant_type': 'client_credentials'},
    );

    print('Spotify Auth Status Code: ${response.statusCode}');
    print('Spotify Auth Response: ${response.body}');

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      accessToken = data['access_token'];
    } else {
      setState(() {
        errorMessage = 'Failed to authenticate with Spotify. Status: ${response.statusCode}';
        isLoading = false;
      });
      throw Exception('Failed to get access token: ${response.body}');
    }
  }

  // Fetch songs using Spotify Track API
  Future<void> fetchSongs() async {
    try {
      final response = await http.get(
        Uri.parse(
          'https://api.github.com/repos/syulia9732/MoodWave-MLModel/contents/songs/processed',
        ),
        headers: {
          'Accept': 'application/vnd.github.v3+json',
        },
      );

      print('GitHub API Status Code: ${response.statusCode}');
      print('GitHub API Response: ${response.body}');

      if (response.statusCode == 200) {
        final List<dynamic> files = json.decode(response.body);

        final targetFile = files.firstWhere(
          (file) => file['name'] == '${widget.selectedEmotion}.csv',
          orElse: () => null,
        );

        if (targetFile == null) {
          setState(() {
            errorMessage = 'No songs found for this emotion.';
            isLoading = false;
          });
          return;
        }

        if (targetFile['size'] == 0) {
          setState(() {
            errorMessage = 'The song list for this emotion is empty.';
            isLoading = false;
          });
          return;
        }

        final csvResponse = await http.get(Uri.parse(targetFile['download_url']));
        if (csvResponse.statusCode == 200) {
          final csvString = utf8.decode(csvResponse.bodyBytes);
          List<List<dynamic>> csvData = const CsvToListConverter().convert(csvString);

          if (csvData.isNotEmpty) csvData.removeAt(0);

          csvData.shuffle();
          final selectedTracks = csvData.take(20).toList();

          for (var track in selectedTracks) {
            String trackId = track[0].toString();

            final trackResponse = await http.get(
              Uri.parse('https://api.spotify.com/v1/tracks/$trackId'),
              headers: {'Authorization': 'Bearer $accessToken'},
            );

            if (trackResponse.statusCode == 200) {
              final trackData = json.decode(trackResponse.body);
              print('Track Data: $trackData');
              songs.add({
                'title': trackData['name'] as String,
                'artist': trackData['artists'][0]['name'] as String,
                'link': trackData['external_urls']['spotify'] as String,
                'image': trackData['album']['images'][0]['url'] as String, // Add album image URL
              });
            } else {
              print('Failed to fetch track: ${trackResponse.statusCode}, ${trackResponse.body}');
            }
          }

          setState(() {
            isLoading = false;
          });
        } else {
          setState(() {
            errorMessage = 'Failed to load CSV file from GitHub.';
            isLoading = false;
          });
        }
      } else {
        setState(() {
          errorMessage = 'Failed to load songs from GitHub. Status: ${response.statusCode}';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error occurred: $e';
        isLoading = false;
      });
    }
  }

  // Function to open Spotify link
  Future<void> _launchSpotifyUrl(String url) async {
    final Uri uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } else {
      setState(() {
        errorMessage = 'Could not launch $url';
      });
      print('Could not launch $url');
    }
  }

  @override
  Widget build(BuildContext context) {
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
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage.isNotEmpty
              ? Center(child: Text(errorMessage))
              : songs.isEmpty
                  ? const Center(child: Text('No songs found for this emotion.'))
                  : ListView.builder(
                      itemCount: songs.length,
                      itemBuilder: (context, index) {
                        return ListTile(
                          leading: Image.network(
                            songs[index]['image']!,
                            width: 50,
                            height: 50,
                            fit: BoxFit.cover,
                          ), // Display album artwork
                          title: Text(songs[index]['title']!),
                          subtitle: Text(songs[index]['artist']!),
                          trailing: IconButton(
                            icon: const Icon(Icons.play_arrow),
                            onPressed: () {
                              _launchSpotifyUrl(songs[index]['link']!);
                            },
                          ),
                        );
                      },
                    ),
    );
  }
}