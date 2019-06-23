from SpriteSheet import *

class BattleGUI(Tk):

    def __init__(self,battle):

        self.battle = battle # copy of the battle going on

        #WINDOW
        Tk.__init__(self) # run tkinter.Tk's initializer
        self.geometry('320x460+0+0') # set the dimensions to 320 x 400 in the top left corner of your screen
        self.resizable(width=False, height=False) # Do not allow the menu to be resized 

        self.font_title = font.Font(family="Comic Sans MS",weight=font.BOLD, size=20) # fonts for titles
        self.font_text = font.Font(family="Comic Sans MS",weight=font.BOLD, size=10) # fonts for text
        self.font_button = font.Font(family="Comic Sans MS",weight=font.BOLD, size=17) # fonts for buttons
        self.font_option = font.Font(family="Comic Sans MS",weight=font.BOLD, size=17) # fonts for buttons

        #FRAMES
        self.main_menu = Frame(self,bg='black') # main menu frame with a black background
        self.move_menu = Frame(self,bg='black') # move menu frame with a black background
        self.item_menu = Frame(self,bg='black') # item menu frame with a black background
        
        for frame in (self.main_menu,self.move_menu,self.item_menu): # loop through all of the frames 
            frame.place(relx=0,rely=0,relheight=1,relwidth=1) # place them

        self.main() # load main frame
        self.move() # load move frame
        self.item() # load item frame
        
        self.main_menu.tkraise() # raise menu frame to the top layer

    def main(self):
        
        player_name = str(self.battle.player.name) # all of the player's stats
        player_health = str(self.battle.player.health)
        player_strength = str(self.battle.player.strength)
        player_speed = str(self.battle.player.speed)
        player_gold = str(self.battle.player.gold)
        player_xp = str(self.battle.player.xp)
        player_max_health = str(self.battle.player.max_health)

        attacker_name = str(self.battle.attacker.name) # all of the attacker's stats
        attacker_health = str(self.battle.attacker.health)
        attacker_strength = str(self.battle.attacker.strength)
        attacker_speed = str(self.battle.attacker.speed)
        attacker_gold = str(self.battle.attacker.gold)
        attacker_xp = str(self.battle.attacker.xp)
        
        menu_legend_label = Label(self.main_menu,text='The Legend Of Gromur',font=self.font_title,bg='#84DE02') # create the widget objects (background colour is a bright green)
        menu_player_label = Label(self.main_menu,text='Name:'+player_name+'\nHealth:'+player_health+'/'+player_max_health+'\nStrength:'+player_strength+'\nSpeed:'+player_speed+'\n\nCurrent Gold:'+player_gold+'\nXP to level up:'+player_xp,font=self.font_text,bg='#FFFFFF',width=15) # create the widget objects (background colour is white)
        menu_entity_label = Label(self.main_menu,text='Name:'+attacker_name+'\nHealth:'+attacker_health+'\nStrength:'+attacker_strength+'\nSpeed:'+attacker_speed+'\n\nGold to drop:'+attacker_gold+'\nXP to drop:'+attacker_xp,font=self.font_text,bg='#FFFFFF',width=15) # create the widget objects (background colour is white)
        menu_attack_button = Button(self.main_menu,text='Attack!',font=self.font_button,command=lambda:self.raise_move(),width=8) # runs raise_move on click
        menu_run_button = Button(self.main_menu,text='Run!',font=self.font_button,width=8)
        menu_item_button = Button(self.main_menu,text='Items',font=self.font_button,width=8,command=lambda:self.raise_item())

        menu_legend_label.place(relx=0.5,rely=0.1,anchor=CENTER) # place the widget objects
        menu_player_label.place(relx=0.05,rely=0.20)
        menu_entity_label.place(relx=0.55,rely=0.20)
        menu_attack_button.place(relx=0.05,rely=0.55)
        menu_run_button.place(relx=0.55,rely=0.55)
        menu_item_button.place(relx=0.05,rely=0.7)

    def move(self):

        player_name = str(self.battle.player.name) # all of the player's stats
        player_health = str(self.battle.player.health)
        player_strength = str(self.battle.player.strength)
        player_speed = str(self.battle.player.speed)
        player_gold = str(self.battle.player.gold)
        player_xp = str(self.battle.player.xp)
        player_max_health = str(self.battle.player.max_health)

        attacker_name = str(self.battle.attacker.name) # all of the attacker's stats
        attacker_health = str(self.battle.attacker.health)
        attacker_strength = str(self.battle.attacker.strength)
        attacker_speed = str(self.battle.attacker.speed)
        attacker_gold = str(self.battle.attacker.gold)
        attacker_xp = str(self.battle.attacker.xp)
        
        menu_legend_label = Label(self.move_menu,text='The Legend Of Gromur',font=self.font_title,bg='#84DE02') # create the widget objects (background colour is a bright green)
        menu_player_label = Label(self.move_menu,text='Name:'+player_name+'\nHealth:'+player_health+'/'+player_max_health+'\nStrength:'+player_strength+'\nSpeed:'+player_speed+'\n\nCurrent Gold:'+player_gold+'\nXP to level up:'+player_xp,font=self.font_text,bg='#FFFFFF',width=15) # create the widget objects (background colour is white)
        menu_entity_label = Label(self.move_menu,text='Name:'+attacker_name+'\nHealth:'+attacker_health+'\nStrength:'+attacker_strength+'\nSpeed:'+attacker_speed+'\n\nGold to drop:'+attacker_gold+'\nXP to drop:'+attacker_xp,font=self.font_text,bg='#FFFFFF',width=15) # create the widget objects (background colour is white)
        menu_movea_button = Button(self.move_menu,text=self.battle.player.move_list[0].name,font=self.font_option,width=8,command=lambda:self.attack(0))  
        menu_moveb_button = Button(self.move_menu,text=self.battle.player.move_list[1].name,font=self.font_option,width=8,command=lambda:self.attack(1))
        menu_movec_button = Button(self.move_menu,text=self.battle.player.move_list[2].name,font=self.font_option,width=8,command=lambda:self.attack(2))
        menu_back_button = Button(self.move_menu,text='Back',font=self.font_option,width=8,command=lambda:self.raise_main())
        menu_player_damage = Label(self.move_menu,text=self.battle.player.attack_text,font=self.font_text,width=35,anchor='w') # create the widget objects (background colour is a bright green)
        menu_attacker_damage = Label(self.move_menu,text=self.battle.attacker.attack_text,font=self.font_text,width=35,anchor='w') # create the widget objects (background colour is a bright green)

        menu_legend_label.place(relx=0.5,rely=0.1,anchor=CENTER) # place the widget objects
        menu_player_label.place(relx=0.05,rely=0.20)
        menu_entity_label.place(relx=0.55,rely=0.20)
        menu_movea_button.place(relx=0.05,rely=0.55)
        menu_moveb_button.place(relx=0.55,rely=0.55)
        menu_movec_button.place(relx=0.05,rely=0.7)
        menu_back_button.place(relx=0.55,rely=0.7)

        if self.battle.player.attack_text != '': # ensure that a move has been made

            menu_player_damage.place(relx=0.05,rely=0.85)
            menu_attacker_damage.place(relx=0.05,rely=0.92)

    def item(self):

        self.current_item = StringVar()
        self.stats = StringVar()

        item_legend_label = Label(self.item_menu,text='The Legend Of Gromur',font=self.font_title,bg='#84DE02') # create the widget objects (background colour is a bright green)
        current_item_stats = Label(self.item_menu,textvariable=self.current_item,font=self.font_text)
        item_back_button = Button(self.item_menu,text='Back',font=self.font_option,width=8,command=lambda:self.raise_main())
        item_use_button = Button(self.item_menu,text='Use item',font=self.font_option,width=8,command=lambda:self.use_item(self.item_listbox.get(ACTIVE)))
        important_stats = Label(self.item_menu,textvariable=self.stats,font=self.font_text,width=15,anchor='w')
        
        self.item_listbox = Listbox(self.item_menu,font=self.font_text) # creates an empty listbox
        self.item_list = Heroes['Player'].return_battle_items() # stores a list of the Player's items that can be used in battle

        for item in self.item_list: # loops through the player's items
            self.item_listbox.insert('end', item[0]) # add them to the listbox

        self.item_listbox.bind('<ButtonRelease-1>', self.get_item_info)

        item_legend_label.place(relx=0.5,rely=0.1,anchor=CENTER) # place the widget objects
        item_back_button.place(relx=0.05,rely=0.85)
        item_use_button.place(relx=0.05,rely=0.7)
        self.item_listbox.place(relx=0.05,rely=0.2)
        current_item_stats.place(relx=0.45,rely=0.7)
        important_stats.place(relx=0.57,rely=0.2)

        self.current_item.set("Select an item\n to view its information!")
        self.stats.set("")

    def get_item_info(self,event):
        
        try:

            index = self.item_listbox.curselection()[0] # get position of item selected in listbox
            text = self.item_listbox.get(index)  # get text of the item at that position

            for counter,item in enumerate(Heroes['Player'].return_items()):

                if item[0] == text:

                    amount = item[1]

            self.current_item.set((item_database[text].attributes.get_information()+'\nAmount:'+amount)) # runs the get_information function to get information exlusive to the item type
            self.stats.set(item_database[text].attributes.get_stats(self.battle))

        except:

            pass
        

    def raise_move(self):

        self.move()
        self.move_menu.tkraise() # raise move frame to the top layer

    def raise_main(self):

        self.main()
        self.main_menu.tkraise() # raise menu frame to the top layer

    def raise_item(self):

        self.item_menu = Frame(self,bg='black') # item menu frame with a black background
        self.item_menu.place(relx=0,rely=0,relheight=1,relwidth=1)
        self.item()
        self.item_menu.tkraise() # raise item frame to the top layer

    def attack(self,move_position):

        self.battle.battle_loop(move_position,self) # attack your opponent

        if not self.battle.ended:

            self.main() # update the stats on main frame
            self.move() # update the stats on move frame
            self.item() # update the stats in item frame

    def use_item(self,item):

        item_database[item].attributes.effect(self.battle.player,self.battle.attacker,self) # run selected item's effect procedure
        self.battle.battle_loop(None,self,True) # run battle_loop without getting the player's move
        self.raise_main() 
        
def startup_battle(battle):

    BattleGUI(battle)
    mainloop()
    
