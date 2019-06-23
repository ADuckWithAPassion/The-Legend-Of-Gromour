from IntroScreen import *

class Hero: # hero class - this will control character's inventories

    def __init__(self,hero):

        self.hero = hero # allows access to the hero varaible throughout the object

    def load_data(self):

        self.attributes = {} # defines an empty dictionary to store its stats
        self.item_list = [] # defines an empty list to store its items

        for entry in self.hero: # loop through every attribute in the hero

            self.attributes[entry.tag] = entry.text # assign it to a dictionary so that it can be accessed later

        self.inv = Inventory(self.hero.tag)
        
    def display_stats(self):

        for stat in self.attributes: # loop through the hero's attributes

            print(stat,''+self.attributes[stat]) # display their stats

    def save_data(self):

        for entry in self.hero: # loops through every stat in the hero object

            entry.text = str(self.attributes[entry.tag]) # overwrites the object's old stats with its current stats 

        self.inv.save_inventory()

        player_database.write('Player_database.xml') # saves the new object back on to the database
            
    def return_items(self):
        
        item_list = [] # define an empty list to contain their items

        for item in self.inv.item: # loop through their inventory
            
            item_list.append(item) # add every item to their item list

        return item_list # return the list of their items

    def return_battle_items(self):

        item_list = [] # define an empty list to contain their battle items

        for item in self.inv.item: # loop through the Entity's inventory

            if item_database[item[0]].type == 'Potion': # filter out non usable items

                item_list.append(item) # add every item of Potion type to their item list

        return item_list # return the list of their battle items

    def remove(self):

        player_data.remove(self.hero) # uses element tree's remove function to delete the hero from our database
        del self # removes our self from memory, goodbye :(
        
class ItemDatabase: # item database class - this will create a list of template item objects for every item in the items database

    def __new__(self,items_data):

        self.item_list = {} # creates an empty item_list dictionary which can be accessed outside the object through calling item_database.item_list

        for item in items_data: # loop through every item that exists within items_data 

            self.item_list[item.tag] = Item(item) # create an item blueprint of it

        return self.item_list # returns the object containing every item's information to the main body


class Item: # item class - this will create an object of an item

    def __init__(self,item):

        self.type = item.attrib['type'] # contains the type of the item (Weapon/Bow/Arrow/Breastplate)

        if self.type == 'Weapon':

            self.attributes = Weapon(item) # create a weapon
 
        elif self.type == 'Bow':

            self.attributes = Bow(item) # create a bow

        elif self.type == 'Arrow':

            self.attributes = Arrow(item) # create an arrow

        elif self.type == 'Breastplate':

            self.attributes = Breastplate(item) # create a breastplate       

        elif self.type == 'Potion':

            self.attributes = Potion(item)
            

class Weapon: # weapon blueprint
    
    def __init__(self,item):
        
        self.name = item.tag # the weapon's attributes
        self.damage = item[0].text
        self.speed = item[1].text
        self.value = item[2].text
        self.armour = 0
        self.weight = 0

    def display_stats(self):
        
        print(self.name) # display its attributes
        print('* Damage:',self.damage)
        print('* Speed:',self.speed)
        print('* Value:',self.value)

    def get_information(self):

        return ('Item:'+self.name+'\nDamage:'+self.damage+'\nSpeed:'+self.speed+'\nValue:'+self.value)

    def equip(self,item):

        if Heroes['Player'].attributes['Weapon'] == 'Empty': # check if the player does not have an equipped weapon
            
            Heroes['Player'].attributes['Weapon'] = item # set the player's equipped weapon to the selected weapon
            
        else:
            
            print("unequip current item first")
        
    def unequip(self,item):

        Heroes['Player'].attributes['Weapon'] = 'Empty' # clear the player's equipped weapon

        
class Bow: # bow blueprint
    
    def __init__(self,item):
        
        self.name = item.tag # the bows's attributes
        self.damage = item[0].text
        self.range = item[1].text
        self.value = item[2].text
        self.armour = 0
        self.weight = 0

    def display_stats(self):
        
        print(self.name)
        print('* Damage:',self.damage) # display its attributes
        print('* Range:',self.range)
        print('* Value:',self.value)

    def get_information(self):

        return ('Item:'+self.name+'\nDamage:'+self.damage+'\nRange:'+self.range+'\nValue:'+self.value)
        
    def equip(self,item):

        if Heroes['Player'].attributes['Bow'] == 'Empty':
            
            Heroes['Player'].attributes['Bow'] = item
            
        else:
            
            print("unequip current item first")
        
    def unequip(self,item):

        Heroes['Player'].attributes['Bow'] = 'Empty'


