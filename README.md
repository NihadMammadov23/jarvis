# Jarvis AI Assistant  
![Jarvis Banner](https://github.com/NihadMammadov23/jarvis/blob/main/jarvis.png)  

---

## Overview

**Jarvis AI Assistant** is a powerful, voice-controlled personal assistant built with Python. It listens to your voice commands, executes tasks like opening applications, telling system stats, fetching news, playing YouTube videos, chatting with you using advanced AI, and much more — all through simple conversational interactions.

Powered by industry-leading libraries like `SpeechRecognition`, `pyttsx3`, and the `DialoGPT` conversational model, Jarvis offers a smooth and engaging user experience that bridges voice commands with intelligent responses.

---

## Features

- 🎤 **Voice Recognition:** Accurately listens and understands your voice commands.  
- 🗣️ **Text-to-Speech:** Converts text responses into natural-sounding speech.  
- 💻 **Application Control:** Open apps like Chrome, VS Code, access folders, shutdown or restart your PC.  
- 🕒 **Time & Greetings:** Provides current time and personalized greetings based on time of day.  
- 🔍 **Wikipedia Search:** Summarizes Wikipedia articles on any topic you ask.  
- 📊 **System Stats:** Reports CPU, RAM, battery status, and overall system statistics.  
- 📰 **News Headlines:** Fetches and reads the top 5 current news headlines.  
- 🎵 **YouTube Playback:** Plays requested songs or videos on YouTube.  
- 💬 **Chat Mode:** Chat with Jarvis powered by Microsoft's DialoGPT conversational AI.  
- 📱 **WhatsApp Messaging:** Sends scheduled WhatsApp messages via voice commands.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/NihadMammadov23/jarvis
cd jarvis
```

2. **Create and activate a virtual environment (optional but recommended)**

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install required packages
   
```bash
pip install -r requirements.txt
```

4. Setup environment
   - Replace YOUR_NEWS_API_KEY in the script with your News API key. Get one for free at NewsAPI.org.
   - Modify application paths in open_application() function according to your system.


Usage:

Run the assistant:

```bash
python jarvis.py
```


Speak commands like:

"Open Chrome"
"What is the CPU usage?"
"Search for Artificial Intelligence on Wikipedia"
"Play Despacito on YouTube"
"Send a WhatsApp message to John"
"Chat with me"
"Tell me the news"
Say "stop" or "goodbye" to exit.



Dependencies:

SpeechRecognition
pyttsx3
pywhatkit
wikipedia
psutil
requests
torch
transformers

All dependencies are listed in requirements.txt.



Contribution!
Contributions are welcome! Feel free to open issues or submit pull requests to improve Jarvis AI Assistant.


License
This project is licensed under the MIT License.

