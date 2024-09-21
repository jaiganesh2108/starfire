import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from random import choice
from utils import opening_text
from pprint import pprint
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import time
import os
import openai
import pyautogui
import threading
import random


USERNAME = config('USERNAME')
BOTNAME = config('BOTNAME')
openai.api_key="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"


engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        if "starfire" in query.lower():
            return True
    except sr.UnknownValueError:
        pass
    return False

# Function to take a screenshot
def take_screenshot():
    """Takes a screenshot and saves it to the 'screenshots' folder with a timestamp"""
    # Define the folder where screenshots will be saved
    folder_path = r'C:\Users\jaig7\OneDrive\Desktop\starfire\screenshot'
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Create a timestamp for the screenshot file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"screenshot_{timestamp}.png"
    
    # Define the full path to save the screenshot
    screenshot_path = os.path.join(folder_path, file_name)
    
    # Capture the screenshot
    screenshot = pyautogui.screenshot()
    
    # Save the screenshot to the defined path
    screenshot.save(screenshot_path)
    return screenshot_path

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-4" if you have access to GPT-4
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error in ChatGPT request: {e}")
        return "Sorry, there was an error connecting to ChatGPT."

def play_random_music(folder_path):
    try:
        songs = [song for song in os.listdir(folder_path) if song.endswith(('.mp3', '.wav'))]
        if songs:
            song_to_play = random.choice(songs)
            os.startfile(os.path.join(folder_path, song_to_play))
        else:
            speak("No songs found in the folder.")
    except Exception as e:
        speak("There was an error playing the music.")
        print(f"Error: {str(e)}")

def open_edge():
    os.startfile("msedge.exe")  # Windows command to open Microsoft Edge

# Function to open Microsoft Paint
def open_paint():
    os.startfile("mspaint.exe")  # Windows command to open Microsoft Paint

# Function to open File Explorer
def open_file_explorer():
    os.startfile(r'C:\\Users\\jaig7\\OneDrive\\Desktop')  

def shutdown_system():
    os.system("shutdown /s /t 1")

def restart_system():
    os.system("shutdown /r /t 1")

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def set_reminder(reminder_message, delay_in_seconds):
    def reminder_task():
        time.sleep(delay_in_seconds)
        speak(reminder_message)
    threading.Thread(target=reminder_task).start()

def lock_system():
    os.system("rundll32.exe user32.dll, LockWorkStation")



# Greet the user
def greet_user():
    """Greets the user according to the time"""
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"Introducing myself, I am {BOTNAME}")
    speak(f"I can help with your daily routine and in your business")
    speak(f"please tell the access code!") 

def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module, and converts it into text"""
    r = sr.Recognizer()

    # Adjust the energy threshold to account for background noise
    r.energy_threshold = 300 # Adjust based on your environment

    with sr.Microphone() as source:
        print('Listening...')
        r.adjust_for_ambient_noise(source, duration=1)  # Adjusts for ambient noise
        audio = r.listen(source, timeout=None)  # Set only timeout, no phrase_time_limit

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        return query.lower()
    except sr.WaitTimeoutError:
        print("Listening timed out. Please try again.")
        return "None"
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please repeat.")
        return "None"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "None"


def activate_bot():
    """Listen for the bot's name to activate the main function"""
    print(f"Waiting for the wake word '{BOTNAME}'...")
    while True:
        query = take_user_input()
        if BOTNAME.lower() in query:
            return True
        time.sleep(1)


