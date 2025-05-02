from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re, pyttsx3

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()

def google_search(command):
    # Check if 'for' exists in the command to avoid IndexError
    if "for" in command:
        search_for = command.split("for", 1)[1]
    else:
        speak("Sorry, I didn't catch what you want to search for.")
        return
    
    reg_ex = re.search('search google for (.*)', command)
    if reg_ex:
        subgoogle = reg_ex.group(1)
        speak("Okay sir!")
        speak(f"Searching for {subgoogle}")
        
        # Correct executable path for ChromeDriver, not Chrome itself
        driver = webdriver.Chrome(executable_path="Application\\chrome.exe")
        driver.get("https://www.google.com")
        
        search = driver.find_element(By.NAME, "q")
        search.send_keys(str(search_for))
        search.send_keys(Keys.RETURN)
    else:
        speak("No valid search term found.")
