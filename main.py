import tkinter as tk
import speech_recognition as sr
import datetime
import webbrowser
import asyncio
import edge_tts
import os
import wikipedia

def get_knowledge(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError:
        return "Please be more specific."
    except:
        return "I couldn't find information on that."

import re

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

    # Math
    if any(op in command for op in [
    "plus", "minus", "times", "multiplied", "divided", "+", "-", "*", "/"]):
        result = solve_math(command)
        return result if result else "I couldn't understand the math."

    # Knowledge
    if command.startswith(("who is", "what is", "tell me about", "define")):
        return get_knowledge(command)

    # Fallback
    return "I heard you. More features will be added soon."


# -------------------- TEXT → SPEECH (MP3) --------------------

async def speak_mp3(text):
    tts = edge_tts.Communicate(
        text=text,
        voice="en-IN-NeerjaNeural"
    )
    await tts.save("response.mp3")

    # Play MP3 ONLY after mic is OFF
    os.system("start response.mp3")

# -------------------- BUTTON HANDLER --------------------

def on_speak():
    status_label.config(text="Status: Listening...")
    window.update()

    user_text = listen_once()
    user_label.config(text=f"You: {user_text if user_text else '—'}")

    status_label.config(text="Status: Processing...")
    window.update()

    response = process_command(user_text)
    assistant_label.config(text=f"Assistant: {response}")

    status_label.config(text="Status: Speaking...")
    window.update()

    asyncio.run(speak_mp3(response))

    status_label.config(text="Status: Ready")

# -------------------- GUI --------------------

window = tk.Tk()
window.title("AI Voice Assistant")
window.geometry("450x320")

tk.Label(window, text="AI Voice Assistant", font=("Arial", 16, "bold")).pack(pady=10)

status_label = tk.Label(window, text="Status: Ready")
status_label.pack()

user_label = tk.Label(window, text="You:", wraplength=400, justify="left")
user_label.pack(pady=10)

assistant_label = tk.Label(window, text="Assistant:", wraplength=400, justify="left")
assistant_label.pack(pady=10)

tk.Button(
    window,
    text="🎤 Speak",
    font=("Arial", 12),
    command=on_speak
).pack(pady=15)

window.mainloop()


