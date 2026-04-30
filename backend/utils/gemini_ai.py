import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_emotional_response(
    user_message: str, 
    history_summary: str = "", 
    recent_stress_levels: list = [], 
    input_type: str = "text",
    behavior_summary: dict = None,
    pattern_summary: dict = None
) -> dict:
    """
    Send the user's masked message and context to Google Gemini AI.
    Returns the exact JSON structure required by StressCare.
    """
    if not GEMINI_API_KEY:
        return get_fallback_response(user_message)
    
    try:
        model_name = 'models/gemini-2.5-flash'
        model = genai.GenerativeModel(model_name)
        print("USING MODEL:", model_name)
        
        # Safe System Prompt version
        system_instruction = (
            "You are StressCare, an emotionally intelligent and observant caregiver assistant.\n\n"
            "You MUST analyze:\n"
            "1. User message\n"
            "2. behavior_summary\n"
            "3. pattern_summary\n\n"
            "IMPORTANT RULES:\n"
            "If pattern_summary.repeated_pattern == true:\n"
            "You MUST acknowledge that the user has been feeling this way for a while.\n\n"
            "If pattern_summary.increasing_stress == true:\n"
            "You MUST mention that stress seems to be increasing.\n\n"
            "If pattern_summary.high_risk == true:\n"
            "You MUST warn about possible burnout.\n\n"
            "If pattern_summary.fatigue_cycle == true:\n"
            "You MUST mention consistent tiredness.\n\n"
            "If multiple conditions are true:\n"
            "Combine them naturally in a human way.\n\n"
            "CRITICAL SAFETY RULE:\n"
            "If user message contains phrases like:\n"
            "I can't do this anymore, I give up, I feel mentally drained, I am exhausted\n"
            "You MUST respond with high concern and support.\n"
            "NEVER classify as neutral.\n\n"
            "Tone rules:\n"
            "Be human, supportive, and calm.\n"
            "Be more serious when risk is high.\n"
            "Do not ignore patterns.\n\n"
            "Return ONLY valid JSON.\n"
            "Do NOT include markdown.\n"
            "Do NOT include extra text.\n"
            "Return EXACTLY this structure:\n"
            "{\n"
            "  \"message\": \"<empathetic response>\",\n"
            "  \"stress_level\": \"low | medium | high\",\n"
            "  \"burnout_score\": <integer 0-100>,\n"
            "  \"emotion\": \"stress | fatigue | neutral | happiness | sadness | anger | fear | surprise | disgust | anxiety | frustration | calmness | engagement\",\n"
            "  \"suggestion\": \"<short helpful suggestion>\",\n"
            "  \"actions\": [],\n"
            "  \"intent\": \"normal\"\n"
            "}"
        )

        print("BEHAVIOR CONTEXT SENT:", behavior_summary)
        input_data = {
            "message": user_message,
            "history_summary": history_summary,
            "recent_stress_levels": recent_stress_levels,
            "behavior_summary": behavior_summary,
            "pattern_summary": pattern_summary,
            "input_type": input_type
        }

        prompt = f"System Instruction: {system_instruction}\n\nInput Context: {json.dumps(input_data)}"
        
        print(f"--- GEMINI REQUEST (Model: {model_name}) ---\nPrompt: {prompt}\n-----------------------")
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        print(f"--- GEMINI RESPONSE ---\nText: {text}\n------------------------")
        
        raw_response = response.text.strip()
        print(f"RAW GEMINI RESPONSE: {raw_response}")
        
        # Clean the response to ensure valid JSON (remove markdown code blocks manually)
        json_text = raw_response
        json_text = json_text.replace("```json", "").replace("```", "").strip()
            
        try:
            ai_result = json.loads(json_text)
            print(f"PARSED JSON: {ai_result}")
        except Exception as json_err:
            print(f"JSON PARSE ERROR: {json_err}")
            print(f"RAW GEMINI RESPONSE FOR DEBUG: {raw_response}")
            return get_fallback_response(user_message)
        
        # Validate and normalize fields
        valid_emotions = ["stress", "fatigue", "neutral", "happiness", "sadness", "anger", "fear", "surprise", "disgust", "anxiety", "frustration", "calmness", "engagement"]
        ai_result["emotion"] = ai_result.get("emotion", "neutral").lower()
        if ai_result["emotion"] not in valid_emotions:
            ai_result["emotion"] = "neutral"
            
        ai_result["message"] = ai_result.get("message", ai_result.get("response", ""))
        ai_result["stress_level"] = ai_result.get("stress_level", "low").lower()
        ai_result["burnout_score"] = ai_result.get("burnout_score", 30)
        ai_result["intent"] = ai_result.get("intent", "normal")
        
        print(f"DETECTED EMOTION: {ai_result['emotion']}")
            
        return ai_result
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            print(f"!!! GEMINI QUOTA EXHAUSTED !!!: {error_msg}")
        else:
            print(f"!!! GEMINI ERROR !!!: {error_msg}")
        # Return a structured error response that routes to fallback
        return get_fallback_response(user_message)


