import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk

def create_icon():
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.attributes('-topmost', True)  # Keep on top
    root.geometry("64x64+10+10")  # Set position (adjust if needed)

    # Load Icon Image
    img_path = os.path.join(os.path.dirname(__file__), "icon.png")
    img = Image.open(img_path)
    img = img.resize((64, 64), Image.Resampling.LANCZOS)
    icon = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=icon, bg="black")
    label.pack()

    # Keep reference
    root.icon = icon
    root.mainloop()

# Run icon in a separate thread
import threading
threading.Thread(target=create_icon, daemon=True).start()

#might need change 


# Initialize recognizer & text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Create a Tkinter window for the overlay
root = tk.Tk()
root.overrideredirect(True)  # Remove window borders
root.attributes("-topmost", True)  # Keep always on top
root.geometry("100x100+50+50")  # Set position and size
root.configure(bg="black")  # Background color

# Load the icon (create your own 100x100px PNG)
icon_path = "/home/darknx/vol/icon.png"  # Change path to your actual icon
icon_image = Image.open(icon_path)
icon_image = icon_image.resize((100, 100))
icon_tk = ImageTk.PhotoImage(icon_image)

# Label to show the icon
icon_label = tk.Label(root, image=icon_tk, bg="black")
icon_label.pack()

# Function to move window
def on_drag(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

# Make the icon draggable
icon_label.bind("<B1-Motion>", on_drag)

def speak(text):
    """Converts text to speech and speaks it out loud."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listens for a voice command and returns the recognized text."""
    root.deiconify()  # Show the icon when listening
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            speak("Sorry, I couldn't understand.")
            return None
        except sr.RequestError:
            print("Error connecting to speech service.")
            speak("Error connecting to speech service.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
    root.withdraw()  # Hide the icon when not listening

def process_command(command):
    """Processes the command and executes appropriate actions."""
    if not command:
        return

    response = None

    # Exit Command
    if "exit" in command or "close" in command:
        response = "Goodbye!"
        print("VOL:", response)
        speak(response)
        root.quit()  # Close the overlay
        exit()

    # Time & Date
    elif "time" in command:
        response = "The current time is " + datetime.now().strftime("%H:%M")
    elif "date" in command:
        response = "Today's date is " + datetime.now().strftime("%B %d, %Y")

    # Open Calculator
    elif "open calculator" in command:
        response = "Opening calculator."
        os.system("gnome-calculator")

    # Google Search
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        response = f"Searching Google for {query}."
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # Open Website
    elif "open website" in command:
        def open_website(query):
       	    site = query.lower().replace("open ", "").strip()
    	    if not site.startswith("http"):
               site = "https://" + site
            if "." not in site:  # If no domain extension is provided, assume .com
                site += ".com"
            webbrowser.open(site)

    else:
        response = "I didn't understand, but I'm learning."

    print("VOL:", response)
    speak(response)

# Main loop
def run_vol():
    while True:
        command = listen()
        if command:
            process_command(command)

# Start voice assistant in a separate thread
import threading
vol_thread = threading.Thread(target=run_vol)
vol_thread.start()

# Start Tkinter loop
root.mainloop()
