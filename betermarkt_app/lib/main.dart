import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:betermarkt_app/hex_to_color.dart';

void main() {
  runApp(const MyApp());
}

String webPage = "https://betermarkt.streamlit.app/";

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BeterMarkt',
      home: const MyHomePage(title: 'BeterMarkt'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late final WebViewController controller;

  @override
  void initState() {
    super.initState();
    controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (String url) {
            print("Page started: $url");
          },
          onPageFinished: (String url) {
            print("Page finished: $url");
          },
          onWebResourceError: (WebResourceError error) {
            print("Error: $error");
          },
        ),
      )
      ..loadRequest(Uri.parse(webPage)); // Replace with your webpage
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 7,
        centerTitle: true,
        backgroundColor: hexToColor("#0e1116"),

        title: Text(
          "BeterMarkt",
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 27,
            color: hexToColor("#FFFFFF"),
          ),
        ),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(3.0),
          child: Container(color: hexToColor("#ff4b4b"), height: 3.0), // Line
        ),
      ),
      body: WebViewWidget(controller: controller),
    );
  }
}
