import sys
import threading
import time
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

# Window size for PC testing (Looks like a mobile screen)
Window.size = (400, 700)

class JarvisEngine:
    def __init__(self, ui_callback):
        self.ui_callback = ui_callback
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id) # 0 for Male, 1 for Female
        self.engine.setProperty('rate', 170)
        self.is_running = True

    def speak(self, text):
        self.ui_callback(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_background(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                query = r.recognize_google(audio, language='en-in')
                return query.lower()
            except Exception:
                return ""

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.ui_callback("[Listening...]")
            r.pause_threshold = 0.8
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                self.ui_callback("[Recognizing...]")
                query = r.recognize_google(audio, language='en-in')
                self.ui_callback(f"You: {query}")
                return query.lower()
            except Exception:
                return "none"

    def execute_loop(self):
        self.speak("Android system framework online. Awaiting activation, Sir.")
        while self.is_running:
            wake_word = self.listen_background()
            
            if "hey jarvis" in wake_word or "jarvis" in wake_word:
                self.speak("Yes Sir, system is fully responsive.")
                
                while self.is_running:
                    query = self.takeCommand()
                    if query == "none":
                        continue

                    # --- ANDROID & PC COMPATIBLE COMMANDS ---
                    if 'open whatsapp' in query or 'whatsapp' in query:
                        self.speak("Opening WhatsApp, Sir.")
                        webbrowser.open("https://whatsapp.com") 
                        break

                    elif 'open instagram' in query or 'instagram' in query:
                        self.speak("Opening Instagram.")
                        webbrowser.open("https://instagram.com")
                        break

                    elif 'the time' in query:
                        strTime = datetime.datetime.now().strftime("%H:%M")
                        self.speak(f"Sir, the current time is {strTime}")

                    elif 'sleep' in query or 'go to sleep' in query:
                        self.speak("Going into background standby mode. Say Hey Jarvis to wake me up.")
                        break

                    elif 'shutdown' in query or 'exit' in query:
                        self.speak("Terminating core protocols. Goodbye Sir.")
                        self.is_running = False
                        App.get_running_app().stop()
                        sys.exit()
            time.sleep(0.1)

# --- KIVY GRAPHICAL USER INTERFACE ---
class JarvisUI(BoxLayout):
    def __init__(self, **kwargs):
        super(JarvisUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        # Title/Status Text
        self.status_label = Label(
            text="JARVIS AI\n[ Standby Mode ]", 
            font_size='24sp',
            halign='center',
            markup=True,
            size_hint=(1, 0.6)
        )
        self.add_widget(self.status_label)

        # Sci-Fi Glowing Center Button
        self.mic_button = Button(
            text="JARVIS CORE",
            font_size='20sp',
            size_hint=(1, 0.4),
            background_color=(0, 0.7, 1, 1) # Neon Blue Color
        )
        self.add_widget(self.mic_button)

        # Start Jarvis Engine in a background thread so UI doesn't freeze
        self.jarvis = JarvisEngine(self.update_status)
        threading.Thread(target=self.jarvis.execute_loop, daemon=True).start()

    def update_status(self, text):
        # Update the UI text safely from background thread
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', text))

class JarvisApp(App):
    def build(self):
        self.title = "Jarvis Mobile Controller"
        return JarvisUI()

if __name__ == "__main__":
    JarvisApp().run()
