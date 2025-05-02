from Jarvis import JarvisAssistant
import re
import os
import random
import pprint
import datetime
import requests
import sys
import urllib.parse  
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from Jarvis.features import WikipediaSearch
obj = JarvisAssistant()
# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello Jarvis", "Jarvis", "wake up Jarvis", "you there Jarvis", "time to work Jarvis", "hey Jarvis",
             "ok Jarvis", "are you there"]
GREETINGS_RES = ["always there for you", "i am ready",
                 "your wish my command", "how can i help you ?", "i am online and ready "]

EMAIL_DIC = {
    'myself': 'example@gmail.com',
    'my official email': 'example@gmail.com',
    'my second email': 'example@gmail.com',
    'my official mail': 'example@gmail.com',
    'my second mail': 'example@gmail.com'
}

CALENDAR_STRS =["what do i have", "do i have plans", "am i busy"]
# =======================================================================================================================================================


def speak(text):
    obj.tts(text)
app_id = config.wolframalpha_id
def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry I couldn't fetch your question's answer. Please try again ")
        return None
def startup():
    speak("Initializing Jarvis")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Caliberating and examining all the core processors")
    speak("Checking the internet connection")
    speak("Wait a moment ")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("Now I am online")
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis")
    speak("Please tell me how may I help you")
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        startup()
        while True:
            command = obj.mic_input()

            if re.search('date', command):
                date = obj.tell_me_date()
                print(date)
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                print(time_c)
                speak(f" the time is {time_c}")

            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                }

                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                    print('Application path not found')

                else:
                    speak('Launching: ' + app + 'for you!')
                    obj.launch_any_app(path_of_app=path)

            elif command in GREETINGS:
                speak(random.choice(GREETINGS_RES))

            elif re.search('open website', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'Alright !! Opening {domain}')
                print(open_result)

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                print(weather_res)
                speak(weather_res)

            elif re.search(r'tell me about|who is', command):
                match = re.search(r'tell me about (.+)|who is (.+)', command)
                topic = match.group(1) or match.group(2) if match else None
                if topic:
                    gog_res =obj.tell_me(topic)
                    print(gog_res)
                    speak(gog_res)
                else:
                    speak("Sorry. I couldn't load your query. Please try again.")

            elif "buzzing" in command or "news" in command or "headlines" in command:
                news_res = obj.news()
                speak('Source: The Times Of India')
                speak('Todays Headlines are..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res)-2:
                        break
                speak('These were the top headlines, Have a nice day !!..')

            elif "hello" in command or "hi" in command or "hola" in command:
                print("hello , how i can help you............?")
                speak("hello , how i can help you............?")

            elif "how are you" in command or "how r u" in command or "h w r" in command:
                print("i am fine ............ , how are you............?")
                speak("i am fine ............ , how are you............?")

            elif "i am fine" in command or "i m fine" in command or "i'm fine" in command or "i am also fine" in command:
                print("glad to hear that , how can i help you............? ")
                speak("glad to hear that , how can i help you............? ")

            elif "thank you" in command or "thank u" in command or "thx" in command:
                print("welcome  ......., how can i help you............?")
                speak("welcome ........, how can i help you............?")

            elif "good morning" in command or "morning" in command:
                print("Good morning, Hope you have a productive day. How can I assist you?")
                speak("Good morning, Hope you have a productive day. How can I assist you?")

            elif "good afternoon" in command or "afternoon" in command:
                print("Good afternoon, How is your day going? How can I be of help?")
                speak("Good afternoon, How is your day going? How can I be of help?")

            elif "good evening" in command or "evening" in command:
                print("Good evening, How can I assist you this evening?")
                speak("Good evening, How can I assist you this evening?")

            elif "whats your name" in command or "who are you" in command or "hu r u" in command:
                print("I'm Jarvis , your personal assistant! How can I help you today?")
                speak("I'm Jarvis , your personal assistant! How can I help you today?")
            
            elif "object detection" in command or "detect the object" in command:
                print("opening object detection system ")
                speak("opening object detection system ")
                obj.detection()
            elif "close object detector" in command or "exit object detector" in command:
                print("Closing object detection system. Goodbye!")
                speak("Closing object detection system. Goodbye!")
                obj.objStope()
            elif "detect sign language" in command or "sign language detect" in command:
                print("opening sign detection system")
                speak("opening sign detection system ")
                obj.signdector()

            elif "close sign detector" in command or "exit sign detector" in command:
                print("Closing sign detection system. Goodbye!")
                speak("Closing sign detection system. Goodbye!")
                obj.stopsing()

            elif "do google " in command or "search on google" in command or "search in google" in command:
                obj.search_anything_google(command)
            
            elif "play music" in command or "hit some music" in command:
                music_dir = "driver\\music"
                songs = os.listdir(music_dir)
                for song in songs:
                    os.startfile(os.path.join(music_dir, song))
            elif('crack a joke' in command or 'joke' in command):
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif 'youtube' in command:
                video = command.split(' ')[1]
                speak(f"Okay, playing {video} on youtube")
                pywhatkit.playonyt(video)

            elif "email" in command or "send email" in command:
                sender_email = config.email
                sender_password = config.email_password

                try:
                    speak("Whom do you want to email ?")
                    recipient = obj.mic_input()
                    receiver_email = EMAIL_DIC.get(recipient)
                    if receiver_email:

                        speak("What is the subject ?")
                        subject = obj.mic_input()
                        speak("What should I say?")
                        message = obj.mic_input()
                        msg = 'Subject: {}\n\n{}'.format(subject, message)
                        obj.send_mail(sender_email, sender_password,
                                      receiver_email, msg)
                        speak("Email has been successfully sent")
                        time.sleep(2)

                    else:
                        speak(
                            "I coudn't find the requested person's email in my database. Please try again with a different name")
                except:
                    speak("Sorry. Couldn't send your mail. Please try again")
            elif "calculate" in command or "calculates" in command:
                speak("ok.....! calculating..........")
                query = command
                answer = computational_intelligence(query)
                speak(f"Answer for the {query} is {answer}")
            elif "what do i have" in command or "do i have plans" or "am i busy" in command:
                obj.google_calendar_events(command)

            if "make a note" in command or "write this down" in command or "remember this" in command:
                speak("What would you like me to write down?")
                note_text = obj.mic_input()
                obj.take_note(note_text)  # Calls the note function from note.py
                speak("I've made a note of that")

            elif "close the note" in command or "close notepad" in command:
                speak("Okay, closing notepad")
                os.system("taskkill /f /im notepad++.exe")

            elif "update me about system" in command:
                sys_info = obj.system_info()
                print(sys_info)
                speak(sys_info)

            elif "where is" in command:
                place = command.replace("where is", "").strip()
                speak("Showing location")
                try:
                    current_loc, target_loc, distance = obj.location(place)
                    if target_loc:
                        city = target_loc.get('city', '')
                        state = target_loc.get('state', '')
                        country = target_loc.get('country', '')

                        if city:
                            res = f"{place.title()} is in {state} state, {country}. It is {distance} km away from your current location."
                        else:
                            res = f"{state} is a state in {country}. It is {distance} km away from your current location."

                        print(res)
                        speak(res)
                    else:
                        speak("Could not retrieve detailed information about the location.")

                except Exception as e:
                    speak("Sorry, I couldn't fetch the location. Please try again.")
                    print(f"Error: {e}")

            elif "where is i am" in command or "tell me my location" in command or "current location" in command:
                speak("Your current location is")
                city, state=obj.my_location()
                speak(f"The City is: {city}, State is : {state}")
                print(f"The City is: {city}, and State is : {state}")

            elif "ip address" in command:
                ip = requests.get('https://api.ipify.org').text
                print(ip)
                speak(f"Your ip address is {ip}")

            elif "switch the window" in command or "switch window" in command:
                speak("Okay, Switching the window")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                speak("By what name do you want to save the screenshot?")
                name = obj.mic_input()
                speak("Alright , taking the screenshot")
                folder_path="Jarvis\\screenshorts"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, f"{name}.png")
                img = pyautogui.screenshot()
                name = f"{name}.png"
                img.save(file_path)
                speak(f"The screenshot has been succesfully captured and saved at screenshorts folder.")
                print(f"The screenshot has been succesfully captured and saved as {file_path}.")
            elif "show me screenshot" in command:
                try:
                    speak("Please tell me the name of the screenshot you want to see.")
                    screenshot_name = obj.mic_input()  # Ask the user for the screenshot name
                    file_path = f"Jarvis\\screenshorts\\{screenshot_name}.png"
                    if os.path.exists(file_path):
                        img = Image.open(file_path)
                        img.show()  # Display the image
                        speak("Here it is.")
                        time.sleep(2)  # Wait for a moment before closing (if needed)
                    else:
                        speak(f"Sorry, I could not find a screenshot named {screenshot_name}.")
                except IOError:
                    speak("Sorry, I am unable to display the screenshot")
            elif "hide all files" in command or "hide this folder" in command:
                os.system("attrib +h /s /d")
                speak("all the files in this folder are now hidden")
            elif "visible" in command or "make files visible" in command:
                os.system("attrib -h /s /d")
                speak("all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")
            elif "goodbye" in command or "offline" in command or "bye" in command:
                speak("Alright, going offline. It was nice working with you")
                sys.exit()
startExecution = MainThread()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    # def run(self):
    #     self.TaskExection
    def startTask(self):
        self.ui.movie = QtGui.QMovie("images\\bg_final.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("images\\initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)
app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())