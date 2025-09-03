import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Optional: reduce noise
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"User  said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return ""

def respond(command):
    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            speak(f"Here are the search results for {query}")
        else:
            speak("Please say what you want me to search for.")
    else:
        speak("Sorry, I can't do that yet.")

if __name__ == "__main__":
    speak("Hi, I am your assistant. How can I help you?")
    while True:
        user_command = listen()
        if user_command:
            if "exit" in user_command or "stop" in user_command:
                speak("Goodbye!")
                break
            respond(user_command)
