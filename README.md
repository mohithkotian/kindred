<div align="center">

# 🧠 StressCare
### Passive Caregiver Support & Burnout Detection System

🏆 **2nd Place Winner — SRISHTI Hackathon 2026**  
⏱ Built in 36 Hours  
👥 Team 808 Imperium

[![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)

**Non-intrusive stress detection for informal caregivers — without requiring explicit disclosure.**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</div>

---

# 🏆 SRISHTI Hackathon 2026 — 2nd Prize

> Team **808 Imperium** secured **2nd Place** at **SRISHTI Hackathon 2026**  
> under **Theme 03 — Tech for Healthcare & Well-Being**.

Built during a 36-hour innovation sprint focused on solving real-world caregiver burnout and emotional wellness challenges using AI-powered passive stress detection.

🔗 **Repository:**  
https://github.com/SRISHTI-HACKATHON-2026/team-112

---

# 📸 Hackathon Moments

### 🏅 Prize Ceremony

| Team Award | Group Photo |
|---|---|
| ![](images/award1.jpg) | ![](images/team1.jpg) |

---

### 🚀 Team Moments

| Celebration | Final Ceremony |
|---|---|
| ![](images/team2.jpg) | ![](images/award2.jpg) |

---

### 💻 Building During Hackathon

<p align="center">
  <img src="images/workspace.jpg" width="700"/>
</p>

---

# ❓ Problem Statement

Informal caregivers often experience emotional exhaustion and burnout while caring for loved ones.

Most existing mental health solutions rely heavily on explicit self-reporting, which many caregivers avoid because of:
- stigma,
- emotional fatigue,
- denial,
- or fear of judgment.

The challenge was to build a system that could:
- detect stress passively,
- respect user privacy,
- avoid medicalized interaction,
- and provide gentle support without overwhelming the user.

---

# 💡 Solution

StressCare is an AI-powered caregiver wellness assistant that passively detects stress patterns through natural conversations and voice interactions.

Instead of forcing users to complete mental health questionnaires, the system quietly analyzes behavioral and emotional indicators to provide:

- burnout detection,
- emotional wellness tracking,
- gentle support nudges,
- and localized caregiver resources.

The platform is designed to feel supportive — not clinical.

---

# ✨ Features

### 🧠 Passive Stress Detection
- Sentiment and stress analysis using NLP
- Voice stress detection via waveform analysis
- Invisible behavioral monitoring without explicit disclosure

### 🎙️ Invisible Journaling
- Natural conversations instead of clinical forms
- No mental health labeling
- Silent pattern tracking across sessions

### 💬 Gentle Support Nudges
- Rest reminders
- Delegation suggestions
- Emotional wellness prompts
- Non-alarming, human-centered interactions

### 🌍 Localized Resource Suggestions
- Region-specific caregiver support resources
- Community groups and helplines
- Nearby support assistance recommendations

### 🔒 Privacy First
- PII masking before AI processing
- Ghost Mode for zero data storage
- PIN-protected session history
- Raw voice data never stored

---

# 🏗️ System Architecture

```text
User Input (Voice Log / Text Chat)
         |
         v
  +------------------+
  |   PII Masking    |
  +--------+---------+
           |
           v
  +------------------+
  |  NLP + Audio AI  |
  +--------+---------+
           |
           v
  +------------------+
  |  Stress Scoring  |
  +--------+---------+
           |
           v
  +--------------------------------------+
  |  Support Engine                      |
  |  Gentle Nudges / Resources / Alerts  |
  +--------------------------------------+
