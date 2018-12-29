import tkinter as GUI_instance
from PIL import ImageTk, Image
import os
import time
import serial #to obtain arduino reading
import re #extract string

#Example showing quick prototype of the simpleGUI for foosball table, using tkinter and the
#simple pack organization. This code is written for python3.5

#Version 1

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
        self.lbl_red.pack(side = "left", fill = "both", expand = "yes")
        self.lbl_blue.pack(side = "left", fill = "both", expand = "yes")
        self.red_score = 0
        self.blue_score = 0
        self.temp_string = ""
        self.found = ""

	#run the endless GUI logic
        self.update_score()
	#open the Tk window
        self.root.mainloop()

    #Permanent method that updates text and reads from Arduino
    def update_score(self):

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
        elif self.found == "R0 B1":
            self.blue_score = self.blue_score +1

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