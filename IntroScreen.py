import xml.etree.ElementTree as ET #allows use of the element tree library
from tkinter import *
import pygame as pygame
import sys
import time
import random
import os  

os.environ['SDL_VIDEO_WINDOW_POS'] = ('0,25')

class IntroGUI(Tk):

    def __init__(self): 

        #WINDOW
        Tk.__init__(self) # run tkinter.Tk's initializer
        self.geometry('320x400+0+0') # set the dimensions to 320 x 400 in the top left corner of your screen
        self.resizable(width=False, height=False) # Do not allow the menu to be resized 
        self.protocol("WM_DELETE_WINDOW", self.close) # if the window is closed, run the close procedure

        self.font_title = font.Font(family="Comic Sans MS",weight=font.BOLD, size=20) # fonts for titles
        self.font_text = font.Font(family="Comic Sans MS",weight=font.BOLD, size=14) # fonts for text

        #FRAMES
        self.main_menu = Frame(self,bg='black') # main menu frame with a black background
        self.control_menu = Frame(self,bg='black') # control menu frame with a black background
    
        for frame in (self.main_menu,self.control_menu): # loop through all of the frames 
            frame.place(relx=0,rely=0,relheight=1,relwidth=1) # place them

        self.main() # load the main frame
        self.controls() # load the controls frame

        self.main_menu.tkraise() # raise menu frame to the top layer

    def main(self):
        
        menu_legend_label = Label(self.main_menu,text='The Legend Of Gromur',font=self.font_title,bg='#84DE02') # create the widget objects (background colour is a bright green)
        menu_newgame_button = Button(self.main_menu,text='New Game',font=self.font_text,command=lambda:self.new_game())
        menu_loadgame_button = Button(self.main_menu,text='Load Game',font=self.font_text,command=lambda:self.load_game())
        menu_controls_button = Button(self.main_menu,text='Controls',font=self.font_text,command=lambda:self.raise_controls())
        menu_quit_button = Button(self.main_menu,text='Quit Game',font=self.font_text,command=lambda:self.close())

        menu_legend_label.place(relx=0.5,rely=0.1,anchor=CENTER) # place the widget objects
        menu_newgame_button.place(relx=0.5,rely=0.35,anchor=CENTER)
        menu_loadgame_button.place(relx=0.5,rely=0.5,anchor=CENTER)
        menu_controls_button.place(relx=0.5,rely=0.65,anchor=CENTER)
        menu_quit_button.place(relx=0.5,rely=0.8,anchor=CENTER)
        
    def controls(self):
        
        controls_menu_label = Label(self.control_menu,text='Controls',font=self.font_title,bg='#84DE02') # create the widget objects (background colour is a bright green)
        controls_up_label = Label(self.control_menu,text='Move up - W',font=self.font_text)
        controls_down_label = Label(self.control_menu,text='Move down - S',font=self.font_text)
        controls_left_label = Label(self.control_menu,text='Move left - A',font=self.font_text)
        controls_right_label = Label(self.control_menu,text='Move right - D',font=self.font_text)
        controls_inventory_label = Label(self.control_menu,text='Open inventory - C',font=self.font_text)
        controls_skip_label = Label(self.control_menu,text='Skip dialogue - E',font=self.font_text)
        controls_quit_button = Button(self.control_menu,text='Return',font=self.font_text,command=lambda:self.raise_menu())

        controls_menu_label.place(relx=0.5,rely=0.1,anchor=CENTER) # place the widget objects
        controls_up_label.place(relx=0.5,rely=0.25,anchor=CENTER)
        controls_down_label.place(relx=0.5,rely=0.35,anchor=CENTER)
        controls_left_label.place(relx=0.5,rely=0.45,anchor=CENTER)
        controls_right_label.place(relx=0.5,rely=0.55,anchor=CENTER)
        controls_inventory_label.place(relx=0.5,rely=0.65,anchor=CENTER)
        controls_skip_label.place(relx=0.5,rely=0.75,anchor=CENTER)
        controls_quit_button.place(relx=0.5,rely=0.9,anchor=CENTER)
        
    def raise_controls(self):

        self.control_menu.tkraise() # raise the control menu to the top (display controls)

    def raise_menu(self):

        self.main_menu.tkraise() # raise the main menu to the top

    def new_game(self):

        self.destroy() # close the Tkinter window
        
        global player_database # change's the variable's scope so that it can be accessed throughout the program (in XML when loading and main game when saving) 
        global player_data
        global inventory_database
        global inventory_data
        global items_database
        global items_data

        player_database = ET.parse("Testing.xml") #load in the player_database (a default version)
        player_data = player_database.getroot() #create an object containing the player_database

        inventory_database = ET.parse("Inventory_database.xml") #load in the inventory_database (a default version)
        inventory_data = inventory_database.getroot() #create an object containing the player_database

        items_database = ET.parse('Items_database.xml') #load in the items_database (a default version)
        items_data = items_database.getroot() #create an object containing the player_database

    def load_game(self):

        self.destroy() # close the Tkinter window

        global player_database # change's the variable's scope so that it can be accessed throughout the program (in XML when loading and main game when saving) 
        global player_data
        global inventory_database
        global inventory_data
        global items_database
        global items_data

        player_database = ET.parse("Player_database.xml") #load in the player_database (current save)
        player_data = player_database.getroot() #create an object containing the player_database

        inventory_database = ET.parse("UpdatedItems.xml") #load in the inventory_database (current save)
        inventory_data = inventory_database.getroot() #create an object containing the player_database

        items_database = ET.parse('Items_database.xml') #load in the items_database (current save)
        items_data = items_database.getroot() #create an object containing the player_database

        
    def close(self):

        self.destroy() # kill the Tkinter window object
        quit() # end python from running
        
    
def startup_intro():

    IntroGUI()
    mainloop()

startup_intro()
