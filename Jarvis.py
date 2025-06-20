import speech_recognition as sr  # For converting speech to text
import pyttsx3  # For text-to-speech conversion (offline)
import pywhatkit  # For playing YouTube videos, sending WhatsApp messages, etc.
import datetime  # To handle date and time
import wikipedia  # To fetch Wikipedia summaries
import psutil  # To get system information like CPU, RAM, battery
import time  # Time-related functions
import datetime as dt  # For scheduling WhatsApp messages (more convenient alias)
import requests  # For HTTP requests (used for News API)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)  # For DialoGPT chatbot model
import torch  # PyTorch framework for model inference
import os  # For running system commands and opening apps
import tkinter as tk  # For GUI components (not used in this snippet but imported)
from tkinter import messagebox  # GUI message boxes (also not used here)
import json  # For handling JSON responses from APIs

# Replace this with your actual News API key to fetch news headlines
NEWS_API_KEY = "YOUR_NEWS_API_KEY"

# Load the DialoGPT tokenizer and model for chat functionality
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
tokenizer.padding_side = "left"  # Set tokenizer to pad sequences on the left
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

# Initialize the speech recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")  # Get available voices
engine.setProperty("voice", voices[1].id)  # Set voice (1 = female voice, usually)


def talk(text):
    """
    Convert given text to speech and speak it out loud.
    """
    engine.say(text)
    engine.runAndWait()


def take_command():
    """
    Listen for a voice command from the user and convert it to text.
    Returns the recognized command as lowercase string or None if not recognized.
    """
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Adapt to surrounding noise
            print("Listening...")
            voice = listener.listen(source)  # Listen for audio input
            command = listener.recognize_google(
                voice
            ).lower()  # Use Google API to recognize speech
            print(f"You said: {command}")
            return command
    except sr.UnknownValueError:
        # Speech was unintelligible
        return None
    except sr.RequestError:
        # API was unreachable or unresponsive
        talk("Sir, I can't connect to the internet right now.")
        return None
    except Exception as e:
        # Catch-all for other errors
        print(f"Error: {e}")
        return None


