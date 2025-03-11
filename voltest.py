import speech_recognition as sr
import pyttsx3
import time
import threading
import webbrowser
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Change voice to a smooth female voice
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break  # Use the first female voice found

engine.setProperty('rate', 170)  # Adjust speed for smoothness

def speak(text):
    """Function to make VOL speak smoothly"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to listen for commands"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Error"

def assistant():
    """Main assistant function"""
    global is_awake
    while True:
        command = listen()
        print(f"User said: {command}")

        if "close" in command:
            speak("Going to sleep. Say 'Ok VOL' to wake me up.")
            is_awake = False
            wait_for_wake_word()  # Call wake-up listener

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif "exit" in command:
            speak("Goodbye!")
            exit()

        else:
            speak("I didn't understand that.")

def wait_for_wake_word():
    """Function to wait for 'Ok VOL' before reactivating"""
    global is_awake
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while not is_awake:
            try:
                print("Waiting for 'Ok VOL'...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                wake_word = recognizer.recognize_google(audio).lower()

                if "ok vol" in wake_word:
                    is_awake = True
                    speak("I'm back! What do you need?")
                    assistant()  # Restart assistant

            except sr.UnknownValueError:
                continue  # Keep listening until wake word is detected

# Start Assistant
is_awake = True
assistant()

