import 'package:flutter/material.dart';

class LoadingPage extends StatefulWidget {
  final String selectedEmotion;

  const LoadingPage({super.key, required this.selectedEmotion});

  @override
  _LoadingPageState createState() => _LoadingPageState();
}

class _LoadingPageState extends State<LoadingPage> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 3), () {
      Navigator.pushNamed(
        context,
        '/playlist',
        arguments: widget.selectedEmotion, // Pass emotion ID to PlaylistPage
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            CircularProgressIndicator(),
            SizedBox(height: 20),
            Text('Looking for recommended songs...'),
          ],
        ),
      ),
    );
  }
}