import datetime
from config.database import db
# Collections
chats = db["chats"]
behavior_logs = db["behavior_logs"]

STRESS_KEYWORDS = ["stress", "tired", "exhausted", "pressure", "overwhelmed"]

def analyze_user_behavior(user_id: str, current_message: str) -> dict:
    """
    Analyze user interaction patterns to detect hidden stress signals.
    Returns flags and a combined behavior score.
    """
    now = datetime.datetime.utcnow()
    
    # 1. Late Night Activity (12:00 AM - 5:00 AM)
    # Note: Using UTC for now, but in a real app we'd use user's local timezone
    # For this hackathon, we'll assume UTC or just check current hour
    current_hour = now.hour
    late_night_activity = 0 <= current_hour <= 5
    
    # Fetch recent history (last 10 messages)
    recent_history = list(chats.find({"user_id": user_id}).sort("created_at", -1).limit(10))
    
    # 2. Repeated Stress Signals
    stress_count = 0
    msg_lower = current_message.lower()
    if any(k in msg_lower for k in STRESS_KEYWORDS):
        stress_count += 1
        
    for chat in recent_history:
        prev_msg = chat.get("user_message", "").lower()
        if any(k in prev_msg for k in STRESS_KEYWORDS):
            stress_count += 1
            
    repeated_stress = stress_count >= 3 # Threshold: 3 occurrences in last 11 messages
    
    # 3. Reduced Activity
    # Check if there was a long gap between last message and this one
    low_activity = False
    if recent_history:
        last_chat_time = recent_history[0].get("created_at")
        if last_chat_time:
            time_gap = (now - last_chat_time).days
            if time_gap >= 3: # Gap of 3+ days
                low_activity = True
                
    # Behavior Score Logic
    behavior_score = 0
    if late_night_activity: behavior_score += 30
    if repeated_stress: behavior_score += 40
    if low_activity: behavior_score += 30
    
    result = {
        "late_night_activity": late_night_activity,
        "repeated_stress": repeated_stress,
        "low_activity": low_activity,
        "behavior_score": behavior_score
    }
    
    # 4. Store Behavior Log
    try:
        behavior_logs.insert_one({
            "user_id": user_id,
            "timestamp": now,
            "behavior_score": behavior_score,
            "flags": {
                "late_night_activity": late_night_activity,
                "repeated_stress": repeated_stress,
                "low_activity": low_activity
            }
        })
    except Exception as e:
        print(f"Error storing behavior log: {e}")
        
    print(f"BEHAVIOR ANALYSIS: {result}")
    print(f"BEHAVIOR SCORE: {behavior_score}")
    
    return result
