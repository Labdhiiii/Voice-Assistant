import tkinter as tk
from tkinter import scrolledtext
import tkinter as tk
import speech_recognition as sr
import datetime
import webbrowser
import asyncio
import edge_tts
import os
import wikipedia
import webbrowser
import urllib.parse
import random
import pygame
import threading
import asyncio
import uuid

pygame.mixer.init()

def speak(text):
    threading.Thread(
        target=lambda: asyncio.run(_speak_async(text)),
        daemon=True
    ).start()


POLITE_RESPONSES = {
    "thanks": [
        "You're welcome 😊",
        "Glad I could help!",
        "Anytime 🌸"
    ],
    "ok": [
        "Alright!",
        "Okay 😊",
        "Sure!"
    ],
    "praise": [
        "Thank you! 🌸",
        "That means a lot!",
        "Happy to help 😄"
    ]
}


def play_music(command):
    # Remove trigger words
    query = command.replace("play", "").replace("music", "").strip()

    if not query:
        query = "popular songs"

    search_query = urllib.parse.quote(query)
    url = f"https://music.youtube.com/search?q={search_query}"

    webbrowser.open(url)
    return f"Playing {query} on YouTube Music."
import wikipedia

wikipedia.set_lang("en")

def extract_entity(command):
    command = command.lower()
    for phrase in ["tell me about", "what is", "who is", "define"]:
        command = command.replace(phrase, "")
    return command.strip()


def get_knowledge(command):
    try:
        entity = extract_entity(command)

        if not entity or len(entity) < 2:
            return "Please tell me what you want to know."

        # Step 1: Search Wikipedia
        search_results = wikipedia.search(entity, results=5)

        if not search_results:
            return "I couldn't find information on that."

        # Step 2: Pick best match (first result is usually best)
        best_match = search_results[0]

        # Step 3: Get summary of resolved entity
        summary = wikipedia.summary(
            best_match,
            sentences=2,
            auto_suggest=False,
            redirect=True
        )

        return summary

    except wikipedia.exceptions.DisambiguationError as e:
        return f"This topic has multiple meanings. Try something more specific."

    except wikipedia.exceptions.PageError:
        return "I couldn't find information on that."

    except Exception:
        return "Something went wrong while searching."

# def get_knowledge(command):
#     try:
#         # Remove trigger phrases
#         query = command.lower()
#         query = query.replace("tell me about", "")
#         query = query.replace("what is", "")
#         query = query.replace("who is", "")
#         query = query.replace("define", "")
#         query = query.strip()

#         if not query:
#             return "Please tell me what you want to know."

#         summary = wikipedia.summary(query, sentences=2)
#         return summary

#     except wikipedia.exceptions.DisambiguationError as e:
#         return f"That topic has multiple meanings. Try being more specific."

#     except wikipedia.exceptions.PageError:
#         return "I couldn't find information on that."

#     except Exception:
#         return "Something went wrong while searching."

# def get_knowledge(query):
#     try:
#         summary = wikipedia.summary(query, sentences=2)
#         return summary
#     except wikipedia.exceptions.DisambiguationError:
#         return "Please be more specific."
#     except:
#         return "I couldn't find information on that."


import re

def solve_math(text):
    text = text.lower()

    # Remove trigger words
    text = re.sub(r"(solve|calculate|what is|equals|equal to)", "", text)

    # Replace spoken operators
    replacements = {
        "plus": "+",
        "minus": "-",
        "multiplied by": "*",
        "multiply by": "*",
        "times": "*",
        "divided by": "/",
        "divide by": "/"
    }

    for word, symbol in replacements.items():
        text = text.replace(word, symbol)

    # Extract only valid math characters
    expression = re.findall(r"[0-9+\-*/(). ]+", text)

    if not expression:
        return None

    try:
        result = eval(expression[0])
        return f"The result is {result}"
    except:
        return "I couldn't solve that math problem."



# -------------------- SPEECH → TEXT --------------------

def listen_once():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Status: Listening...")
        window.update()
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text.lower()
    except:
        return None

# -------------------- INTENT LOGIC --------------------