class Arrow: # arrow blueprint
    
    def __init__(self,item):
        
        self.name = item.tag # the arrows's attributes
        self.damage = item[0].text
        self.value = item[1].text

    def display_stats(self):
        
        print(self.name)
        print('* Damage:',self.damage) # display its attributes
        print('* Value:',self.value)

    def get_information(self):

        return ('Item:'+self.name+'\nDamage:'+self.damage+'\nValue:'+self.value)

    def equip(self,item):

        if Heroes['Player'].attributes['Arrow'] == 'Empty':
            
            Heroes['Player'].attributes['Arrow'] = item
            
        else:
            
            print("unequip current item first")
        
    def unequip(self,item):

        Heroes['Player'].attributes['Arrow'] = 'Empty'


class Breastplate: # breastplate blueprint

    def __init__(self,item):
        
        self.name = item.tag # the breastplate's attributes
        self.armour = item[0].text
        self.weight = item[1].text
        self.value = item[2].text
        self.damage = 0
        self.speed = 0
        
    def display_stats(self):
        
        print(self.name)
        print('* Armour:',self.armour) # display its attributes
        print('* Weight:',self.weight)
        print('* Value:',self.value)

    def get_information(self):

        return ('Item:'+self.name+'\nArmour:'+self.armour+'\nWeight:'+self.weight+'\nValue:'+self.value)

    def equip(self,item):

        if Heroes['Player'].attributes['Breastplate'] == 'Empty':
            
            Heroes['Player'].attributes['Breastplate'] = item
            
        else:
            
            print("unequip current item first")
        
    def unequip(self,item):

        Heroes['Player'].attributes['Breastplate'] = 'Empty'


class Potion: # potion blueprint

    def __init__(self,item):

        effects = {'Heal':self.heal}
        
        self.name = item.tag # the potion's attributes
        self.effect_name = item[0].attrib['effect']
        self.effect = effects[self.effect_name]
        self.potency = item[0].text
        self.value = item[1].text
        
    def heal(self,player,attacker,gui):
        Heroes['Player'].inv.remove_item(self.name)
        player.health += int(self.potency)
        player.attack_text = 'Player used a Potion to heal for '+str(self.potency)

        if player.health > int(Heroes[player.name].attributes['MaxHealth']):

            player.health = int(Heroes[player.name].attributes['MaxHealth'])
            player.attack_text = 'Player used a Potion to heal to full health'
        
    def get_information(self):

        return ('Item:'+self.name+'\nEffect:'+self.effect_name+'\nPotency:'+self.potency+'\nValue:'+self.value)

    def get_stats(self,battle):

        player = battle.player
        attacker = battle.attacker
        
        if self.effect_name == 'Heal':
            
            return ('Player Health: '+str(player.health))

        else:

            print(self.effect_name)

    def equip(self,item):

        pass

    def unequip(self,item):

        pass
    
        
class Inventory: # allows the creation of an inventory for any hero
    
    def __init__(self,hero):
        
        self.hero = hero # allows access throughout the class of the hero's name
        self.item = [] # creates an empty list to contain the hero's items
        
        self.load_inventory()
        
    def load_inventory(self): # load the entity's inventory from the inventory database, then create an object of it
        
        for item in inventory_data.find(self.hero): # find the hero inside the inventory_database and loop through inside it
            
            self.item.append([item.tag,item.text]) # append every item inside the hero's inventory to self.item - a list
            
    def save_inventory(self): # save the entity's inventory to the database
        
        inventory_data.find(self.hero).clear() # find and clear the hero's inventory from the inventory_data
        
        for item in self.item: # loop through for every item the hero current has as a temporary item
            
            ET.SubElement(inventory_data.find(self.hero), item[0]).text = item[1] # add it to the inventory_data, under the hero's name

        inventory_database.write(open('UpdatedItems.xml', 'w'), encoding='unicode') # save the changes just made to the inventory_database

    def add_item(self,new_item,amount): # add an item to the entity's inventory (item_list)

        amount = int(amount) # fix floats

        if amount <= 0: # don't allow negative amounts

            return True # exit out 
        
        for item in self.item: # loop through the entity's item_list variable

            if item[0] == new_item: # check if the item name already exists in their item_list

                item[1] = str(int(item[1]) + amount) # add the new amount of the item to their old amount of the item

                return True # exit out of the function

        self.item.append([new_item,str(amount)]) # if the item does not exist, then add an entry of it within the item_list

    def remove_item(self,old_item): # remove an item from an entity's inventory (item_list)

        for item in self.item: # loop through the entity's item list

            if item[0] == old_item: # if the item is inside of their inventory
                
                item[1] = str(int(item[1]) - 1) # remove one of it from their inventory

            if item[1] == '0': # if the amount of item equals 0

                self.item.remove(item) # then remove it using python's list remove method

