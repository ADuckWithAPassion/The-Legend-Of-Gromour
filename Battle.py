import random # allows access to the random library
from BattleGUI import *


class Move: # This will create a move object containing the move's information

    def __init__(self,name,damage,accuracy):

        self.name = name # contains the moves stats
        self.damage = damage
        self.accuracy = accuracy
        

class Participant: # This will create a super class. It will be used by AI controlled enemies, and the player class will inherit it.

    def __init__(self,name):
        
        self.name = name # contains the entity's stats
        self.health = int(Heroes[self.name].attributes['Health'])
        self.strength = int(Heroes[self.name].attributes['Strength'])
        self.speed = int(Heroes[self.name].attributes['Speed'])
        self.gold = int(Heroes[self.name].attributes['Gold'])
        self.xp = int(Heroes[self.name].attributes['XP'])
        self.max_health = int(Heroes[self.name].attributes['MaxHealth'])
        self.attack_text = ""
        self.weapon_damage = int(item_database[Heroes[self.name].attributes['Weapon']].attributes.damage)
        self.weapon_speed = int(item_database[Heroes[self.name].attributes['Weapon']].attributes.speed)
        self.breastplate_armour = int(item_database[Heroes[self.name].attributes['Breastplate']].attributes.armour)
        self.breastplate_weight = int(item_database[Heroes[self.name].attributes['Breastplate']].attributes.weight)
        
        self.move_list = [attack_a,attack_b,attack_c] # a list of possible moves the entity can use
        
    def get_move(self): # called when the battle requires the user's move
        
        self.move = self.move_list[random.randint(0,len(self.move_list)-1)] # selects a move at random out of its move list

    def attack(self,hurt): # called when the entity needs to attack

        if self.move.accuracy >= random.randint(1,100): # if the player lands their attack
            
            damage = self.strength + self.move.damage + self.weapon_damage # contains the damage the attack will deal 
            hurt.health -= damage * 1/hurt.breastplate_armour # applies the damage to the other entity

            self.attack_text = self.name+" used "+self.move.name+" dealing "+str(damage*1/hurt.breastplate_armour)+" damage!"

        else: # if the player misses their attack

            self.attack_text = self.name+" used "+self.move.name+"... But they missed!"

        if (hurt.health <= 0): # checks if the other entity has died

            return True # return out if the other entity is dead

    def display_stats(self):

        print(self.name+"'s stats:")
        print("  * Health:",self.health)
        print("  * Strength:",self.strength)
        print("  * Speed:",self.speed)
        print("")
         
class Person(Participant): # this sub class inherits the Entity class to gain all of its functionality 

    def __init__(self,name):

        Participant.__init__(self,name) # this runs the Entity's __init__ function

    def get_move(self,position): # overwrites the Entity's get_move function, replacing it with its own

        self.move = self.move_list[(position)] # contains the move object (the value associated with the key they entered)
        
    
class Fight: # The actual battle class - the battle will occur within an instance of this

    def __init__(self,player,attacker,player_sprite,attacker_sprite):

        self.player = player # allows access throughout the class to the player
        self.attacker = attacker # allows access throughout the class to the attacker

        self.player_sprite = player_sprite
        self.attacker_sprite = attacker_sprite
        
        self.fighters = [player,attacker] # a list containing the fighters (used to order who moves first)

        self.player.display_stats()
        self.attacker.display_stats()

        self.ended = False

        startup_battle(self) # load the battle GUI and give it reference to this object 

    def battle_loop(self,player_move_position,battle_gui,item_used=False): 

        self.battle_gui = battle_gui # gives my Logic access to my GUI

        if not item_used:

            self.player.get_move(player_move_position) # get the player's move
            self.attacker.get_move() # get the attacker's move

            move_first = self.check_speed() # calculate who moves first
            move_second = self.fighters[(self.fighters.index(move_first)+1) % 2] # get the person who moves second

            if (move_first.attack(move_second)): # apply damage to the slower entity
                 
                self.match_finished(move_first,move_second) # match has ended - faster entity has won

            if (move_second.attack(move_first)): # apply damage to the faster entity

                self.match_finished(move_second,move_first) # match has ended - slower entity has won
                
            print(move_first.name,move_first.health,move_first.move.name)
            print(move_second.name,move_second.health,move_second.move.name)
            print("")

        else:

            self.attacker.get_move() # get the attacker's move
            self.attacker.attack(self.player)
            print(self.attacker.move.name)
            
    def check_speed(self):

        if ((self.player.speed+self.player.weapon_speed-self.player.breastplate_weight)*random.randint(5,15)/10 >= self.attacker.speed+self.attacker.weapon_speed-self.attacker.breastplate_weight): # compare the speeds of the entities

            return self.player # return the player if the player is the faster entity

        return self.attacker # return the attacker if the attacker is the faster entity

    def match_finished(self,winner,loser):

        self.battle_gui.destroy() # close Tkinter window

        print("WINNER:",winner.name,"BY",winner.health,"HP") 
        print("LOSER:",loser.name)

        if winner == self.player: # if the player won

            self.player_sprite.victory(self.player,self.attacker) # player's victory
            self.attacker_sprite.death(self.attacker) # attacker's death

        else: # if attacker won

            #self.attacker_sprite.victory()
            self.player_sprite.death(self.player) # player's death
            
        self.ended = True # set my ended flag to true so my GUI knows to close
        
attack_a = Move('Punch',50,90) # creates the move objects (will be updated later in development with the information from the database) 
attack_b = Move('Kick',70,50)
attack_c = Move('Slap',20,100)