def get_fallback_response(user_message: str) -> dict:
    """
    Intelligent keyword-based fallback system for StressCare.
    Ensures a valid response even if Gemini is unavailable.
    """
    msg_lower = user_message.lower()
    
    # 🔍 KEYWORD-BASED EMOTION DETECTION
    emotion = "neutral"
    if any(w in msg_lower for w in ["sleep", "tired", "exhausted", "sleepy", "energy"]):
        emotion = "fatigue"
    elif any(w in msg_lower for w in ["stress", "pressure", "overwhelmed", "anxious", "tension"]):
        emotion = "stress"
    elif any(w in msg_lower for w in ["happy", "good", "excited", "joy"]):
        emotion = "happiness"
    elif any(w in msg_lower for w in ["sad", "upset", "unhappy", "cry"]):
        emotion = "sadness"
    elif any(w in msg_lower for w in ["angry", "annoyed", "irritated", "hate"]):
        emotion = "anger"
    elif any(w in msg_lower for w in ["worried", "nervous", "anxiety", "fear"]):
        emotion = "anxiety"
    elif any(w in msg_lower for w in ["calm", "relaxed", "peaceful"]):
        emotion = "calmness"
    
    print(f"FALLBACK EMOTION USED: {emotion}")
    
    # Keyword detection for dynamic demo feel
    if emotion == "stress" or any(w in msg_lower for w in ["overwhelmed", "can't handle", "panic", "suicide", "hurt"]):
        return {
            "emotion": "stress",
            "message": "I'm so sorry you're feeling this way. Please know that you're not alone, and it's okay to ask for help when things feel like too much.",
            "stress_level": "high",
            "burnout_score": 85,
            "suggestion": "Take a moment to sit down and focus on your breath. If you're feeling unsafe, please reach out to someone you trust immediately.",
            "actions": [{"label": "Emergency Contacts", "type": "task"}],
            "intent": "crisis"
        }
    
    if emotion == "stress" or any(w in msg_lower for w in ["stress", "busy", "work", "pressure", "exam"]):
        return {
            "emotion": "stress",
            "message": "It sounds like you have a lot on your plate right now. It's completely natural to feel a bit stretched during busy times.",
            "stress_level": "medium",
            "burnout_score": 60,
            "suggestion": "Try breaking your tasks into smaller, manageable steps. Taking a 5-minute walk might also help clear your mind.",
            "actions": [{"label": "Plan my day", "type": "task"}],
            "intent": "normal"
        }
        
    if emotion == "fatigue" or any(w in msg_lower for w in ["sleep", "tired", "exhausted", "rest"]):
        return {
            "emotion": "fatigue",
            "message": "I hear you. It sounds like you might be feeling a bit tired today. Sleep is so important for our well-being.",
            "stress_level": "low",
            "burnout_score": 35,
            "suggestion": "Try to take a short rest or drink some water. Even a small 15-minute break can make a big difference.",
            "actions": [],
            "intent": "normal"
        }

    if emotion == "happiness":
        return {
            "emotion": "happiness",
            "message": "I'm so glad to hear that you're having a good day! Positive energy is wonderful.",
            "stress_level": "low",
            "burnout_score": 15,
            "suggestion": "Take a moment to truly savor this feeling. You deserve this happiness!",
            "actions": [],
            "intent": "normal"
        }
    
    if emotion == "sadness":
        return {
            "emotion": "sadness",
            "message": "I'm here for you. It's okay to feel down sometimes, and I'm listening if you want to share more.",
            "stress_level": "low",
            "burnout_score": 40,
            "suggestion": "Be gentle with yourself today. Maybe listen to some comforting music or have a warm drink.",
            "actions": [],
            "intent": "normal"
        }

    if emotion == "anger":
        return {
            "emotion": "anger",
            "message": "It sounds like you're feeling quite frustrated or angry. It's important to acknowledge those feelings.",
            "stress_level": "medium",
            "burnout_score": 50,
            "suggestion": "Try taking a few deep breaths or stepping away from the situation for a moment to cool down.",
            "actions": [],
            "intent": "normal"
        }

    if emotion == "anxiety":
        return {
            "emotion": "anxiety",
            "message": "I can tell you're feeling a bit anxious or worried. Let's take things one step at a time.",
            "stress_level": "medium",
            "burnout_score": 55,
            "suggestion": "Try the 5-4-3-2-1 grounding technique: notice 5 things you see, 4 you can touch, 3 you hear, 2 you smell, and 1 you can taste.",
            "actions": [],
            "intent": "normal"
        }

    if emotion == "calmness":
        return {
            "emotion": "calmness",
            "message": "It's wonderful that you're feeling calm and peaceful right now. That's a great state to be in.",
            "stress_level": "low",
            "burnout_score": 10,
            "suggestion": "Enjoy this tranquility. It's a perfect time for some light reading or meditation.",
            "actions": [],
            "intent": "normal"
        }

    # Default fallback
    return {
        "emotion": "neutral",
        "message": "Thank you for sharing that with me. I'm here to listen and support you in any way I can. 💙",
        "stress_level": "low",
        "burnout_score": 20,
        "suggestion": "Maybe take a few deep breaths and tell me more about what's on your mind?",
        "actions": [],
        "intent": "normal"
    }