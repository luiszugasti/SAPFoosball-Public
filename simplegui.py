import tkinter as GUI_instance
from PIL import ImageTk, Image
import os
import time
import serial #to obtain arduino reading
import re #extract string

#Example showing quick prototype of the simpleGUI for foosball table, using tkinter and the
#simple pack organization. This code is written for python3.5

#Version 1.1
#Changes: modify code to allow for new sensor setup.
#Add start of game routine and game modes and end of game routine.


class Foosball_app():

    def __init__(self):
	#Open the serial port
        self.port = serial.Serial('/dev/ttyACM0',9600)

	#Define the Gui instance with Tk
        self.root = GUI_instance.Tk()
        self.root.geometry('1920x1080') #HD
        self.root.title("Foosball GUI")

	#Structure of GUI, instance variables
        self.lbl_red = GUI_instance.Label(text="a", bg="red", fg="white", font=("Arial Bold", 200))
        self.lbl_blue = GUI_instance.Label(text="b", bg="blue", fg="white", font=("Arial Bold", 200))
		#This is in case the user decides for a timed game!!! :)
		self.lbl_black = GUI_instance.Label(text = "" bg = "black" fg ="white" font =("Arial Bold", 100))
		self.lbl_black.pack(side = "bottom", fill = "x", expand = "yes")
        self.lbl_red.pack(side = "left", fill = "both", expand = "yes")
        self.lbl_blue.pack(side = "left", fill = "both", expand = "yes")
        self.red_score = 0
        self.blue_score = 0
		self.time = 0
		self.flag = 0
        self.temp_string = ""
        self.found = ""

	#run the startup method.
		game_start(self)
	#open the Tk window
        self.root.mainloop()

    #Permanent method that updates text and reads from Arduino, NEW: timed determines if we have a timer.
	#If timed is 0, we don't have a timer. If timed is 1, we have a timer.
	#Dont forget about overtime - Jordan Wang :)
    def update_score_not_timed(self):

        self.lbl_red.configure(text=self.red_score) #self.found
        self.lbl_blue.configure(text=self.blue_score) #self.temp_string

        #subroutine to parse through the serial port input
        self.temp_string = self.port.read(12).decode("utf-8")
					#Will get at least one portion of
					#byte stream that is not cut off
        #find first instance of red
        #cut it off
        try:
            self.found = re.search('\n(.+?)\n', self.temp_string).group(1)
        except AttributeError:
	    # AAA, ZZZ not found in the original string
            self.found = "R0 B0"#Default to nothing
        #Assume we have a string, lazy:
        #addition step, update score parameters
        if self.found == "R1 B0":
            self.red_score = self.red_score +1
			self.sleep()
        elif self.found == "R0 B1":
            self.blue_score = self.blue_score +1
			self.sleep()
        #score checks, win by 2 rule
        if (((self.blue_score > 10) | (self.red_score > 10)) & ((self.blue_score >= (self.red_score +2)))):
                self.blue_score = 0
                self.red_score = 0
				self.game_start()
        #I know this is redundant
        if (((self.blue_score > 10) | (self.red_score > 10)) & ((self.red_score >= (self.blue_score +2)))):
                self.blue_score = 0
                self.red_score = 0
				self.game_start()
        self.root.after(10, self.update_score_not_timed) #check every ten ms. , and run the method
                                                 #again.
									
		#Implements a single threaded timer for the python program.
def update_score_timed(self):
		
        self.lbl_red.configure(text=self.red_score) #self.found
        self.lbl_blue.configure(text=self.blue_score) #self.temp_string
		#Initialize timer for 10 minutes.
		if self.flag ==0:
			self.time=time.time()
			self.flag = 1
		
		self.lbl_black.configure(text=time.time() - self.time)
		if (time.time() - self.time) > 600:
			self.lbl_black(text="GAME OVER")
			self.blue_score = 0
            self.red_score = 0
			self.time=0
			self.flag=0
			self.game_start()
			
        #subroutine to parse through the serial port input
        self.temp_string = self.port.read(12).decode("utf-8")
					#Will get at least one portion of
					#byte stream that is not cut off
        #find first instance of red
        #cut it off
        try:
            self.found = re.search('\n(.+?)\n', self.temp_string).group(1)
        except AttributeError:
	    # AAA, ZZZ not found in the original string
            self.found = "R0 B0"#Default to nothing
        #Assume we have a string, lazy:
        #addition step, update score parameters
        if self.found == "R1 B0":
            self.red_score = self.red_score +1
			self.sleep()
        elif self.found == "R0 B1":
            self.blue_score = self.blue_score +1
			self.sleep()
        #score checks, win by 2 rule
        if (((self.blue_score > 10) | (self.red_score > 10)) & ((self.blue_score >= (self.red_score +2)))):
                self.blue_score = 0
                self.red_score = 0
				self.game_start()
        #I know this is redundant
        if (((self.blue_score > 10) | (self.red_score > 10)) & ((self.red_score >= (self.blue_score +2)))):
                self.blue_score = 0
                self.red_score = 0
				self.game_start()
        self.root.after(10, self.update_score_timed) #check every ten ms. , and run the method
                                                 #again.
												 
		#Stop checking for the score for a brief amount of time.
	def sleep(self):
		time.sleep(4)

	def game_start(self):
		self.lbl_red = GUI_instance.Label(text="<-Start 10 min. game", bg="red", fg="white", font=("Arial Bold", 200))
        self.lbl_blue = GUI_instance.Label(text="Start non timed game->", bg="blue", fg="white", font=("Arial Bold", 200))
		#Above: descriptive names for selection. If the user chooses to place the ball in the blue goal, then 
		#start game as usual, otherwise, if the player places the ball in the red goal, start a timer.
		
		#Selection criteria for timed/non timed game.
		try:
            self.found = re.search('\n(.+?)\n', self.temp_string).group(1)
        except AttributeError:
	    # AAA, ZZZ not found in the original string
            self.found = "R0 B0"#Default to nothing
        #Assume we have a string, lazy:
        #addition step, update score parameters
		if self.found == "R1 B0":
            self.update_score_not_timed()
        elif self.found == "R0 B1":
            self.update_score_timed()#need to change this!
		
#Instatiate app
app=Foosball_app()

#Previous code, FYI, this is not the proper way of using block comments in python!!! Don't do it!!!

"""
#String variables
blue_score = 0
red_score = 0

# Create a window
window = Tk()
window.geometry('1920x1080') #HD

#Elements of the window
window.title("Foosball GUI")

lbl_red = Label(window, text=red_score, bg="red", fg="white", font=("Arial Bold", 200))
lbl_blue = Label(window, text=blue_score, bg="blue", fg="white", font=("Arial Bold", 200))
lbl_status = Label(window, text="Status", bg="green", fg="white", font=("Arial Bold", 100))

#Simple pack (not fit for our use)
lbl_red.pack(side = "left", fill = "both", expand = "yes")
lbl_blue.pack(side = "left", fill = "both", expand = "yes")
#lbl_status.pack(side="bottom", fill = "both", expand = "yes")

#load an image into tkinter
#img = ImageTk.PhotoImage(Image.open("test.jpg"))
#panel = Label(window, image = img)
#panel.pack(side = "bottom", fill = "both", expand = "yes")

# Run the window loop
window.mainloop()
"""