def open_application(command):
    """
    Opens applications or performs system commands based on the user's command.
    """
    if "chrome" in command:
        talk("Opening Google Chrome")
        # Path to Chrome executable - adjust if different on your machine
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

    elif "downloads" in command:
        talk("Opening Downloads folder")
        # Opens the user's Downloads directory
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        os.startfile(downloads_path)

    elif "vs code" in command or "visual studio code" in command:
        talk("Opening Visual Studio Code")
        # Path to VS Code executable - adjust user folder accordingly
        os.startfile(
            "C:\\Users\\USER\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        )

    elif "shutdown" in command:
        talk("Shutting down the computer")
        os.system("shutdown /s /t 1")  # Windows shutdown command with 1 second delay

    elif "restart" in command:
        talk("Restarting the computer")
        os.system("shutdown /r /t 1")  # Windows restart command with 1 second delay

    else:
        talk("Sorry, I don't recognize that application yet.")


def chat_with_jarvis_local():
    """
    Enables a chat mode with the DialoGPT model.
    The user can talk to Jarvis until they say 'stop chat' or 'exit chat'.
    """
    talk("Jarvis chat mode activated. Say 'stop chat' to exit.")
    chat_history_ids = None  # Initialize chat history

    while True:
        user_input = take_command()
        if user_input is None:
            continue  # If no valid input, keep listening

        # Exit chat mode commands
        if "stop chat" in user_input or "exit chat" in user_input:
            talk("Exiting chat mode, sir.")
            break

        try:
            # Encode user input with EOS token for the model
            new_user_input_ids = tokenizer.encode(
                user_input + tokenizer.eos_token, return_tensors="pt"
            )

            # Append new input to chat history to keep context
            bot_input_ids = (
                torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
                if chat_history_ids is not None
                else new_user_input_ids
            )

            # Generate model response with sampling for diversity
            chat_history_ids = model.generate(
                bot_input_ids,
                max_length=1000,
                pad_token_id=tokenizer.eos_token_id,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.75,
            )

            # Decode the generated response, skipping special tokens
            reply = tokenizer.decode(
                chat_history_ids[:, bot_input_ids.shape[-1] :][0],
                skip_special_tokens=True,
            )
            print(f"Jarvis: {reply}")
            talk(reply)  # Speak out the reply

        except Exception as e:
            print(f"Chat error: {e}")
            talk("Sorry sir, something went wrong in our conversation.")


def get_system_stats(command):
    """
    Retrieves and reports system statistics based on the command.
    Supports CPU, RAM, Battery, and combined statistics.
    """
    if "cpu" in command:
        cpu_percent = psutil.cpu_percent(interval=1)
        talk(f"CPU usage is at {cpu_percent} percent.")
        print(f"CPU: {cpu_percent}%")

    elif "ram" in command or "memory" in command:
        ram = psutil.virtual_memory()
        talk(f"RAM usage is at {ram.percent} percent.")
        print(f"RAM: {ram.percent}%")

    elif "battery" in command:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            talk(f"Battery is at {percent} percent and is currently {plugged}.")
            print(f"Battery: {percent}% ({plugged})")
        else:
            talk("Sorry, I can't access battery data on this system.")

    elif "statistics" in command:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            talk(
                f"CPU usage is at {cpu_percent} percent, RAM usage is at {ram.percent} percent, "
                f"and the battery is at {percent} percent and is currently {plugged}."
            )
            print(
                f"CPU: {cpu_percent}%, RAM: {ram.percent}%, Battery: {percent}% ({plugged})"
            )
        else:
            talk("Sorry, I can't access battery data on this system.")


def get_news():
    """
    Fetches and reads aloud the top 5 news headlines using the News API.
    """
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "ok":
            articles = data["articles"][:5]  # Limit to top 5 headlines
            talk("Here are the top news headlines.")
            for i, article in enumerate(articles, start=1):
                title = article["title"]
                talk(f"Headline {i}: {title}")
                print(f"{i}. {title}")
        else:
            talk("Sorry, I couldn’t fetch the news at the moment.")
    except Exception as e:
        talk("There was an error while getting the news.")
        print(f"News API Error: {e}")


def run_jarvis():
    """
    Main function running the assistant.
    Continuously listens for commands and performs actions accordingly.
    """
    talk("Hello sir. How can I assist you?")

    while True:
        command = take_command()

        if command is None:
            continue  # Ignore unrecognized commands and keep listening

        # Exit commands
        if "stop" in command or "exit" in command or "goodbye" in command:
            talk("Goodbye sir. Have a great day!")
            break

        # Greetings based on time of day
        elif "hi" in command or "hello" in command:
            hour = int(datetime.datetime.now().strftime("%H"))
            if 0 < hour <= 6:
                talk("Good night sir")
            elif 6 < hour <= 12:
                talk("Good morning sir")
            elif 12 < hour <= 18:
                talk("Good day sir")
            elif 18 < hour <= 24:
                talk("Good evening sir")

        # Respond to the assistant's name
        elif command == "jarvis":
            talk("Sir?")

        # Play songs on YouTube
        elif "play" in command:
            talk("Done, sir")
            # Clean the command to extract the song name
            command = (
                command.replace("jarvis", "")
                .replace("service", "")
                .replace("song", "")
                .replace("play", "")
                .strip()
            )
            pywhatkit.playonyt(command)  # Play on YouTube

        # Wake-up phrase
        elif "woke up" in command:
            talk("Oh, sir, I am here!")

        # Tell the current time
        elif "time" in command:
            time_now = datetime.datetime.now().strftime("%H:%M")
            talk("Current time is " + time_now)
            print(time_now)

        # Open apps, shutdown, or restart commands
        elif "open" in command or "shutdown" in command or "restart" in command:
            open_application(command)

        # Search Wikipedia for info
        elif "search for" in command:
            search_item = command.replace("search for", "").strip()
            try:
                info = wikipedia.summary(search_item, sentences=2)
                talk(info)
                print(info)
            except wikipedia.exceptions.DisambiguationError:
                talk(
                    "There are multiple results for this search. Please be more specific."
                )
            except wikipedia.exceptions.PageError:
                talk("No matching results found on Wikipedia.")
            except Exception as e:
                talk("An error occurred while searching.")
                print(f"Wikipedia error: {e}")

        # Introduce Jarvis
        elif "introduce" in command:
            talk(
                "My name is Jarvis. My serial number is BV9W85B6V89, model SN2#9CBQ3BC9QC. "
                "I was created by Nihad Mammadov. "
                "My mission is to make your job easy with the commands you give me."
            )

        # System statistics
        elif (
            "cpu" in command
            or "ram" in command
            or "memory" in command
            or "battery" in command
            or "statistics" in command
        ):
            get_system_stats(command)

        # Send WhatsApp message using pywhatkit
        elif "whatsapp" in command:
            talk("Who should I send it to?")
            person = take_command()

            contacts = {
                "example": "+1234567890",  # Replace with actual contact names and phone numbers
            }

            number = contacts.get(person.lower())
            if not number:
                talk("Sorry, I don't have that contact saved.")
                continue

            talk("What is the message?")
            msg = take_command()

            talk("Sending the message now.")

            # Schedule the message for the next minute
            now = dt.datetime.now()
            hour = now.hour
            minute = now.minute + 1
            if minute >= 60:
                minute -= 60
                hour += 1

            talk(
                f"Message scheduled at {hour}:{minute:02d}. Please do not close your browser."
            )
            # Send WhatsApp message using pywhatkit
            pywhatkit.sendwhatmsg(number, msg, hour, minute, wait_time=10)

        # Read news headlines
        elif "news" in command:
            get_news()

        # Activate chat mode with DialoGPT
        elif "chat with me" in command or "talk to me" in command:
            chat_with_jarvis_local()

        else:
            talk("Sir, I didn’t catch that. Please say it again.")


# Program entry point
if __name__ == "__main__":
    run_jarvis()
