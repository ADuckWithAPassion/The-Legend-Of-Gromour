from XML import * # run the XML.py file


class GUI(Tk): # create a tkinter object

    def __init__(self,owner): 

        self.owner = owner # name of shop keeper

        #WINDOW
        Tk.__init__(self) # run tkinter.Tk's initializer
        self.geometry('320x400+0+0') # set the dimensions to 320 x 400 in the top left corner of your screen
        self.resizable(width=False, height=False) # Do not allow the menu to be resized 

        #FONTS
        self.font_title = font.Font(family="Comic Sans MS",weight=font.BOLD, size=35)
        self.font_text = font.Font(family="Comic Sans MS", size=18,weight=font.BOLD)
        self.font_option = font.Font(family="Comic Sans MS", size=10,weight=font.BOLD)
        self.font_stat = font.Font(family="Comic Sans MS",size=8,weight=font.BOLD)
        self.font_error = font.Font(family="Comic Sans MS",size=8)
    
        #FRAMES
        self.main_menu = Frame(self,bg='black')
        self.buy_menu = Frame(self,bg='black')
        self.sell_menu = Frame(self,bg='black')

        for frame in (self.main_menu,self.buy_menu,self.sell_menu): # loop through all of the frames
            frame.place(relx=0,rely=0,relheight=1,relwidth=1) # place them

        self.menu()
        self.buy()
        self.sell()

        self.main_menu.tkraise() # raise menu frame to the top layer

    def menu(self):

        #MENU
        menu_name = Label(self.main_menu,text=(self.owner+"'s"+' Shop'),font=self.font_title,bg='#84DE02',fg='black') 
        menu_buy = Button(self.main_menu,text='Buy',font=self.font_text,command=lambda:self.raise_buy())
        menu_sell = Button(self.main_menu,text='Sell',font=self.font_text,command=lambda:self.raise_sell())
        menu_leave = Button(self.main_menu,text='Leave',font=self.font_text,command=lambda:self.exit_shop())

        self.player_gold=StringVar() # allows text
        self.player_gold.set("Your Gold:"+str(Heroes['Player'].attributes['Gold']))

        self.shop_gold=StringVar() # allows text
        self.shop_gold.set("Shop's Gold:"+str(Heroes[self.owner].attributes['Gold']))
        
        menu_name.place(relx=0.5,rely=0.1,anchor=CENTER)
        menu_buy.place(relx=0.1,rely=0.25)
        menu_sell.place(relx=0.1,rely=0.45)
        menu_leave.place(relx=0.1,rely=0.65)

    def buy(self):

        #BUY
        buy_name = Label(self.buy_menu,text=(self.owner+"'s"+' Shop'),font=self.font_title,bg='#84DE02',fg='black') # name of the shop
        buy_return = Button(self.buy_menu,bg='white',fg='black',text='Return',font=self.font_text,command=lambda:self.raise_main()) # button to return to main menu
        buy_purchase = Button(self.buy_menu,text='Purchase',font=self.font_text,command=lambda:self.purchase(self.buy_listbox.get(ACTIVE),buy_spinbox.get())) # button to buy selected item
        buy_player_gold = Label(self.buy_menu,textvariable=self.player_gold,font=self.font_stat) # amount of gold player has
        buy_shop_gold = Label(self.buy_menu,textvariable=self.shop_gold,font=self.font_stat) # amount of gold shop keeper has
        buy_spinbox = Spinbox(self.buy_menu, from_=1, to=32,width=5) # amount of item to buy
        self.current_buy = StringVar() 
        buy_current_item_stats = Label(self.buy_menu,textvariable=self.current_buy,font=self.font_stat) # current stats of the selected item
        self.buy_error_message = StringVar()
        self.buy_error_message.set('What would you like to buy?')
        buy_errors = Label(self.buy_menu,textvariable=self.buy_error_message,font=self.font_error)
        
        buy_name.place(relx=0.5,rely=0.1,anchor=CENTER)
        buy_return.place(relx=0.1,rely=0.65)
        buy_purchase.place(relx=0.1,rely=0.85)
        buy_player_gold.place(relx=0.65,rely=0.45)
        buy_shop_gold.place(relx=0.65,rely=0.35)
        buy_spinbox.place(relx=0.70,rely=0.25)
        buy_current_item_stats.place(relx=0.45,rely=0.60)
        buy_errors.place(relx=0.52,rely=0.90)

        self.update_buy()
         
    def update_buy(self):
        
        self.buy_listbox = Listbox(self.buy_menu, width=20, height=6,font=self.font_option) # an empty listbox
        self.buy_listbox.place(relx=0.1,rely=0.25)
        item_list = Heroes[self.owner].return_items() # list of the shop keeper's items
    
        for item in item_list: # loop through the shop keeper's item list
            
            self.buy_listbox.insert('end', item[0]) # add it to the list box

        try:
            
            self.current_buy.set(('Item:'+item_list[0][0]+'\nValue:'+item_database[item_list[0][0]].attributes.value+'\nAmount:'+item_list[0][1])) # get selected item's information (name,value,amount)

        except:

            self.current_buy.set("No items") # no item selected

        self.player_gold.set("Your Gold:"+str(Heroes['Player'].attributes['Gold'])) # set the player's gold
        self.shop_gold.set("Shop's Gold:"+str(Heroes[self.owner].attributes['Gold'])) # set the shop keeper's gold

        self.buy_listbox.bind('<ButtonRelease-1>', self.get_item_buy)

    def get_item_buy(self,event): # event is the mouse click

        try:
            
            index = self.buy_listbox.curselection()[0] # get position of item selected in listbox
            text = self.buy_listbox.get(index)  # get text of the item at that position
            stock = Heroes[self.owner].return_items()[index][1] # get the stock of that item from shop keeper's inventory
            self.current_buy.set((item_database[text].attributes.get_information()+'\nAmount:'+stock)) # runs the get_information function to get information exlusive to the item type

        except:

            pass

    def purchase(self,item,amount):
        
        try:

            if int(amount) >= 1 and int(amount)<=30: # is the amount between 1 and 30           

                for x in range(int(amount)): 

                    trade = Shops[self.owner].buy(item) # buy the item the amount of times

                    if trade == 'money': # not enough gold

                        self.buy_error_message.set("I lack the gold to buy that")

                    elif trade == 'notfound': # item not found (should not occur)

                        self.buy_error_message.set("The shop keeper has none of them")

                    else: # trade successful

                        self.buy_error_message.set("Nice trading with you")
                        
            else:

                self.buy_error_message.set("Amounts must be between\n 1 and 30")
                
        except:

            self.buy_error_message.set("Invalid amount")
            print("Invalid Entries") # an invalid character is within the amount box

        self.update_buy() # update the items in the listbox

    def sell(self):

        #SELL
        sell_name = Label(self.sell_menu,text=(self.owner+"'s"+' Shop'),font=self.font_title,bg='#84DE02',fg='black')
        sell_return = Button(self.sell_menu,text='Return',font=self.font_text,command=lambda:self.raise_main())
        sell_exchange = Button(self.sell_menu,text='Exchange',font=self.font_text,command=lambda:self.exchange(self.sell_listbox.get(ACTIVE),sell_spinbox.get()))
        sell_player_gold = Label(self.sell_menu,textvariable=self.player_gold,font=self.font_stat)
        sell_shop_gold = Label(self.sell_menu,textvariable=self.shop_gold,font=self.font_stat)
        sell_spinbox = Spinbox(self.sell_menu, from_=1, to=32,width=5)
        self.current_sell = StringVar()
        sell_current_item_stats = Label(self.sell_menu,textvariable=self.current_sell,font=self.font_stat)
        self.sell_error_message = StringVar()
        self.sell_error_message.set('What would you like to sell?')
        sell_errors = Label(self.sell_menu,textvariable=self.sell_error_message,font=self.font_error)
        
        sell_name.place(relx=0.5,rely=0.1,anchor=CENTER)
        sell_return.place(relx=0.1,rely=0.65)
        sell_exchange.place(relx=0.1,rely=0.85)
        sell_player_gold.place(relx=0.65,rely=0.45)
        sell_shop_gold.place(relx=0.65,rely=0.35)
        sell_spinbox.place(relx=0.7,rely=0.25)
        sell_current_item_stats.place(relx=0.45,rely=0.60)
        sell_errors.place(relx=0.52,rely=0.90)
        
        self.update_sell()

    def update_sell(self):
        
        self.sell_listbox = Listbox(self.sell_menu, width=20, height=6,font=self.font_option) # an empty listbox
        self.sell_listbox.place(relx=0.1,rely=0.25)
        item_list = Heroes['Player'].return_items() # list of the player's items

        for item in item_list: # loop through the player's item list
            
            self.sell_listbox.insert('end', item[0]) # add it to the list box

        try:
            
            self.current_sell.set(('Item:'+item_list[0][0]+'\nValue:'+item_database[item_list[0][0]].attributes.value+'\nAmount:'+item_list[0][1])) # get selected item's information (name,value,amount)

        except:
            
            self.current_sell.set("No items") # no item selected

        self.player_gold.set("Your Gold:"+str(Heroes['Player'].attributes['Gold'])) # set the player's gold
        self.shop_gold.set("Shop's Gold:"+str(Heroes[self.owner].attributes['Gold'])) # set the shop keeper's gold

        self.sell_listbox.bind('<ButtonRelease-1>', self.get_item_sell)

    def get_item_sell(self,event): # event is the mouse click

        try:
            
            index = self.sell_listbox.curselection()[0] # get position of item selected in listbox
            text = self.sell_listbox.get(index)  # get text of the item at that position
            stock = Heroes['Player'].return_items()[index][1] # get the stock of that item from player's inventory
            self.current_sell.set((item_database[text].attributes.get_information()+'\nAmount:'+stock)) # runs the get_information function to get information exlusive to the item type

        except:

            pass

    def exchange(self,item,amount):
        
        try:

            if int(amount) >= 1 and int(amount)<=30: # is the amount between 1 and 30           

                for x in range(int(amount)): 

                    trade = Shops[self.owner].sell(item) # sell the item the amount of times

                    if trade == 'money': # not enough gold

                        self.sell_error_message.set("The shop keeper lacks the\n gold to buy that")

                    elif trade == 'notfound': # item not found (should not occur)

                        self.sell_error_message.set("You have none of them")

                    elif trade == 'equipped': # item is equipped

                        self.sell_error_message.set("You cannot sell\nequipped items")
                    
                    else: # trade successful

                        self.sell_error_message.set("Nice trading with you")
                        
            else:

                self.sell_error_message.set("Amounts must be between\n 1 and 30")
                
        except:

            self.sell_error_message.set("Invalid amount")
            print("Invalid Entries") # an invalid character is within the amount box

        self.update_sell() # update the items in the listbox

    def raise_main(self):

        self.main_menu.tkraise() # raise menu frame to the top layer

    def raise_sell(self):
        
        self.update_sell() # update the sell menu
        self.sell_menu.tkraise() # raise the sell frame to the top layer

    def raise_buy(self):
                
        self.update_buy()  # update the buy menu
        self.buy_menu.tkraise() # raise buy frame to top layer 

    def exit_shop(self):

        Heroes[self.owner].save_data() # save the owner's new inventory
        Heroes['Player'].save_data() # save the player's new inventory

        self.destroy() # destroy the tkinter window
        
def startup_shop(): 

    app = GUI('Bob') # create a tkinter object
    mainloop() # run and update the tkinter object

#startup_shop() run the shop
