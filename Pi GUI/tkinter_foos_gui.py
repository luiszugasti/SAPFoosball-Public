import tkinter as GUI_instance    #GUI functionality
import sys                        #input parameters
import os
import time                       #sleep functionality
import serial                     #to obtain arduino reading
import re 	                  #extract string
import random                     #emulate games
import subprocess                 #play winning music!

#V1.04:
#Adding following features:
#Startup command that allows the disabling of the serial port instantiation, and instead allows the user to simulate goal scoring automatically.
#Clean up of the tkinter code, as well as running in full screen, addition of various fun sound bytes.

class Foosball_app():

    def __init__(self, sensor):
        print(sensor)
        #exit() #so it does not crash

	#Define the Gui instance with Tk
        self.root = GUI_instance.Tk()
        self.root.geometry('1920x1080') #HD
        self.root.title("Foosball GUI")

        #force Tkinter to run in full screen mode
        #self.root.overrideredirect(True)
        #self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

	#Structure of GUI, instance variables
        self.root.title("Foosball GUI")
        self.lbl_red = GUI_instance.Label(text="a", bg="red", fg="white", font=("Arial Bold", 200))
        self.lbl_blue = GUI_instance.Label(text="b", bg="blue", fg="white", font=("Arial Bold", 200))
        self.lbl_red.pack(side = "left", fill = "both", expand = "yes")
        self.lbl_blue.pack(side = "left", fill = "both", expand = "yes")
        self.red_score = 0
        self.blue_score = 0
        self.final = [10] * 2

	#run the endless GUI logic, depending on the value of sensor
        if sensor == "1":
            self.initiate_sensor()
            self.human_game()
        else:
            self.auto_game()
	#open the Tk window
        self.root.mainloop()

    #for most of these functions: self is passed as self is changed within!
    def initiate_sensor(self):
        #Open the serial port
        self.port = serial.Serial('/dev/ttyACM0',9600)
        
        #simple to run these pointers for looping, not neccessary if we're going to have keyboard inputs
        self.temp_string = "" 
        self.found = ""


    def human_game(self):
        #Method that updates text and reads from Arduino

        self.update_score(1)

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

        #check the sensor every ten milliseconds and then run the method again.
        self.root.after(10, self.human_game)

    def update_score(self, context):
        #takes all redundant code between auto_game and human_game into one concise little package.

        self.lbl_red.configure(text= self.red_score) #self.red_score
        self.lbl_blue.configure(text= self.blue_score) #self.blue_score

	#addition step, update score parameters
        if (int(self.final[0]) or int(self.final[1])) <= 10:
            random_goal = "goal" + str(random.randint(0,11)) + ".wav" #create our string
            player = subprocess.Popen(["mplayer", random_goal, "-ss", "0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if int(self.final[0]) <= 10:
            self.red_score = self.red_score +1
            time.sleep(1)
        elif int(self.final[1]) <= 10:
            self.blue_score = self.blue_score +1
            time.sleep(1)
        
        #need to flush the port if its a human game

        if context == 1:
            self.port.flushInput()
   
        #score checks, win by 2 rule
        if (((self.blue_score > 10) | (self.red_score > 10)) & ((self.blue_score >= (self.red_score +2)))):
            self.lbl_red.configure(text= self.red_score) #self.red_score
            self.lbl_blue.configure(text= self.blue_score) #self.blue_score
            player = subprocess.Popen(["mplayer", "win_final.mp3", "-ss", "0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.blue_score = 0
            self.red_score = 0
            time.sleep(10)
        #I know this is redundant
        if (((self.blue_score > 10) | (self.red_score > 10)) & ((self.red_score >= (self.blue_score +2)))):
            self.lbl_red.configure(text= self.red_score) #self.red_score
            self.lbl_blue.configure(text= self.blue_score) #self.blue_score
            self.blue_score = 0
            self.red_score = 0
            player = subprocess.Popen(["mplayer", "win_final.mp3", "-ss", "0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(10)

    def auto_game(self):
        #endless loop that simulates a game between "A.I" (not A.I.)
        
        ra = random.randint(0,10)
        if ra > 5:
            #simulate a red goal
            self.final[0] = 2
            self.final[1] = 200
        else:
            #simulate a blue goal
            self.final[0] = 200
            self.final[1] = 2
        self.update_score(0)
        self.root.after(100, self.auto_game)

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
