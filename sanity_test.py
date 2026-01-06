import speech_recognition as sr
import pyttsx3

# --- TTS TEST ---
engine = pyttsx3.init()
engine.say("Text to speech is working")
engine.runAndWait()

# --- MIC TEST ---
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)

    engine.say(f"You said {text}")
    engine.runAndWait()
except Exception as e:
    print("Error:", e)
