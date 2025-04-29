import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import requests
import random
import json
import re
from urllib.request import urlopen

class Jarvis:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Default voice
        self.engine.setProperty('rate', 190)  # Speed of speech
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate the recognizer for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        self.user_name = "Sir"  # Default name
        self.wake_word = "jarvis"
        self.reminders = []
        
        # Initialize
        self.speak("Initializing JARVIS")
        self.speak(f"Hello {self.user_name}, how can I assist you today?")

    def speak(self, text):
        """Convert text to speech"""
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen to user's voice input and convert to text"""
        text = ""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing...")
                
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError:
            self.speak("Sorry, my speech service is down.")
        except Exception as e:
            print(f"Error: {e}")
            
        return text.lower()

    def process_command(self, command):
        """Process the user's command"""
        if not command:
            return
            
        # Check for wake word
        if self.wake_word not in command:
            return
            
        # Remove wake word from command
        command = command.replace(self.wake_word, "").strip()
        
        # Greeting
        if any(word in command for word in ["hello", "hi", "hey"]):
            self.greet()
            
        # Time
        elif "time" in command:
            self.tell_time()
            
        # Date
        elif "date" in command:
            self.tell_date()
            
        # Open application
        elif "open" in command:
            app = command.replace("open", "").strip()
            self.open_application(app)
            
        # Weather
        elif "weather" in command:
            self.get_weather()
            
        # News
        elif "news" in command:
            self.get_news()
            
        # Wikipedia
        elif "wikipedia" in command or "who is" in command:
            query = command.replace("wikipedia", "").replace("who is", "").strip()
            self.search_wikipedia(query)
            
        # Google search
        elif "search" in command or "google" in command:
            query = command.replace("search", "").replace("google", "").strip()
            self.search_google(query)
            
        # Tell a joke
        elif "joke" in command:
            self.tell_joke()
            
        # Tell a quote
        elif "quote" in command:
            self.tell_quote()
            
        # Set a reminder
        elif "remind" in command or "reminder" in command:
            self.set_reminder(command)
            
        # Check reminders
        elif "reminders" in command:
            self.check_reminders()
            
        # Set an alarm
        elif "alarm" in command:
            self.set_alarm(command)
            
        # Set a timer
        elif "timer" in command:
            self.set_timer(command)
            
        # System controls
        elif "volume" in command:
            self.control_volume(command)
            
        # Shutdown computer
        elif "shutdown" in command or "turn off computer" in command:
            self.shutdown_computer()
            
        # Exit Jarvis
        elif any(word in command for word in ["exit", "quit", "goodbye", "bye"]):
            self.exit_jarvis()
            
        # If command not recognized
        else:
            self.speak("I'm not sure how to help with that yet.")

    def greet(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        
        if 0 <= hour < 12:
            self.speak(f"Good morning {self.user_name}")
        elif 12 <= hour < 18:
            self.speak(f"Good afternoon {self.user_name}")
        else:
            self.speak(f"Good evening {self.user_name}")

    def tell_time(self):
        """Tell the current time"""
        time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {time}")

    def tell_date(self):
        """Tell the current date"""
        date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {date}")

    def open_application(self, app):
        """Open specified application"""
        app = app.lower()
        
        # Dictionary of common applications and their paths
        # You may need to adjust these paths for your system
        apps = {
            "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "spotify": "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe",
            "vscode": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
            "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
            "notepad": "notepad.exe",
            "calculator": "calc.exe"
        }
        
        # Handle websites
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "github": "https://github.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://www.linkedin.com",
            "amazon": "https://www.amazon.com",
            "netflix": "https://www.netflix.com"
        }
        
        try:
            # Check if it's a website
            if app in websites:
                self.speak(f"Opening {app}")
                webbrowser.open(websites[app])
                return
                
            # Check if it's a known application
            if app in apps:
                self.speak(f"Opening {app}")
                os.startfile(os.path.expandvars(apps[app]))
                return
                
            # Try to open as a generic application
            self.speak(f"Attempting to open {app}")
            os.system(f"start {app}")
            
        except Exception as e:
            self.speak(f"Sorry, I couldn't open {app}")
            print(f"Error: {e}")

    def get_weather(self):
        """Get current weather information"""
        # You would need to sign up for a free API key from OpenWeatherMap
        # Replace YOUR_API_KEY with your actual API key
        try:
            self.speak("For which city would you like the weather?")
            city = self.listen()
            
            if not city:
                self.speak("I couldn't understand the city name.")
                return
                
            # Using a free weather API
            api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
            base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            # For demo purposes, let's simulate a response
            # In a real implementation, you would use:
            # response = requests.get(base_url).json()
            
            # Simulated response
            self.speak(f"The current temperature in {city} is 22 degrees Celsius with partly cloudy skies.")
            
        except Exception as e:
            self.speak("Sorry, I couldn't fetch the weather information.")
            print(f"Error: {e}")

    def get_news(self):
        """Get latest news headlines"""
        # You would need to sign up for a free API key from NewsAPI
        # Replace YOUR_API_KEY with your actual API key
        try:
            # Using a free news API
            api_key = "YOUR_API_KEY"  # Replace with your NewsAPI key
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            
            # For demo purposes, let's simulate a response
            # In a real implementation, you would use:
            # response = requests.get(url).json()
            
            # Simulated response
            self.speak("Here are today's top headlines:")
            self.speak("Scientists discover new renewable energy source that could revolutionize power generation.")
            self.speak("Tech company announces breakthrough in artificial intelligence development.")
            self.speak("International space mission successfully lands on Mars.")
            
        except Exception as e:
            self.speak("Sorry, I couldn't fetch the latest news.")
            print(f"Error: {e}")

    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        if not query:
            self.speak("What would you like to search for?")
            query = self.listen()
            
        if not query:
            return
            
        try:
            self.speak(f"Searching Wikipedia for {query}")
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            self.speak(results)
        except Exception as e:
            self.speak(f"Sorry, I couldn't find information about {query} on Wikipedia.")
            print(f"Error: {e}")

    def search_google(self, query):
        """Search Google"""
        if not query:
            self.speak("What would you like to search for?")
            query = self.listen()
            
        if not query:
            return
            
        self.speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "Why was the computer cold? It left its Windows open!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "How do you organize a space party? You planet!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "I'm reading a book on anti-gravity. It's impossible to put down!"
        ]
        
        joke = random.choice(jokes)
        self.speak(joke)

    def tell_quote(self):
        """Tell a random inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The best way to predict the future is to create it. - Peter Drucker",
            "It does not matter how slowly you go as long as you do not stop. - Confucius",
            "Everything you've ever wanted is on the other side of fear. - George Addair"
        ]
        
        quote = random.choice(quotes)
        self.speak(quote)

    def set_reminder(self, command):
        """Set a reminder"""
        # Extract time and message from command
        # This is a simple implementation - a more robust solution would use NLP
        try:
            # Example command: "remind me to call mom at 5 pm"
            parts = command.split("remind me to")
            if len(parts) < 2:
                self.speak("Please specify what you'd like me to remind you about.")
                return
                
            message_parts = parts[1].split("at")
            
            if len(message_parts) < 2:
                self.speak("Please specify a time for the reminder.")
                return
                
            message = message_parts[0].strip()
            time_str = message_parts[1].strip()
            
            # Add to reminders list
            self.reminders.append({"message": message, "time": time_str})
            
            self.speak(f"I'll remind you to {message} at {time_str}")
            
        except Exception as e:
            self.speak("I couldn't set that reminder. Please try again.")
            print(f"Error: {e}")

    def check_reminders(self):
        """Check and read out current reminders"""
        if not self.reminders:
            self.speak("You don't have any reminders set.")
            return
            
        self.speak("Here are your current reminders:")
        for i, reminder in enumerate(self.reminders, 1):
            self.speak(f"{i}. {reminder['message']} at {reminder['time']}")

    def set_alarm(self, command):
        """Set an alarm"""
        # This is a simplified implementation
        try:
            # Example command: "set alarm for 7 am"
            time_str = command.split("for")[-1].strip()
            
            self.speak(f"Alarm set for {time_str}")
            
            # In a real implementation, you would:
            # 1. Parse the time string to a datetime object
            # 2. Calculate the time difference
            # 3. Set a timer to trigger the alarm
            # 4. Play a sound when the alarm triggers
            
        except Exception as e:
            self.speak("I couldn't set that alarm. Please try again.")
            print(f"Error: {e}")

    def set_timer(self, command):
        """Set a timer"""
        try:
            # Example command: "set timer for 5 minutes"
            duration_str = command.split("for")[-1].strip()
            
            # Extract number and unit
            match = re.search(r"(\d+)\s*(second|minute|hour|day)s?", duration_str)
            
            if not match:
                self.speak("I couldn't understand the timer duration.")
                return
                
            amount = int(match.group(1))
            unit = match.group(2)
            
            # Convert to seconds
            seconds = 0
            if unit == "second":
                seconds = amount
            elif unit == "minute":
                seconds = amount * 60
            elif unit == "hour":
                seconds = amount * 3600
            elif unit == "day":
                seconds = amount * 86400
                
            self.speak(f"Timer set for {amount} {unit}{'s' if amount > 1 else ''}")
            
            # In a real implementation, you would:
            # 1. Start a background timer
            # 2. Play a sound when the timer expires
            
            # For demo purposes, we'll just wait and then speak
            # Note: This will block the program - in a real implementation,
            # you would use threading or asyncio
            time.sleep(5)  # Simulating a short wait instead of the full duration
            self.speak(f"Your {amount} {unit}{'s' if amount > 1 else ''} timer has expired.")
            
        except Exception as e:
            self.speak("I couldn't set that timer. Please try again.")
            print(f"Error: {e}")

    def control_volume(self, command):
        """Control system volume"""
        try:
            if "up" in command or "increase" in command:
                self.speak("Increasing volume")
                # In a real implementation, you would use a library like pycaw
                # to control the system volume
            elif "down" in command or "decrease" in command:
                self.speak("Decreasing volume")
            elif "mute" in command:
                self.speak("Muting volume")
            else:
                self.speak("I'm not sure what you want me to do with the volume.")
                
        except Exception as e:
            self.speak("I couldn't control the volume.")
            print(f"Error: {e}")

    def shutdown_computer(self):
        """Shutdown the computer"""
        self.speak("Are you sure you want to shutdown the computer?")
        confirmation = self.listen()
        
        if "yes" in confirmation:
            self.speak("Shutting down the computer")
            # In a real implementation, you would use:
            # os.system("shutdown /s /t 1")
            self.speak("This is a simulation. In a real implementation, the computer would shut down now.")
        else:
            self.speak("Shutdown cancelled")

    def exit_jarvis(self):
        """Exit the JARVIS program"""
        self.speak(f"Goodbye {self.user_name}. Have a great day!")
        exit()

    def run(self):
        """Main loop to run JARVIS"""
        while True:
            command = self.listen()
            self.process_command(command)


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()