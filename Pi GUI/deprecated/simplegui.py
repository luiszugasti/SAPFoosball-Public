import tkinter as GUI_instance
from PIL import ImageTk, Image
import sys
import os
import time
import serial   #to obtain arduino reading
import re 	#extract string

#Example showing quick prototype of the simpleGUI for foosball table, using tkinter and the
#simple pack organization. This code is written for python 3.5

#V1.04:
#Adding following features:
#Startup command that allows the disabling of the serial port instantiation, and instead allows the user to simulate goal scoring with the use of a keyboard.
#Clean up of the tkinter code, as well as running in full screen.

#Version 1.03
#Final version of communication between arduino. Arduino sends distances to the raspberry pi and the raspberry pi does 
#the following:
#	a) extract the numerical values of the string
#	b) place each numerical value within a list
# 	c) from that list, obtain the distance and decide upon what to do based on it.

class Foosball_app():

    def __init__(self, sensor):
        print(sensor)
        #Open the serial port
        self.port = serial.Serial('/dev/ttyACM0',9600)

	#Define the Gui instance with Tk
        self.root = GUI_instance.Tk()
        self.root.geometry('1920x1080') #HD
        self.root.title("Foosball GUI")

	#Structure of GUI, instance variables
        self.root.title("Foosball GUI")
        self.lbl_red = GUI_instance.Label(text="a", bg="red", fg="white", font=("Arial Bold", 200))
        self.lbl_blue = GUI_instance.Label(text="b", bg="blue", fg="white", font=("Arial Bold", 200))
        self.lbl_red.pack(side = "left", fill = "both", expand = "yes")
        self.lbl_blue.pack(side = "left", fill = "both", expand = "yes")
        self.red_score = 0
        self.blue_score = 0
        self.temp_string = ""
        self.found = ""
        self.final = [10] * 2

	#run the endless GUI logic
        self.update_score()
	#open the Tk window
        self.root.mainloop()

    #Permanent method that updates text and reads from Arduino
    def update_score(self):
        
        self.lbl_red.configure(text= self.red_score) #self.red_score
        self.lbl_blue.configure(text= self.blue_score) #self.blue_score

        # subroutine to parse through the serial port input
        self.temp_string = self.port.read(20).decode("ISO-8859-1")
					#Will get at least one portion of
					#byte stream that is not cut off
					#Expecting 20 character string. (Sampling theorem!)
        try:
            self.found = re.search('R(.+?)R', self.temp_string).group(1)
        except AttributeError:
	    # AAA, ZZZ not found in the original string
            self.found = "0000B0000"#Default to nothing
        #Assume we have a string, break it into distances from concatenation.
	#take in R####B####
	#Extract first number, place it in container RED, Extract second number, place it in container BLUE
        result = ''
        for ch in self.found:
            if ch == 'B':
                result = result + ' '
            else:
                result = result + ch
        print(result)
        #now we have string "#### ####"
	#Place red in the first pos of array, blue in second pos of array.
        self.final[0] = int(re.findall(r'\d+', result)[0])
        self.final[1] = int(re.findall(r'\d+', result)[1])

        #addition step, update score parameters
        if int(self.final[0]) <= 10:
            self.red_score = self.red_score +1
            time.sleep(1)
            self.port.flushInput()
        elif int(self.final[1]) <= 10:
            self.blue_score = self.blue_score +1
            time.sleep(1)
            self.port.flushInput()
            
        #score checks, win by 2 rule
        if (((self.blue_score > 10) | (self.red_score > 10)) & ((self.blue_score >= (self.red_score +2)))):
            self.blue_score = 0
            self.red_score = 0
        #I know this is redundant
        if (((self.blue_score > 10) | (self.red_score > 10)) & ((self.red_score >= (self.blue_score +2)))):
            self.blue_score = 0
            self.red_score = 0
       
        self.root.after(10, self.update_score) #check every ten ms. , and run the method
                                                 #again.        
#Instatiate app
if len(sys.argv) > 1: #Simple to not have to call error handlers
    if sys.argv[1] == "ns":
        #For now, skip running the app
        print("no sensor mode enabled")
        time.sleep(5)
        sensor = 0
else:
    print('default: sensor mode enabled (to disable, use:' , '\n' , '           python3 simplegui.py ns'\
    , '\n' 'to invoke the function.')
    time.sleep(5)
    sensor = 1
app=Foosball_app(sensor)