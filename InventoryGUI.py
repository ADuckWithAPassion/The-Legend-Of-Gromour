from ShopGUI import *

class InventoryGUI(Tk):

    def __init__(self):

        #WINDOW
        Tk.__init__(self) # run tkinter.Tk's initializer
        self.geometry('320x400+0+0')# set the dimensions to 320 x 400 in the top left corner of your screen
        self.resizable(width=False, height=False)# Do not allow the menu to be resized 

        #FRAME
        self.frame = Frame(self,bg='black')

        self.frame.place(relx=0,rely=0,relheight=1,relwidth=1)
        
        #FONTS
        self.font_title = font.Font(family="Comic Sans MS",weight=font.BOLD, size=35)
        self.font_text = font.Font(family="Comic Sans MS", size=16,weight=font.BOLD)
        self.font_option = font.Font(family="Comic Sans MS", size=9,weight=font.BOLD)
        self.font_stat = font.Font(family="Comic Sans MS",size=7,weight=font.BOLD)

        #WIDGETS
        self.config(bg='black')
        
        name = Label(self.frame,text='Player Name',font=self.font_title,bg='#84DE02',fg='black')
        leave = Button(self.frame,text='Leave',font=self.font_option,command=lambda:self.exit_inventory()) # a button that closes the inventory on click

        self.gold = StringVar() # Empty StringVar()s which will have data set within them
        self.helmet = StringVar()
        self.breastplate = StringVar()
        self.weapon = StringVar()
        self.bow = StringVar()
        self.arrow = StringVar()
        self.current_item = StringVar()

        self.gold.set("Gold:"+str(Heroes['Player'].attributes['Gold'])) # look inside the player object to get their attributes
        self.helmet.set("Helmet:"+Heroes['Player'].attributes['Helmet']) # store data within the StringVar()s
        self.breastplate.set("Breastplate:"+Heroes['Player'].attributes['Breastplate']) # this will update the GUI
        self.weapon.set("Weapon:"+Heroes['Player'].attributes['Weapon'])
        self.bow.set("Bow:"+Heroes['Player'].attributes['Bow'])
        self.arrow.set("Arrow:"+Heroes['Player'].attributes['Arrow'])

        gold = Label(self.frame,textvariable=self.gold,font=self.font_stat) # creates a label 
        helmet = Label(self.frame,textvariable=self.helmet,font=self.font_stat)# these labels contain the updated StringVar()s
        breastplate = Label(self.frame,textvariable=self.breastplate,font=self.font_stat) 
        weapon = Label(self.frame,textvariable=self.weapon,font=self.font_stat)
        bow = Label(self.frame,textvariable=self.bow,font=self.font_stat)
        arrow = Label(self.frame,textvariable=self.arrow,font=self.font_stat)       
        current_item_stats = Label(self.frame,textvariable=self.current_item,font=self.font_stat)

        self.item_listbox = Listbox(self.frame,font=self.font_stat) # creates an empty listbox
        self.item_list = Heroes['Player'].return_items() # stores a list of the players item names

        equip = Button(self.frame,text='Equip',font=self.font_option,width=7,command=lambda:self.equip(self.item_listbox.get(ACTIVE))) # a button to run equip()
        unequip = Button(self.frame,text='Unequip',font=self.font_option,width=7,command=lambda:self.unequip(self.item_listbox.get(ACTIVE))) # a button to run unequip()
        
        for item in self.item_list: # loops through the player's items
            self.item_listbox.insert('end', item[0]) # add them to the listbox

        self.item_listbox.bind('<ButtonRelease-1>', self.get_item_info)

        name.place(relx=0.5,rely=0.1,anchor=CENTER)
        gold.place(relx=0.1,rely=0.8)
        helmet.place(relx=0.45,rely=0.25)
        breastplate.place(relx=0.45,rely=0.35)
        weapon.place(relx=0.45,rely=0.45)
        bow.place(relx=0.45,rely=0.55)
        arrow.place(relx=0.45,rely=0.65)
        name.place(relx=0.5,rely=0.1,anchor=CENTER)
        leave.place(relx=0.1,rely=0.875)
        self.item_listbox.place(relx=0.05,rely=0.35)
        equip.place(relx=0.05,rely=0.25)
        unequip.place(relx=0.25,rely=0.25)
        leave.place(relx=0.1,rely=0.875)
        current_item_stats.place(relx=0.45,rely=0.75)

        self.current_item.set("Select an item\n to view its information!")

    def get_item_info(self,event): # event is the mouse click

        try:

            index = self.item_listbox.curselection()[0] # get position of item selected in listbox
            text = self.item_listbox.get(index)  # get text of the item at that position
            amount = Heroes['Player'].return_items()[index][1] # get the stock of that item from player's inventory
            self.current_item.set((item_database[text].attributes.get_information()+'\nAmount:'+amount)) # runs the get_information function to get information exlusive to the item type

        except:

            pass

    def equip(self,selected):

        item_database[selected].attributes.equip(selected) # get the item object and run its equip function

        self.helmet.set("Helmet:"+Heroes['Player'].attributes['Helmet']) # store data within the StringVar()s
        self.breastplate.set("Breastplate:"+Heroes['Player'].attributes['Breastplate']) # this will update the GUI
        self.weapon.set("Weapon:"+Heroes['Player'].attributes['Weapon'])
        self.bow.set("Bow:"+Heroes['Player'].attributes['Bow'])
        self.arrow.set("Arrow:"+Heroes['Player'].attributes['Arrow'])

    def unequip(self,selected):

        item_database[selected].attributes.unequip(selected) # get the item object and run its unequip function

        self.helmet.set("Helmet:"+Heroes['Player'].attributes['Helmet']) # store data within the StringVar()s
        self.breastplate.set("Breastplate:"+Heroes['Player'].attributes['Breastplate']) # this will update the GUI
        self.weapon.set("Weapon:"+Heroes['Player'].attributes['Weapon'])
        self.bow.set("Bow:"+Heroes['Player'].attributes['Bow'])
        self.arrow.set("Arrow:"+Heroes['Player'].attributes['Arrow'])

    def exit_inventory(self):

        Heroes['Player'].save_data()
        self.destroy()

def startup_inventory(): 

    app = InventoryGUI() # create a tkinter object
    mainloop() # run and update the tkinter object

#startup_inventory() run the inventory

