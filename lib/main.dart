import 'package:flutter/material.dart';
import 'start_page.dart';
import 'question_page.dart';
import 'loading_page.dart';
import 'playlist_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MoodWave',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const StartPage(),
        '/question': (context) => const QuestionPage(),
        '/loading': (context) {
          final args = ModalRoute.of(context)!.settings.arguments as String;
          return LoadingPage(selectedEmotion: args);
        },
        '/playlist': (context) {
          final args = ModalRoute.of(context)!.settings.arguments as String;
          return PlaylistPage(selectedEmotion: args);
        },
      },
    );
  }
}

class StartPage extends StatelessWidget {
  const StartPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.deepPurple[50], // Set the color you want here

        title: const Text('MoodWave'),
        centerTitle: true,
        leading: IconButton(
          icon: const Icon(Icons.refresh),
          onPressed: () {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => const StartPage()),
            );
          },
        ),
      ),
      body: Container(
        color: Colors.deepPurple[50],
        child: Center(
          child: GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                PageRouteBuilder(
                  pageBuilder: (context, animation, secondaryAnimation) {
                    return QuestionPage(); // The page you want to navigate to
                  },
                  transitionsBuilder:
                      (context, animation, secondaryAnimation, child) {
                    var begin = Offset(1.0, 0.0); // Start from the right
                    var end = Offset.zero; // End at the current position
                    var curve = Curves.easeInOut;

                    var tween = Tween(begin: begin, end: end)
                        .chain(CurveTween(curve: curve));
                    var offsetAnimation = animation.drive(tween);

                    return SlideTransition(
                        position: offsetAnimation, child: child);
                  },
                ),
              );
            },
            child: Container(
              child: Column(
                mainAxisAlignment:
                    MainAxisAlignment.center, // Centers content vertically
                children: [
                  const Text(
                    'Welcome to MoodWave!',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.deepPurple,
                    ),
                  ),
                  const SizedBox(
                      height: 10), // Space between title and subtitle
                  const Padding(
                    padding: EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 20), // Adds left and right padding
                    child: SizedBox(
                      width: 300, // Max width for better readability
                      child: Text(
                        'Select a color, and we’ll find the perfect playlist for your mood.',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.black54,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 20), // Space between text and button
                  SizedBox(
                    width: 200, // Button width
                    height: 50, // Button height
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          PageRouteBuilder(
                            pageBuilder:
                                (context, animation, secondaryAnimation) {
                              return QuestionPage(); // The page you want to navigate to
                            },
                            transitionsBuilder: (context, animation,
                                secondaryAnimation, child) {
                              var begin =
                                  Offset(1.0, 0.0); // Start from the right
                              var end =
                                  Offset.zero; // End at the current position
                              var curve = Curves.easeInOut;

                              var tween = Tween(begin: begin, end: end)
                                  .chain(CurveTween(curve: curve));
                              var offsetAnimation = animation.drive(tween);

                              return SlideTransition(
                                  position: offsetAnimation, child: child);
                            },
                          ),
                        );
                      },
                      child: const Text('Start'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
