from tkinter import *


class BattleGUI(Tk):

    def __init__(self):

        #WINDOW
        Tk.__init__(self) # run tkinter.Tk's initializer
        self.geometry('320x400+0+0') # set the dimensions to 320 x 400 in the top left corner of your screen
        self.resizable(width=False, height=False) # Do not allow the menu to be resized 

        self.font_title = font.Font(family="Comic Sans MS",weight=font.BOLD, size=20) # fonts for titles
        self.font_text = font.Font(family="Comic Sans MS",weight=font.BOLD, size=14) # fonts for text
        self.font_button = font.Font(family="Comic Sans MS",weight=font.BOLD, size=17) # fonts for buttons

        #FRAMES
        self.main_menu = Frame(self,bg='black') # main menu frame with a black background
        self.move_menu = Frame(self,bg='black') # move menu frame with a black background
    
        for frame in (self.main_menu,self.move_menu): # loop through all of the frames 
            frame.place(relx=0,rely=0,relheight=1,relwidth=1) # place them

        self.main_menu.tkraise() # raise menu frame to the top layer

    
def startup_battle():

    BattleGUI()
    mainloop()

startup_battle()