class Shop: # Creates a shop object that will interact with the database and allow trading through the shop GUI

    def __init__(self,owner):

        self.owner = owner # The name of the shop owner (must exist within the databases)

    def display_stock(self): # Displays the shop owner's inventory to the console

        weapon_list = [] # an empty list to contain every weapon in the shopkeeper's inventory
        bow_list = [] # an empty list to contain every bow in the shopkeeper's inventory
        arrow_list = [] # an empty list to contain every arrow in the shopkeeper's inventory
        breastplate_list = [] # an empty list to contain every breastplate in the shopkeeper's inventory

        for item in Heroes[self.owner].inv.item: # loops through the shop keeper's inventory

            if item_database[item[0]].type == 'Weapon': # if the item's type is weapon

                weapon_list.append(item) # add it weapon_list

            elif item_database[item[0]].type == 'Bow': # if the item's type is bow

                bow_list.append(item) # add it bow_list

            elif item_database[item[0]].type == 'Arrow': # if the item's type is arrow

                arrow_list.append(item) # add it arrow_list

            elif item_database[item[0]].type == 'Breastplate': # if the item's type is breastplate

                breastplate_list.append(item) # add it breastplate_list

        item_list = weapon_list + bow_list + arrow_list + breastplate_list # concatenate all of the lists together in order of their type

        for item in item_list: # loop through every item in their inventory
 
            item_database[item[0]].attributes.display_stats() # run the items's display_stats() method
            print('* Stock:',item[1]) # display the stock of the item

    def buy(self,item): # Purchase an item from the shopkeeper

        for goods in Heroes[self.owner].inv.item: # looks through the shop keeper's inventory
            
            if item == goods[0]: # check to see if the item matches what they are looking for

                if int(Heroes['Player'].attributes['Gold']) >= int(item_database[item].attributes.value): # if the player can afford the item

                    Heroes['Player'].attributes['Gold'] = str(int(Heroes['Player'].attributes['Gold']) - int(item_database[item].attributes.value)) # take the cost of the item from the player's gold
                    Heroes[self.owner].attributes['Gold'] = str(int(Heroes[self.owner].attributes['Gold']) + int(item_database[item].attributes.value)) # add the cost of the item to the shopkeeper's gold
                    Heroes[self.owner].inv.remove_item(item) # remove the item from the shop keeper's inventory
                    Heroes['Player'].inv.add_item(item,1) # add 1 of the item to the player's inventory

                    print("You purchased",item,"for",item_database[item].attributes.value,"gold") # notification confirming the transaction

                    return True # return out - the item has been bought!

                else: # if they cannot afford the item

                    print("Sorry, you don't have enough gold") # notification rejecting the transaction

                    return 'money'# return out - the item has not been bought!

        print("Sorry, I don't have them!") # notification rejecting the transaction
        return 'notfound'
    
    def sell(self,item): # Sell an item to the shopkeeper
        
        for goods in Heroes['Player'].inv.item: # loop through the player's inventory

            if item == goods[0]: # if the item is what we are searching for

                item_type = item_database[item].type # get the type of item (weapon/bow/ect)
                
                if Heroes['Player'].attributes[item_type] == item: # if the player's currently equipped item matches the item being sold

                    print("Cannot sell equipped\nitems")
                    return 'equipped' # exit out of the function

                if int(Heroes[self.owner].attributes['Gold']) >= int(item_database[item].attributes.value): # check if the shop keeper can afford it
                    
                    Heroes[self.owner].attributes['Gold'] = str(int(Heroes[self.owner].attributes['Gold']) - int(item_database[item].attributes.value)) # take away the cost of the item from the shopkeeper's gold
                    Heroes['Player'].attributes['Gold'] = str(int(Heroes['Player'].attributes['Gold']) + int(item_database[item].attributes.value)) # add the cost of the item to the player's gold
                    Heroes['Player'].inv.remove_item(item) # remove the item from the player
                    Heroes[self.owner].inv.add_item(item,1) # add 1 of the item to the shopkeeper

                    print("You exchanged",item,"for",item_database[item].attributes.value,"gold") # transaction passed
                    return True # exit out of the function

                else: # if the shop keeper can not afford it
                    
                    print("Sorry, I don't have enough gold") # transaction failed
                    return 'money'# exit out of the function
                
        print("Sorry, you don't have them!") # item not found, so transaction failed
        return 'notfound'


Heroes = {} #an empty dictionary where characters will be stored
Shops = {}

item_database = ItemDatabase(items_data) # store every item's information in item_database

for hero in player_data: # loop through every hero in the database

    Heroes[hero.tag] = Hero(hero) # create an object of the hero
    Heroes[hero.tag].load_data() # load in the hero object

Shops['Bob'] = Shop('Bob')
Shops['EndGameShop'] = Shop('EndGameShop')


            
