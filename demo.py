import speech_recognition as sr
from time import ctime
import time
import os
import sys
from gtts import gTTS
import requests, json
listeningB = True


with open('config/homeassistant.json') as config:
    tdata = json.load(config)

with open('config/general.json') as config:
    gdata = json.load(config)

light_names = tdata["light_unfriendly_names"]
tbaseurl = tdata["protocol://hostname:port"]
aname = gdata["assistantName"]
callingCard = "hey " + aname

def turnOffLight(unFriendlyName):
    url = "http://IP_ADDRESS:8123/api/states/binary_sensor.nonfriendly69name420".replace("http://IP_ADDRESS:8123",baseurl).replace("nonfriendly69name420",unFriendlyName)
    h = {
        "Authorization": "Bearer LONG_LIVED_ACCESS_TOKEN",
        "content-type": "application/json",
    }
    d = json.dumps({state: "off"})
    return requests.post(url, headers = h, data = d);

def turnOnLight(unFriendlyName):
    url = "http://IP_ADDRESS:8123/api/states/binary_sensor.nonfriendly69name420".replace("http://IP_ADDRESS:8123",baseurl).replace("nonfriendly69name420",unFriendlyName)
    h = {
        "Authorization": "Bearer LONG_LIVED_ACCESS_TOKEN",
        "content-type": "application/json",
    }
    d = json.dumps({state: "on"})
    return requests.post(url, headers = h, data = d);

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(aname + " is listening...")
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
            for name in light_names:
                turnOffLight(name)
            print('Listening stopped')
            return listening

        if "good night" in data:
            listening = False
            respond("Turning off the lights.")
            for name in light_names:
                turnOffLight(name)
            print('Listening stopped')
            return listening

        if "turn on the lights" in data:
            listening = True
            respond("Turning on the lights.")
            for name in light_names:
                turnOnLight(name)
            print('Listening stopped')
            return listening

        if "bye" in data:
            listening = False
            respond("Goodbye.")
            print('Listening stopped')
            return listening

        if "what is" in data:
            url = "https://api.duckduckgo.com/?q=querytest123&format=json&pretty=1"
            urlPlus = data.replace(" ", "%20")
            url = url.replace("querytest123", urlPlus)
            response = requests.request("GET", url, headers=headers)
            data = response.json()
            dataText = '"' + data["Abstract"] + '", from ' + data["AbstractSource"] + ', powered by DuckDuckGo.'
            respond(dataText)

    if not listeningB:
        if callingCard in data:
            listening = False
            respond("Hello, how can I help you?")
            print('Listening stopped')
            return listening
    return listeningB

while True:
    data = listen()
    listeningC = digital_assistant(data)
    listeningB = listeningC