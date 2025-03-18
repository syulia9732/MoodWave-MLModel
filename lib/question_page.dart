import 'package:flutter/material.dart';

class QuestionPage extends StatefulWidget {
  const QuestionPage({super.key});

  @override
  _QuestionPageState createState() => _QuestionPageState();
}

class _QuestionPageState extends State<QuestionPage> {
  String? selectedEmotionId;
  Color? selectedColor;

  final List<Map<String, dynamic>> emotions = [
    {
      "id": "joy",
      "label": "I feel my soul dancing 🌞",
      "color": Color(0xFFFFD700)
    }, // Bright Yellow
    {
      "id": "anger",
      "label": "I'm pissed 🔥",
      "color": Color(0xFFD32F2F)
    }, // Fiery Red
    {
      "id": "caring",
      "label": "I'm loved 💗",
      "color": Color(0xFFFFB6C1)
    }, // Soft Pink
    {
      "id": "desire",
      "label": "I wish they were mine ❤️‍🔥",
      "color": Color(0xFFB22222)
    }, // Deep Crimson
    {
      "id": "disappointment",
      "label": "I feel let down 😞",
      "color": Color(0xFF708090)
    }, // Muted Gray-Blue
    {
      "id": "embarrassment",
      "label": "I'm so embarassed 😳",
      "color": Color(0xFFFF6F61)
    }, // Blush Pink
    {
      "id": "excitement",
      "label": "I’m so excited! 🤩",
      "color": Color(0xFFFF4500)
    }, // Electric Orange
    {
      "id": "fear",
      "label": "I’m having a panic attack 😨",
      "color": Color(0xFF4B0082)
    }, // Dark Purple
    {
      "id": "gratitude",
      "label": "I feel grateful:) 😊",
      "color": Color(0xFFFFD700)
    }, // Warm Goldenrod
    {
      "id": "pride",
      "label": "I feel strong and capable 💪",
      "color": Color(0xFF4169E1)
    }, // Bold Royal Blue
    {
      "id": "relief",
      "label": "This moment feels peaceful 😌",
      "color": Color(0xFFC1D9C2)
    }, // Desaturated Mint
    {
      "id": "remorse",
      "label": "I can’t forgive myself 😔",
      "color": Color(0xFF008080)
    }, // Deep Teal
    {
      "id": "sadness",
      "label": "I feel like I'm sinking 😢",
      "color": Color(0xFF1E3A5F)
    }, // Deep Navy Blue
  ];

  Widget _buildColorButton(Map<String, dynamic> emotion) {
    return GestureDetector(
      onTap: () {
        setState(() {
          selectedEmotionId = emotion["id"];
          selectedColor = emotion["color"];
        });
      },
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
        decoration: BoxDecoration(
          color: emotion["color"],
          borderRadius: BorderRadius.circular(20), // Smooth rounded edges
          border: Border.all(
            color: selectedEmotionId == emotion["id"] ? Colors.black : Colors.transparent,
            // width: 3,
          ),
        ),
        child: Center(
          child: Text(
            emotion["label"],
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Please select a color')),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 50),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Center(
              child: Wrap(
                alignment: WrapAlignment.center,
                spacing: 12,
                runSpacing: 12,
                children: emotions
                    .map((emotion) => _buildColorButton(emotion))
                    .toList(),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: selectedColor != null
                  ? () {
                      Navigator.pushNamed(context, '/loading',
                          arguments: selectedEmotionId);
                    }
                  : null,
              child: const Text('Next'),
            ),
          ],
        ),
      ),
    );
  }
}
