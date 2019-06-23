import random # allows access to the random library


class Move: # This will create a move object containing the move's information

    def __init__(self,name,damage,accuracy):

        self.name = name # contains the moves stats
        self.damage = damage
        self.accuracy = accuracy
        

class Entity: # This will create a super class. It will be used by AI controlled enemies, and the player class will inherit it.

    def __init__(self,name, health, strength, speed):
        
        self.name = name # contains the entity's stats
        self.health = health
        self.strength = strength
        self.speed = speed 

        self.move_list = [attack_a,attack_b,attack_c] # a list of possible moves the entity can use
        
    def get_move(self): # called when the battle requires the user's move
        
        self.move = self.move_list[random.randint(0,len(self.move_list)-1)] # selects a move at random out of its move list

    def attack(self,hurt): # called when the entity needs to attack

        damage = self.strength + self.move.damage # contains the damage the attack will deal (this will change later in development)
        hurt.health -= damage # applies the damage to the other entity

        if (hurt.health <= 0): # checks if the other entity has died

            return True # return out if the other entity is dead

    def display_stats(self):

        print(self.name+"'s stats:")
        print("  * Health:",self.health)
        print("  * Strength:",self.strength)
        print("  * Speed:",self.speed)
        print("")
         
class Player(Entity): # this sub class inherits the Entity class to gain all of its functionality 

    def __init__(self,name, health, strength, speed):

        Entity.__init__(self,name, health, strength, speed) # this runs the Entity's __init__ function

    def get_move(self): # overwrites the Entity's get_move function, replacing it with its own

        while True: # keep asking for the player's move if the move does not exist
        
            for x in range(len(self.move_list)): # loop through their move list

                print(str(x+1)+') '+str(self.move_list[x].name)) # display the key and value of their move. 1) Punch 2) Slice. ect
                
            position = int(input(("\nEnter a number between 1-"+str(len(self.move_list))+": "))) # asks the user for the key of the move they want

            if (position-1 >= 0 and position-1 <= len(self.move_list)-1): # checks that the move does exist

                break # exit the loop
                
        self.move = self.move_list[(position - 1)] # contains the move object (the value associated with the key they entered)
        
    
class Battle: # The actual battle class - the battle will occur within an instance of this

    def __init__(self,player,attacker):

        self.player = player # allows access throughout the class to the player
        self.attacker = attacker # allows access throughout the class to the attacker

        self.fighters = [player,attacker] # a list containing the fighters (used to order who moves first)

        self.player.display_stats()
        self.attacker.display_stats()
        
        self.battle_loop() # begin the battle loop

    def battle_loop(self): 

        while True: # loop through until the player/attacker is defeated

            self.player.get_move() # get the player's move
            self.attacker.get_move() # get the attacker's move

            move_first = self.check_speed() # calculate who moves first
            move_second = self.fighters[(self.fighters.index(move_first)+1) % 2] # get the person who moves second

            if (move_first.attack(move_second)): # apply damage to the slower entity

                print('\n'+move_first.name,"is the winner! Surviving by",move_first.health,"HP")
                break # exit loop if the slower entity has died

            if (move_second.attack(move_first)): # apply damage to the faster entity

                print('\n'+move_second.name,"is the winner! Surviving by",move_second.health,"HP")
                break # exit loop if the faster entity has died

            print(move_first.name,move_first.health)
            print(move_second.name,move_second.health)
            print("")
            
    def check_speed(self):

        if (self.player.speed >= self.attacker.speed): # compare the speeds of the entities

            return self.player # return the player if the player is the faster entity

        return self.attacker # return the attacker if the attacker is the faster entity


attack_a = Move('Punch',50,90) # creates the move objects (will be updated later in development with the information from the database) 
attack_b = Move('Kick',70,50)
attack_c = Move('Slap',20,100)

player = Player('Player',60,30,50) # creates a player object
attacker = Entity('Joe',95,10,60) # creates an entity object 

Battle(player,attacker) # creates a battle between the player and attacker
