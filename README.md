# 🧠 SmartGov Bot - HackForNepal 2025 🇳🇵

**Category:** E-Governance  
**Team Name:** Me and the boys  
**Team Members:**  
- Ashish Limbu  
- Bidur Siwakoti  
- Christopher Pokhreal  
- Umar Abudalla Ansari  

---

## 📌 Overview

SmartGov Bot is an intelligent chatbot system designed to simplify access to Nepali government services through natural, conversational interfaces. It helps citizens navigate complex procedures like:

- Citizenship Application  
- PAN Registration  
- Passport Application  
- Voter ID Guidance  
- Social Security Allowances  
- Public Service Exams (e.g., Loksewa)

---

## 🎯 Key Features

- 💬 **Conversational Guidance**: Step-by-step walkthroughs for bureaucratic procedures  
- 📝 **Interactive Form Filling**: Users provide personal details through a guided chat  
- 🧠 **Context-Aware Conversations**: Handles follow-ups, clarifications, and incomplete input  
- 🗣️ **Voice Support**: Uses browser-native TTS/STT for accessibility  
- 🌐 **Multilingual Ready**: Easily extendable for Nepali and English  
- 🗂️ **Custom API Integration**: Simulates real-world form submissions to government-like endpoints

---

## 🛠 Tech Stack

| Layer         | Tech Used                          |
|---------------|------------------------------------|
| **Backend**   | Rasa (Python), Custom Actions      |
| **Frontend**  | HTML, CSS, JavaScript (Vanilla/React) |
| **Voice I/O** | Web Speech API (Text-to-Speech, Speech-to-Text) |
| **Optional**  | Node.js (API bridge), MongoDB (data storage) |

---

## 🚀 How It Works

1. The user starts a conversation via chat or voice
2. The bot guides them step-by-step using forms (e.g., driving license application)
3. Each required slot is filled interactively (e.g., name, DOB, address)
4. Once complete, the bot simulates a form submission via an API
5. Users receive confirmation or next-step instructions

---



 **Clone this repo**  
   `git clone https://github.com/yourusername/smartgov-bot.git`

2. **Install Rasa**  
   `pip install rasa`

3. **Train the model**  
   `rasa train`

4. **Run the bot**  
   ` rasa run --enable-api --cors "*" --debug`
   
   `rasa run actions` (in another terminal)
   
   `python api_server.py`

6. **Test in UI**  
   Open `index.html` in your browser or run frontend via `npm start` (React)

---

##  Contact Us

If you'd like to support, collaborate, or deploy this bot for your municipality:

📧 Email: [siwakoti.bidur7745@email.com]  


