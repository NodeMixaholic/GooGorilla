import speech_recognition as sr
from time import ctime
import time
import os
import sys
from gtts import gTTS
import requests, json
from tuyaha import TuyaApi
listeningB = True
tapi = TuyaApi()


with open('config/tuya.json') as config:
    tdata = json.load(config)

username,password,country_code,application = tdata['username'],tdata['password'],tdata['country_code'],tdata['application']
tapi.init(username,password,country_code,application)
device_ids = tapi.get_all_devices()
switch = dict(sorted(dict((i.name(),i) for i in device_ids if i.obj_type == 'switch').items()))
switch['All Switches'] = list(switch.values())
lights = dict(sorted(dict((i.name(),i) for i in device_ids if i.obj_type == 'light').items()))
lights['All Lights'] = list(lights.values())
devices = {**switch,**lights}

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sam is listening...")
        audio = r.listen(source)
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return data

def respond(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("ttssam.mp3")
    os.system("mpg321 ttssam.mp3")

def digital_assistant(data):
    if listeningB:
        if "hello" in data:
            listening = True
            respond("Hi, my name is Sam.")

        if "how are you" in data:
            listening = True
            respond("I am doing great.")

        if "what time is it" in data:
            listening = True
            respond(ctime())
        
        if "turn off the lights" in data:
            listening = True
            respond("Turning off the lights.")
            for i in device:
                i.turn_off()
            print('Listening stopped')
            return listening

        if "good night" in data:
            listening = False
            respond("Turning off the lights.")
            for i in device:
                i.turn_off()
            print('Listening stopped')
            return listening

        if "turn on the lights" in data:
            listening = True
            respond("Turning on the lights.")
            for i in device:
                i.turn_on()
            print('Listening stopped')
            return listening

        if "bye" in data:
            listening = False
            respond("Goodbye.")
            print('Listening stopped')
            return listening
    if not listeningB:
        if "hey sam" in data:
            listening = False
            respond("Hello, how can I help you?")
            print('Listening stopped')
            return listening
    return listeningB

while True:
    data = listen()
    listeningC = digital_assistant(data)
    listeningB = listeningC