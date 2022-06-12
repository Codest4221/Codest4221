# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 17:53:13 2022

@author: Furkan Can
"""

from googlesearch import search
import subprocess
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
#from client.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import sys
import cv2 
from selenium import webdriver
from PIL import Image
import PIL.ImageOps
import time
import numpy as np


"""
Now we will set our engine to Pyttsx3 which is used for text to speech in 
Python and sapi5 is Microsoft speech application platform interface we will 
be using this for text to speech function.

You can change voice Id to “0” for Male voice while using assistant here 
we are using Female voice for all text to speech
"""

def speak(text):
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty("rate", 180)
        engine.say(text)
        engine.runAndWait()
    except:
        speak("Yemek molasındayım. Sonra konuşuruz.")
        sys.exit()

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak("Good Morning Sir !")

	elif hour>= 12 and hour<18:
		speak("Good Afternoon Sir !")

	else:
		speak("Good Evening Sir !")

	assname =("Jarvis")
	speak("I am your Assistant")
	speak(assname)

def username():
	speak("What should i call you sir")
	uname = takeCommand()
	speak("Welcome Mister")
	speak(uname)
	columns = shutil.get_terminal_size().columns
	
	print("#####################".center(columns))
	print("Welcome Mr.", uname.center(columns))
	print("#####################".center(columns))
	
	speak("How can i Help you, Sir")

def takeCommand():
	
	r = sr.Recognizer()
	
	with sr.Microphone() as source:
		
		print("Listening...")
		r.pause_threshold = 1
		audio = r.listen(source)

	try:
		print("Recognizing...")
		query = r.recognize_google(audio, language ='en-in')
		print(f"User said: {query}\n")

	except Exception as e:
		print(e)
		print("Unable to Recognize your voice.")
		return "None"
	
	return query

def starting(urls):
    try:
        for url in urls:
            webbrowser.open(url)
    except:
        konus("Google erişiminde bir hata oluştu.")
        sys.exit


def searching(word, number):
    try:
        lst = []
        for url in search(word, lang="en", stop=number):
            lst.append(url)
        return lst
    except:
        konus("Google erişiminde bir hata oluştu.")
        sys.exit()


# Main codes --- All the commands start from here
if __name__ == '__main__':
	clear = lambda: os.system('cls')
	
	# This Function will clean any
	# command before execution of this python file
	clear()
	wishMe()
	username()
	
	while True:
		
		query = takeCommand().lower()
		
		# All the commands said by user will be
		# stored here in 'query' and will be
		# converted to lower case for easily
		# recognition of command
		if 'wikipedia' in query:
			speak('Searching Wikipedia...')
			query = query.replace("wikipedia", "")
			results = wikipedia.summary(query, sentences = 3)
			speak("According to Wikipedia")
			print(results)
			speak(results)

		elif 'open youtube' in query:
			speak("Here you go to Youtube\n")
			starting(searching("youtube",1))

		elif 'youtube' in query:
			query = query.replace("youtube", "")
			speak("Here you go to Youtube\n")
			starting(searching(query+"youtube",1))

		elif 'open google' in query:
			speak("Here you go to Google\n")
			starting(searching("google",1))

		elif 'google' in query:
			query = query.replace("google", "")
			speak("Here you go to Google\n")
			starting(searching(query+"google",1))

		elif 'time' in query:
			strTime = datetime.datetime.now().strftime("% H:% M:% S")
			speak(f"Sir, the time is {strTime}")

		elif 'how are you' in query:
			speak("I am fine, Thank you")
			speak("How are you, Sir")

		elif 'fine' in query or "good" in query:
			speak("It's good to know that your fine")

		elif "change my name to" in query:
			query = query.replace("change my name to", "")
			assname = query

		elif "change name" in query:
			speak("What would you like to call me, Sir ")
			assname = takeCommand()
			speak("Thanks for naming me")

		elif "what's your name" in query or "What is your name" in query:
			speak("My friends call me")
			speak(assname)
			print("My friends call me", assname)

		elif 'exit' in query:
			speak("Thanks for giving me your time")
			exit()

		elif 'search' in query or 'play' in query:
			
			query = query.replace("search", "")
			query = query.replace("play", "")		
			webbrowser.open(query)

		elif "who i am" in query:
			speak("If you talk then definitely your human.")

		elif "why you came to world" in query:
			speak("It's a secret")

		elif 'power point presentation' in query:
			speak("opening Power Point presentation")
			power = r"C:\\Users\\Furkan Can\\Desktop\\Voice Assistant.pptx"
			os.startfile(power)

		elif 'is love' in query:
			speak("It is 7th sense that destroy all other senses")

		elif 'lock window' in query:
				speak("locking the device")
				ctypes.windll.user32.LockWorkStation()

		elif 'shutdown system' in query:
				speak("Hold On a Sec ! Your system is on its way to shut down")
				subprocess.call('shutdown / p /f')

		elif "don't listen" in query or "stop listening" in query:
			speak("for how much time you want to stop jarvis from listening commands")
			a = int(takeCommand())
			time.sleep(a)
			print(a)
		
		elif "where is" in query:
			query = query.replace("where is", "")
			location = query
			speak("User asked to Locate")
			speak(location)
			webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"))
			webbrowser.get('chrome').open_new_tab('https://www.google.com/maps/place/' + location + "")

		elif "camera" in query or "take a photo" in query:
			# program to capture single image from webcam in python

			# importing OpenCV library

			# initialize the camera
			# If you have multiple camera connected with
			# current device, assign a value in cam_port
			# variable according to that
			cam_port = 0
			cam = cv2.VideoCapture(cam_port)

			# If image will detected without any error,
			# show result
			i = 0
			while 1:
				i += 1
				# reading the input using the camera
				result, image = cam.read()
				# showing result, it take frame name and image
				# output
				cv2.imshow("voice", image)
				if i==100:
				# saving image in local storage
					cv2.imwrite("voice.png", image)
					break
			
				# If keyboard interrupt occurs, destroy image
				# window
				if cv2.waitKey() & 0xFF == ord('q'):
					break
				
			cv2.destroyWindow("voice")

			# If captured image is corrupted, moving to else part

		elif "write a note" in query:
			speak("What should i write, sir")
			note = takeCommand()
			file = open('jarvis.txt', 'w')
			speak("Sir, Should i include date and time")
			snfm = takeCommand()
			if 'yes' in snfm or 'sure' in snfm:
				strTime = datetime.datetime.now().strftime("%H:%M:%S")
				file.write(strTime+"\n")
				file.write(note)
			else:
				file.write(note)	

		elif "show the note" in query:
			speak("Showing Notes")
			file = open("jarvis.txt", "r")
			print(file.read())
			speak(file.read(6))
		elif "weather" in query:
						#!/usr/bin/env python

			# use selenium to take webpage screen shot based on stackoverflow from Corey Goldberg
			# http://stackoverflow.com/questions/3422262/take-a-screenshot-with-selenium-webdriver/6282203#6282203
			# http://stackoverflow.com/questions/3422262/take-a-screenshot-with-selenium-webdriver

			

			fox = webdriver.Chrome("C:\\Program Files (x86)\\chromedriver.exe")
			fox.get('https://weather.com/tr-TR/kisisel/bugun/l/TUXX0002:1:TU?Goto=Redirected')

			time.sleep(5)

			element = fox.find_element_by_id('WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034')
			location = element.location
			size = element.size
			fox.save_screenshot('weather_mn.png')
			fox.quit()

			# trim selenium screen shot inspired from stackoverlow
			# http://stackoverflow.com/questions/15018372/how-to-take-partial-screenshot-with-selenium-webdriver-in-python

			im = Image.open('weather_mn.png')

			left = location['x']
			top = location['y']
			# dimensions added to capture just widget area
			right = location['x'] + 500
			bottom = location['y'] + 245

			im = im.crop((left, top, right, bottom)) # defines crop points

			im = im.convert("RGB")
			im = PIL.ImageOps.invert(im)

			im = im.convert("RGBA")
			datas = im.getdata()


			# make portions of image transparent inspired from stackoverflow by cr333
			# http://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent

			newData = []
			for item in datas:

				if item[0] == 0 and item[1] == 0 and item[2] == 0:
					newData.append((255, 255, 255, 0))
				else:
					newData.append(item)

			im.putdata(newData)

			# replace colors based on stackoverflow from Joe Kington
			# http://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color

			data = np.array(im)   # "data" is a height x width x 4 numpy array
			red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

			white_areas = (red == 0) & (blue == 0) & (green == 0)
			data[..., :-1][white_areas] = (255, 255, 255)

			im2 = Image.fromarray(data)

			im2.save("weather_mn_desktop.png", "PNG")

		
		"""elif "weather" in query:
			
			# Google Open weather website
			# to get API of Open weather
			api_key = "Api key"
			base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
			speak(" City name ")
			print("City name : ")
			city_name = takeCommand()
			complete_url = base_url + "appid =" + api_key + "&q =" + city_name
			response = requests.get(complete_url)
			x = response.json()
			
			if x["cod"] != "404":
				y = x["main"]
				current_temperature = y["temp"]
				current_pressure = y["pressure"]
				current_humidiy = y["humidity"]
				z = x["weather"]
				weather_description = z[0]["description"]
				print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))
			
			else:
				speak(" City Not Found ")"""