if __name__ == '__main__':
    greet_user()

    while True:
        if activate_bot():
            speak("Access Granted!")
            speak(f"welcome back {USERNAME}, how can I assist you?")
            while True:
                query = take_user_input().lower()

                if query == 'None':
                    continue

                if 'exit' in query or 'eject' in query:
                    speak("Have a goodday sir!")
                    break

                if listen_for_wake_word():
                    activate_bot()

                if 'open notepad' in query:
                    open_notepad()

                elif 'open discord' in query:
                    open_discord()

                elif 'open command prompt' in query or 'open cmd' in query:
                    open_cmd()

                elif 'open camera' in query:
                    open_camera()

                elif 'open calculator' in query:
                    open_calculator()

                elif 'ip address' in query:
                    ip_address = find_my_ip()
                    speak(f'Your IP Address is {ip_address}')
                    print(f'Your IP Address is {ip_address}')

                elif 'wikipedia' in query:
                    speak('What do you want to search on Wikipedia, sir?')
                    search_query = take_user_input().lower()
                    results = search_on_wikipedia(search_query)
                    speak(f"According to Wikipedia, {results}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(results)

                elif 'youtube' in query:
                    speak('What do you want to play on Youtube, sir?')
                    video = take_user_input().lower()
                    play_on_youtube(video)

                elif 'search on google' in query:
                    speak('What do you want to search on Google, sir?')
                    query = take_user_input().lower()
                    search_on_google(query)

                elif 'send whatsapp' in query:
                    speak('On what number should I send the message sir? Please enter in the console: ')
                    number = input("Enter the number: ")
                    speak("What is the message sir?")
                    message = take_user_input().lower()
                    send_whatsapp_message(number, message)
                    speak("I've sent the message sir.")

                elif "send email" in query:
                    speak("On what email address do I send sir? Please enter in the console: ")
                    receiver_address = input("Enter email address: ")
                    speak("What should be the subject sir?")
                    subject = take_user_input().capitalize()
                    speak("What is the message sir?")
                    message = take_user_input().capitalize()
                    if send_email(receiver_address, subject, message):
                        speak("I've sent the email sir.")
                    else:
                        speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

                elif 'joke' in query:
                    speak(f"Hope you like this one sir")
                    joke = get_random_joke()
                    speak(joke)
                    speak("For your convenience, I am printing it on the screen sir.")
                    pprint(joke)

                elif "advice" in query:
                    speak(f"Here's an advice for you, sir")
                    advice = get_random_advice()
                    speak(advice)
                    speak("For your convenience, I am printing it on the screen sir.")
                    pprint(advice)

                elif "trending movies" in query:
                    speak(f"Some of the trending movies are: {get_trending_movies()}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(*get_trending_movies(), sep='\n')

                elif 'news' in query:
                    speak(f"I'm reading out the latest news headlines, sir")
                    speak(get_latest_news())
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(*get_latest_news(), sep='\n')

                elif 'weather' in query:
                    ip_address = find_my_ip()
                    city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                    speak(f"Getting weather report for your city {city}")
                    weather, temperature, feels_like = get_weather_report(city)
                    speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
                    speak(f"Also, the weather report talks about {weather}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
                
                elif 'screenshot' in query: 
                    speak("Taking a screenshot, sir.")
                    screenshot_path = take_screenshot()  
                    print(f"Screenshot saved as {screenshot_path}")

                elif 'super search' in query:
                    speak('What would you like to ask ChatGPT?')
                    prompt = take_user_input()
                    chatgpt_response = chat_with_gpt(prompt)
                    
                    if chatgpt_response:
                        speak(f"ChatGPT says: {chatgpt_response}")
                        print(f"ChatGPT says: {chatgpt_response}")
                    else:
                        speak("There was an issue communicating with ChatGPT.")
                        print("Error: Failed to get a response from ChatGPT")

                elif 'set a reminder' in query:
                    speak("What reminder would you like to set?")
                    reminder_message = take_user_input()
                    speak("In how many seconds should I remind you?")
                    delay_in_seconds = int(take_user_input())
                    set_reminder(reminder_message, delay_in_seconds)
                    speak(f"Reminder set for {delay_in_seconds} seconds.")

                elif 'play music' in query:
                    music_folder = r'C:\Users\YourUsername\Music'
                    play_random_music(music_folder)
                    speak("Playing random music.")
                
                elif 'what time is it' in query:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    speak(f"The time is {current_time}")

                elif 'what is the date' in query:
                    current_date = datetime.now().strftime("%B %d, %Y")
                    speak(f"Today's date is {current_date}")

                elif "how are you" in query:
                    speak("i'm good sir!")

                elif "hey starfire" in query:
                    speak("hi sir!")

                elif "my number" in query:
                    speak("your phone number: ")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print("YOUR NUMBER: ")

                elif 'open edge' in query:
                    open_edge()

                elif 'open paint' in query:
                    open_paint()

                elif 'open file explorer' in query:
                    open_file_explorer()

                elif 'delete file' in query:
                    speak('Which file would you like to delete? Please enter the file path.')
                    file_path = input('Enter file path: ')
                    if delete_file(file_path):
                        speak(f"File {file_path} deleted successfully.")
                    else:
                        speak(f"Could not delete {file_path}. Please check the file path and try again.")

                elif 'solve math' in query:
                    speak('What math problem would you like me to solve?')
                    math_problem = take_user_input().lower()
                    gpt_response = chat_with_gpt(f"Please solve this math problem: {math_problem}")
                    speak(f"The solution is: {gpt_response}")
                    print(f"Solution: {gpt_response}")
                    
                elif 'lock system' in query:
                    speak("Locking the system, sir.")
                    lock_system()

                elif 'shut down the system' in query:
                    speak('Shutting down the system, sir.')
                    shutdown_system()

                elif 'restart the system' in query:
                    speak('Restarting the system, sir.')
                    restart_system()

                