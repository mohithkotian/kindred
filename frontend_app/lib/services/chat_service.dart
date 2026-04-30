import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ChatService {
  static const String baseUrl = "http://127.0.0.1:8000";

  // 📤 SEND MESSAGE TO BACKEND
  static Future<Map<String, dynamic>> sendMessage({
    required String message,
    required bool ghostMode,
    String session_id = "default",
    String inputType = "text",
  }) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("auth_token");

    final res = await http.post(
      Uri.parse("$baseUrl/chat/message"),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
      body: jsonEncode({
        "message": message,
        "session_id": session_id,
        "ghost_mode": ghostMode,
        "input_type": inputType,
      }),
    );
    
    final decodedBody = utf8.decode(res.bodyBytes);
    final data = jsonDecode(decodedBody);
    print("API RESPONSE: $data");
    return data;
  }

  // 🔒 UPDATE PRIVACY STATUS
  static Future<Map<String, dynamic>> updatePrivacy({
    required String chatId,
    required bool isPrivate,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("auth_token");

    final res = await http.put(
      Uri.parse("$baseUrl/chat/privacy"),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
      body: jsonEncode({
        "chat_id": chatId,
        "is_private": isPrivate,
      }),
    );
    return jsonDecode(utf8.decode(res.bodyBytes));
  }

  // 💾 GET CHAT HISTORY
  static Future<List<dynamic>> getChatHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("auth_token");

    final res = await http.get(
      Uri.parse("$baseUrl/chat/history"),
      headers: {
        "Authorization": "Bearer $token",
      },
    );
    
    final decodedBody = utf8.decode(res.bodyBytes);
    final data = jsonDecode(decodedBody);
    return data["messages"] ?? [];
  }

  // 🗑️ CLEAR CHAT HISTORY
  static Future<Map<String, dynamic>> clearChatHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("auth_token");

    final res = await http.delete(
      Uri.parse("$baseUrl/chat/history"),
      headers: {
        "Authorization": "Bearer $token",
      },
    );
    final decodedBody = utf8.decode(res.bodyBytes);
    return jsonDecode(decodedBody);
  }

  // 📊 GET STRESS TRENDS
  static Future<List<dynamic>> getStressTrends() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("auth_token");

    final res = await http.get(
      Uri.parse("$baseUrl/chat/stress-trends"),
      headers: {
        "Authorization": "Bearer $token",
      },
    );
    
    final decodedBody = utf8.decode(res.bodyBytes);
    final data = jsonDecode(decodedBody);
    return data["trends"] ?? [];
  }
}