def process_command(command):
    if not command:
        return "Sorry, I did not understand."

    # Greetings
    if any(word in command for word in ["hello", "hi", "hey"]):
        return "Hello. I am ready."

    # Exit
    if any(word in command for word in ["bye", "exit", "quit"]):
        return "Goodbye. Have a nice day."

    # Time / Date
    if "time" in command:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"

    if "date" in command:
        return f"Today's date is {datetime.datetime.now().strftime('%d %B %Y')}"

    # System commands
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    
    if "play" in command or "music" in command:
        return play_music(command)

    # Math
    if any(op in command for op in [
    "plus", "minus", "times", "multiplied", "divided", "+", "-", "*", "/"]):
        result = solve_math(command)
        return result if result else "I couldn't understand the math."

    # Knowledge
    if command.startswith(("who is", "what is", "tell me about", "define")):
        return get_knowledge(command)
    
    # Polite conversation
    if any(word in command for word in ["thank you", "thanks", "thx"]):
        return random.choice(POLITE_RESPONSES["thanks"])

    if any(word in command for word in ["ok", "okay", "alright"]):
        return random.choice(POLITE_RESPONSES["ok"])

    if any(word in command for word in ["nice", "cool", "great", "good job", "well done","amazing","loved it"]):
        return random.choice(POLITE_RESPONSES["praise"])

    # Fallback
    return "I heard you. More features will be added soon."


# -------------------- TEXT → SPEECH (MP3) --------------------
async def _speak_async(text):
    try:
        filename = f"tts_{uuid.uuid4().hex}.mp3"

        tts = edge_tts.Communicate(text, voice="en-IN-NeerjaNeural")
        await tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(filename)

    except Exception as e:
        print("TTS Error:", e)

# async def speak_mp3(text):
#     tts = edge_tts.Communicate(
#         text=text,
#         voice="en-IN-NeerjaNeural"
#     )
#     await tts.save("response.mp3")

#     pygame.mixer.music.load("response.mp3")
#     pygame.mixer.music.play()

#     # Wait until audio finishes
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

# async def speak_mp3(text):
#     tts = edge_tts.Communicate(
#         text=text,
#         voice="en-IN-NeerjaNeural"
#     )
#     await tts.save("response.mp3")

#     # Play MP3 ONLY after mic is OFF
#     os.system("start response.mp3")

# -------------------- BUTTON HANDLER --------------------
def on_speak():
    user_text = listen_once()

    response = process_command(user_text)

    add_message("You", user_text if user_text else "—")
    add_message("Sakhi", response)

    say_and_update(response)

# def on_speak():
#     status_label.config(text="Status: Listening...")
#     window.update()

#     user_text = listen_once()

#     add_message("You", user_text if user_text else "—")

#     status_label.config(text="Status: Processing...")
#     window.update()

#     response = process_command(user_text)

#     add_message("Sakhi", response)

#     status_label.config(text="Status: Speaking...")
#     window.update()

#     asyncio.run(speak_mp3(response))

#     status_label.config(text="Status: Ready")

# def on_speak():
#     status_label.config(text="Status: Listening...")
#     window.update()

#     user_text = listen_once()
#     user_label.config(text=f"You: {user_text if user_text else '—'}")

#     status_label.config(text="Status: Processing...")
#     window.update()

#     response = process_command(user_text)
#     assistant_label.config(text=f"Assistant: {response}")

#     status_label.config(text="Status: Speaking...")
#     window.update()

#     asyncio.run(speak_mp3(response))

#     status_label.config(text="Status: Ready")

# -------------------- GUI --------------------

window = tk.Tk()
window.title("AI Voice Assistant")
window.geometry("520x420")
window.configure(bg="#f4f6f8")

title = tk.Label(
    window,
    text="SAKHI",
    font=("Segoe UI", 18, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50"
)
title.pack(pady=5)

subtitle = tk.Label(
    window,
    text="Your AI Voice Assistant",
    font=("Segoe UI", 10),
    bg="#f4f6f8",
    fg="#555"
)
subtitle.pack()

status_label = tk.Label(
    window,
    text="Status: Ready",
    bg="#f4f6f8",
    fg="green"
)
status_label.pack(pady=5)

def say_and_update(text):
    status_label.config(text="Status: Speaking...", fg="green")
    speak(text)
    window.after(3000, lambda: status_label.config(text="Status: Idle", fg="gray"))

chat_box = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    width=60,
    height=15,
    font=("Segoe UI", 10)
)
chat_box.pack(padx=10, pady=10)
chat_box.config(state=tk.DISABLED)

def add_message(sender, message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"{sender}: {message}\n\n")
    chat_box.yview(tk.END)
    chat_box.config(state=tk.DISABLED)

speak_button = tk.Button(
    window,
    text="🎤 Speak",
    font=("Segoe UI", 12),
    width=15,
    bg="#3498db",
    fg="white",
    command=on_speak
)
speak_button.pack(pady=10)

window.mainloop()
