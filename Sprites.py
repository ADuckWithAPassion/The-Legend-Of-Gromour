# Contains classes for my entities
from Battle import *


class Entity(pygame.sprite.Sprite): # inherit from pygame's sprites

    def __init__(self,x,y,w,h,game):

        pygame.sprite.Sprite.__init__(self) # run pygame's sprites __init__

        self.pos = vector(int(x),int(y)) # a vector containing the sprite's x and y 
        self.w = int(w) 
        self.h = int(h)
        self.game = game # a copy (by reference) of main

        self.game.entities_group.add(self) # adds this sprite to the entities_group in main

    def draw(self,screen):

        pass
    
class Character(Entity):

    def __init__(self,x,y,w,h,game,name):

        Entity.__init__(self,x,y,w,h,game)

        self.name = name
        self.speed = PLAYER_SPEED / 2
        self.sprite = pygame.Surface((self.w,self.h)) # create a surface with dimensions 10 x 10
        #self.sprite.fill(BLUE) # fill the surface green (R,G,B) (0,255,0)
        self.vel = vector(0,0) # create a velocity vector with x=0,y=0 initially stored
        self.direction = 0 # default direction is facing up
        self.distance = 0 # default distance to move on spawn is 0 
        self.counter = 0
        self.ID = 'Enemy'
        self.sprite = entityList[1][self.ID].animationList[0]
        self.selected_stack = [] # a stack to contain two position vectors
        self.devbarrier_stack = [] # a stack to contain all of the devbarriers (temporary barriers for testing)
        self.coordinates_stack = [] # a stack to contain all of the devbarrier's information - can be copy pasted directly into barriers file to save it (press enter in game to view) 

        self.game.character_group.add(self) # adds this sprite to the character_group in main
        self.game.blitable_group.add(self) # adds this sprite to the blitable_group in main
        
    def update(self):

        self.vel.x,self.vel.y = (0,0) # clear any previous velocity

        if self.distance == 0: # if you have moved in a certain direction for too long

            if random.randint(0,200) == 0: # check for a random number between 0 - 100

                self.direction = random.randint(0,3) # select a random direction (up,down,left,right)
                self.distance = random.randint(20,40) # select a random distance 0-20
                
        elif self.distance >= 1: # if you have not walked in the direction for long enough
            
            [self.move_down,self.move_up,self.move_left,self.move_right][self.direction]() # move in the direction you are facing
            self.distance -= 1 # subtract from the distance

        self.pos += self.vel # update their position

        if self.collision_detection(self.pos.x,self.pos.y,self.w,self.h): # check for collision

            self.pos -= self.vel # update their position

        self.animate() # animate the character
        
    def animate(self):

        self.counter += 1 # increase counter by 1
        
        if self.vel.x != 0 or self.vel.y != 0: # insure that the character is moving

            # update the sprite depending on how far in to their walking animation they are
                
            if self.counter % 50 >= 25: 

                self.sprite = entityList[self.direction][self.ID].animationList[2]

            elif self.counter % 50 >= 0:

                self.sprite = entityList[self.direction][self.ID].animationList[1]

            else:

                self.sprite = entityList[self.direction][self.ID].animationList[0]
        
        else:

            self.counter = 0 # reset the counter; they are standing still
            self.sprite = entityList[self.direction][self.ID].animationList[0] # default standing sprite
        
    def move_up(self):
        
        self.vel.y = - self.game.dt * self.speed # prevents higher fps resulting in faster movement
        self.vel.x = 0
        self.direction = 1
        
    def move_down(self):

        self.vel.y = self.game.dt * self.speed # prevents higher fps resulting in faster movement
        self.vel.x = 0
        self.direction = 0

    def move_left(self):

        self.vel.y = 0
        self.vel.x = - self.game.dt * self.speed # prevents higher fps resulting in faster movement
        self.direction = 2

    def move_right(self):

        self.vel.y = 0
        self.vel.x = self.game.dt * self.speed # prevents higher fps resulting in faster movement
        self.direction = 3

    def collision_detection(self,x,y,w,h,mouse=False):

        if mouse:

            x = x - self.game.player.offset.x 
            y = y - self.game.player.offset.y
            
        for barrier in self.game.collide_group: # look through all barriers within my collide_group

            if barrier == self:

                continue # if the barrier is the entity performing the check, ignore it and continue
            
            if (x < barrier.pos.x + barrier.w and # check if barrier's right side is on the right of the player's left side
                x + w > barrier.pos.x and # check if the player's right side is on the right of the barrier's left side
                # if both are true, then the player and barrier are colliding in the x dimension
                y < barrier.pos.y + barrier.h and # cehck if barrier's bottom side is on the bottom of the player's top side
                y + h > barrier.pos.y): # check if the player's bottom side is on the bottom of the barrier's top side
                # if both are true, then the player and barrier are colliding in the y dimension
                # if all four are true, then the player and barrier are colliding in the x and y dimension. A collision has occured. 

                if barrier.__class__.__name__ == 'SPAWNBarrier':

                    if self.__class__.__name__ == 'SpawnableEnemy':
                        
                        return False
                
                if self.__class__.__name__ != 'Player': # if this is not a player, exit out

                    return True
                
                if barrier.__class__.__name__ == 'ShopKeeper': # if the player walks into a shop keeper

                    startup_shop() # open the shop GUI

                if barrier.__class__.__name__ == 'Michael': # if the player walks into Michael

                    if Heroes['Player'].attributes['ReceivedGold'] == 'False':

                        Heroes['Player'].attributes['Gold'] = str(int(Heroes['Player'].attributes['Gold']) + 300)
                        self.game.chatbox.set_text("Here you go! Spend this 300 gold wisely on your adventure!")
                        Heroes['Player'].attributes['ReceivedGold'] = 'True'
                        time.sleep(0.5)
                        
                    else:

                        self.game.chatbox.set_text("Sorry, I have no more gold to spare!")

                if barrier.__class__.__name__ == 'Harry': # if the player walks into Harry

                    if Heroes['Player'].attributes['ReceivedPotion'] == 'False':

                        Heroes['Player'].inv.add_item('Medium_Health_Potion',1)
                        Heroes['Player'].attributes['ReceivedPotion'] = 'True'
                        self.game.chatbox.set_text("Here, have a potion!")
                        time.sleep(0.5)
                        
                    else:

                        self.game.chatbox.set_text("That was the last of my potions, sorry!")

                if barrier.__class__.__name__ == 'TELEPORTTOSHOPBarrier': # if the player walked onto a teleport to shop barrier

                    self.vel.x = self.pos.x - 2220 # adjust the player's velocity to place them in the shop 
                    self.vel.y = self.pos.y - 2663

                    return True

                if barrier.__class__.__name__ == 'TELEPORTOUTSHOPBarrier': # if the player walked onto a teleport to shop barrier

                    self.vel.x = self.pos.x - 1787 # adjust the player's velocity to place them in the shop 
                    self.vel.y = self.pos.y - 842

                    return True

                if barrier.__class__.__name__ == 'DOORABarrier':

                    if Heroes['Player'].attributes['DoorA'] == 'Unlocked':

                        return False

                    else:

                        self.game.chatbox.set_text("The door is locked - maybe the guy in the first area will sell me the key for 200 gold?")

                if barrier.__class__.__name__ == 'DOORBBarrier':

                    if Heroes['Player'].attributes['DoorB'] == 'Unlocked':

                        return False

                    else:

                        self.game.chatbox.set_text("The door is locked - maybe the guy in the second area will sell me the key for 800 gold?")

                if barrier.__class__.__name__ == 'TK': # if the player walks into TK

                    if int(Heroes['Player'].attributes['Gold']) >= 1000: # check if the player has enough gold
                        self.game.player.game_over() # end the game

                    else:

                        self.game.chatbox.set_text("Earn 1000 gold, then we may speak!")

                if barrier.__class__.__name__ == 'KeyDealerA': # if the player walks into KeySellerA

                    if Heroes['Player'].attributes['DoorA'] == 'Unlocked':

                        self.game.chatbox.set_text("Enjoy ya key!")
                        return True
                    
                    if int(Heroes['Player'].attributes['Gold']) >= 200:

                        Heroes['Player'].attributes['DoorA'] = 'Unlocked'
                        Heroes['Player'].attributes['Gold'] = str(int(Heroes['Player'].attributes['Gold']) - 200)

                        self.game.chatbox.set_text("Enjoy ya key!")

                    else:

                        self.game.chatbox.set_text("SELLING KEYS - 200 PER YA KEY!")

                    return True

                if barrier.__class__.__name__ == 'KeyDealerB': # if the player walks into KeySellerB

                    if Heroes['Player'].attributes['DoorB'] == 'Unlocked':

                        self.game.chatbox.set_text("Enjoy ya key!")
                        return True
                    
                    if int(Heroes['Player'].attributes['Gold']) >= 800:

                        Heroes['Player'].attributes['DoorB'] = 'Unlocked'
                        Heroes['Player'].attributes['Gold'] = str(int(Heroes['Player'].attributes['Gold']) - 800)

                        self.game.chatbox.set_text("Enjoy ya key!")

                    else:

                        self.game.chatbox.set_text("SELLING KEYS - 800 PER YA KEY!")

                    return True

                if barrier.__class__.__name__ == 'Friend':

                    self.game.difficulty = (self.game.difficulty + 1) % int(barrier.level)
                    self.game.chatbox.set_text("The game's difficulty is now "+str(self.game.difficulty))

                    for enemy in self.game.character_group.sprites():

                        if enemy.__class__.__name__ == 'SpawnableEnemy':

                            enemy.death(None)    
                    
                    time.sleep(0.5)

                if barrier.__class__.__name__ == 'INNBarrier':

                    if self.rested >= pygame.time.get_ticks():

                        return True
                    
                    if int(Heroes['Player'].attributes['Gold']) >= 100:

                        Heroes['Player'].attributes['Gold'] = str(int(Heroes['Player'].attributes['Gold']) - 100)
                        Heroes['Player'].attributes['Health'] = Heroes['Player'].attributes['MaxHealth']
                        self.game.chatbox.set_text("You feel well rested")
                        self.rested = pygame.time.get_ticks() + 2 * 1000

                    else:
                        self.game.chatbox.set_text("You lack the 100 gold")

                if barrier.__class__.__name__ == 'NOCHARACTERBarrier':

                    return False

                if barrier.__class__.__name__ == 'Enemy' or barrier.__class__.__name__ == 'SpawnableEnemy':

                    player = Person(self.name) # creates a player object
                    attacker = Participant(barrier.name) # creates an attacker object

                    Fight(player,attacker,self,barrier) # creates a battle between the player and attacker
                
                if mouse == True:

                    print(barrier.__class__.__name__+'('+str(barrier.pos.x)+','+str(barrier.pos.y)+','+str(barrier.w)+','+str(barrier.h)+',game)')

                return True # collision detected

    def death(self,player):

        self.game.blitable_group.remove(self) # removes this sprite from the blitable_group in main
        self.game.character_group.remove(self) # removes this sprite from the character_group in main
        self.game.entities_group.remove(self) # removes this sprite from the entities_group in main
        self.game.collide_group.remove(self) # removes this sprite from the collide_group in main
        self.timer = pygame.time.get_ticks() + self.spawn_delay * 1000 # update the respawn timer
        self.game.respawning.append(self) # add them to the respawning list
        
        if player:
    
            Heroes['Player'].attributes['MaxHealth'] = str(int(Heroes['Player'].attributes['MaxHealth'])+int(Heroes[self.name].attributes['XP']))
            Heroes['Player'].attributes['Health'] = str(int(Heroes['Player'].attributes['Health'])+int(Heroes[self.name].attributes['XP']))
            Heroes['Player'].attributes['Strength'] = str(int(Heroes['Player'].attributes['Strength'])+int(Heroes[self.name].attributes['XP']))
            Heroes['Player'].attributes['Speed'] = str(int(Heroes['Player'].attributes['Speed'])+int(Heroes[self.name].attributes['XP']))
            
    def draw(self,screen):

        screen.blit(self.sprite, (self.pos + self.game.player.offset)) # blit the entity's sprite at his position.


class Player(Character):

    def __init__(self,x,y,w,h,game,name):
        
        Character.__init__(self,x,y,w,h,game,name) # inherit from the character class

        self.offset = vector(SCREEN_WIDTH/2 - PLAYER_WIDTH/2 - self.pos.x, SCREEN_HEIGHT/2 - PLAYER_HEIGHT/2 - self.pos.y) # transform everything by this to put the player in the center of the screen
        self.ID = 'Player'
        self.rested = pygame.time.get_ticks() + 2 * 1000
        self.speed = PLAYER_SPEED
        #self.sprite.fill(GREEN)
        self.sprite = entityList[0]['Player'].animationList[1]

    def update(self):

        self.vel.x,self.vel.y = (0,0) # wipe the previous value stored in their velocity

        for event in pygame.event.get(): # loop through all stored events in pygames queued events list

            if event.type == pygame.QUIT: # check the event type

                self.game.leave() # run main game's leave function (save and quits game)

            if event.type == pygame.KEYDOWN: # check if a key has been pressed

                if event.key == pygame.K_w: # if user pressed w

                    self.move_up()

                elif event.key == pygame.K_a: # if user pressed a

                    self.move_left()

                elif event.key == pygame.K_s: # if user pressed s

                    self.move_down()

                elif event.key == pygame.K_d: # if user pressed d

                    self.move_right()

                elif event.key == pygame.K_e: # if user pressed e

                    self.game.chatbox.set_text('')

                elif event.key == pygame.K_c: # if user pressed c

                    startup_inventory()
                
                elif event.key == pygame.K_u: # if user pressed u
                        
                    self.selected_stack.append(vector(self.pos.x,self.pos.y)) # add the user's current position to a stack (list)

                    if len(self.selected_stack) == 2: # if the length of the stack is 2

                        self.devbarrier_stack.append(DEVBarrier(self.selected_stack[0].x,self.selected_stack[0].y,self.selected_stack[1].x,self.selected_stack[1].y,self.game,self)) # create a DEVBarrier, and append it to a list
                        self.selected_stack = [] # clear the contents of selected_stack

                    time.sleep(0.2) # pause for 0.2 seconds (prevents accidental spam)

                elif event.key == pygame.K_BACKSPACE: # if user pressed backspace

                    if len(self.devbarrier_stack) > 0: # check that there are devbarriers placed
                    
                        self.game.devbarrier_group.remove(self.devbarrier_stack[-1]) # remove last devbarrier in devbarrier_group
                        self.game.entities_group.remove(self.devbarrier_stack[-1])
                        del self.devbarrier_stack[-1] # remove last devbarrier in devbarrier_stack
                        del self.coordinates_stack[-1] # remove last devbarrier in coordinates_stack

                        time.sleep(0.2) # pause for 0.2 seconds (prevents accidental spam)
                        
                elif event.key == pygame.K_RETURN:

                    print("")
                    
                    for coordinate in self.coordinates_stack:

                        print(coordinate)

            elif event.type == pygame.MOUSEBUTTONUP: # when the user releases their finger from clicking the mouse

                self.collision_detection(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1,True) # check with what the mouse is touching

        self.pos += self.vel
        self.offset -= self.vel
    
        if self.collision_detection(self.pos.x,self.pos.y,self.w,self.h): # check for collisions
    
            self.pos -= self.vel # undo movement
            self.offset += self.vel
            
        self.animate()    

    def draw(self,screen):

        boost = vector(0,-12) # an offset to boost the player's sprite above his hitbox (gives a 3d depth feel)
        screen.blit(self.sprite, (self.pos + self.game.player.offset + boost)) # blit the entity's sprite at his position.
        surf = pygame.Surface((1,1))
        surf.fill(RED)
        screen.blit(surf,(self.pos +self.game.player.offset))
    def victory(self,player,attacker):

        Heroes[self.name].attributes['Health'] = player.health # save the player's health
        Heroes[self.name].attributes['Gold'] = str(int(Heroes[self.name].attributes['Gold']) + int(Heroes[attacker.name].attributes['Gold'])) # save the player's gold

    def death(self,player):

        self.game.screen.blit(self.game.death_screen,(0,0)) # draw the death screen
        pygame.display.flip() # update screen

        dead = True 
        while dead: # wait until not dead

            self.dt = self.game.clock.tick(FPS)/1000 # get the difference in time since last called. limit fps to 60 

            for event in pygame.event.get(): # loop through all events

                if event.type == pygame.KEYDOWN: # check if key has been pressed

                    if event.key == pygame.K_SPACE: # if user pressed space

                        dead = False # end loop

        print("YOU'RE ALIVE!?!?")
        self.vel.x = self.pos.x - 1033
        self.vel.y = self.pos.y - 644
        Heroes['Player'].attributes['Gold'] = 0
        
    def game_over(self):

        self.game.screen.blit(self.game.victory_screen,(0,0)) # draw the death screen
        pygame.display.flip() # update screen

        over = True 
        while over: # wait until not dead

            self.dt = self.game.clock.tick(FPS)/1000 # get the difference in time since last called. limit fps to 60 

            for event in pygame.event.get(): # loop through all events

                if event.type == pygame.KEYDOWN: # check if key has been pressed

                    if event.key == pygame.K_SPACE: # if user pressed space

                        over = False # end loop

        self.pos.x = 3500
        self.pos.y = 450
        
        Shops['EndGameShop'].buy('Mayonnaise')
        self.game.leave()

        
class Enemy(Character):

    def __init__(self,x,y,w,h,game,name):

        Character.__init__(self,x,y,w,h,game,name) # run its parent's (Character) __init__ procedure
        self.spawn_delay = 1 # delay before this entity spawns

        #self.sprite.fill(ORANGE)
        
    def update(self): # overwrite character's update method

        temp = self.game.player.pos - self.pos # a vector containing player pos pointing towards the enemy
        
        self.vel.x,self.vel.y = (0,0) # clear the velocity vectors

        if self.distance < 0: # get a new direction to move

            if abs(temp.x) >= abs(temp.y): # check whether he is closer in the x or y dimension

                if temp.x >=0: # check whether to move left or right to get closer to the player

                    self.direction = 3

                if temp.x < 0: # check whether to move left or right to get closer to the player

                    self.direction = 2

            else:

                if temp.y >=0: # check whether to move up or down to get closer to the player

                    self.direction = 0

                if temp.y < 0: # check whether to move up or down to get closer to the player

                    self.direction = 1

            self.distance = 10 # repeat 100 times before getting a new direction (prevents character from making unnatural movements

        else: # keep moving in current direction

            self.distance -= 1 # subtract from the distance
                
        [self.move_down,self.move_up,self.move_left,self.move_right][self.direction]() # move in the direction you are facing

        self.pos += self.vel

        if self.collision_detection(self.pos.x,self.pos.y,self.w,self.h):

            self.pos -= self.vel

        self.animate()

    def spawn(self):

        self.game.respawning.remove(self)

class Friend(Character):

    def __init__(self,x,y,w,h,game,name):

        Character.__init__(self,x,y,w,h,game,name)
        self.ID = 'Friend'
        self.sprite = entityList[1][self.ID].animationList[0]
        self.level = Heroes[name].attributes['level']

class ChatBox(Entity):

    def __init__(self,game):
        
        Entity.__init__(self,0,SCREEN_HEIGHT - CHAT_HEIGHT,SCREEN_WIDTH,CHAT_HEIGHT,game) # run parent's (Entity) __init__ method

        self.sprite = pygame.Surface((self.w,self.h)) # create a surface with dimensions w x h
        self.sprite.fill(WHITE) # fill the surface green (R,G,B) (255,255,255)
        self.sprite.set_alpha(CHAT_OPACITY) # make the chatbox transparent

        self.text = self.game.font.render((''), 1, (BLACK))
        self.empty = True
        
    def set_text(self,text):

        self.text = self.game.font.render((text), 1, (BLACK))

        if len(text) > 0:

            self.empty = False

        else:

            self.empty = True

    def render(self):

        if not self.empty:

            self.game.screen.blit(self.sprite, (self.pos))
            self.game.screen.blit(self.text, self.pos)
    
        
class Barrier(Entity):

    def __init__(self,x,y,w,h,game):
        
        Entity.__init__(self,x,y,w,h,game) # run its parent's (Entitiy) __init__ procedure

        self.sprite = pygame.Surface((w,h)) # create a surface with dimensions w x h
        #self.sprite.fill(PURPLE) # fill the surface green (R,G,B) (0,255,0)
        self.game.barrier_group.add(self) # adds this sprite to the blitable_group in main
        self.sprite.set_alpha(ALPHA) # make it transparent

    def draw(self,screen):
        pass
        #screen.blit(self.sprite, (self.pos + self.game.player.offset)) # blit the entity's sprite at his position.
        

class DEVBarrier(Entity):

    def __init__(self,x_1,y_1,x_2,y_2,game,player):
                
        self.x = round(x_1,2) # top left x coordinate (rounded to 1 D.P)
        self.y = round(y_1,2) #top left y coordinate (rounded to 1 D.P)
        self.w = round(x_2 - x_1,2) # calculates the width (rounded to 1 D.P)
        self.h = round(y_2 - y_1,2) # calculates the height (rounded to 1 D.P)

        Entity.__init__(self,self.x,self.y,self.w,self.h,game) # run its parent's __init__

        self.sprite = pygame.Surface((self.w,self.h)) # create a surface of its size's dimensions
        self.sprite.fill(RED) # colour it red

        self.sprite.set_alpha(ALPHA) # make it transparent

        self.game.devbarrier_group.add(self) # add it the main game's devbarrier list

        player.coordinates_stack.append(("Barrier(" + str(self.x) + "," + str(self.y) + "," + str(self.w) + "," + str(self.h) + ",game)")) # allows copy paste of the devbarrier's information to be converted into a real barrier

    def draw(self,screen):

        screen.blit(self.sprite, (self.pos + self.game.player.offset)) # blit the entity's sprite at his position.
        

class SHOPBarrier(Barrier):

    def __init__(self,x,y,w,h,game):

        Barrier.__init__(self,x,y,w,h,game) # run its parent's (Barrier) __init__ procedure

        #self.sprite.fill(YELLOW) # colour it yellow

class SpawnableEnemy(Enemy):

    def __init__(self,x,y,w,h,game,name):

        Enemy.__init__(self,x,y,w,h,game,name) # run its parent's (Enemy) __init__ procedure

        game.respawning.append(self)
        
        game.collide_group.remove(self)
        game.entities_group.remove(self)
        game.character_group.remove(self)

        self.spawn_delay = 3 # delay before this entity spawns

        self.timer = pygame.time.get_ticks() + self.spawn_delay * 1000
        
    def spawn(self):

        if pygame.time.get_ticks() > self.timer: # check if enough time has passed for it to respawn

            self.game.collide_group.add(self)
            self.game.entities_group.add(self)
            self.game.character_group.add(self)
            self.game.blitable_group.add(self) # removes this sprite from the blitable_group in main
            self.game.respawning.remove(self)

            Heroes[self.name].attributes['x'] = 2274
            Heroes[self.name].attributes['y'] = 1426

            self.pos.x = 2274
            self.pos.y = 1426

            if self.game.difficulty == 0:

                Heroes[self.name].attributes['Health'] = int(2.72**random.randint(0,6)+300)
                Heroes[self.name].attributes['Strength'] = str(random.randint(10,50))
                Heroes[self.name].attributes['Speed'] = str(random.randint(10,70))
                Heroes[self.name].attributes['XP'] = str(random.randint(0,5))
                Heroes[self.name].attributes['Gold'] = str(random.randint(80,120))

                Heroes[self.name].attributes['Weapon'] = 'Empty'
                Heroes[self.name].attributes['Breastplate'] = 'Empty'
            

            elif self.game.difficulty == 1:

                Heroes[self.name].attributes['Health'] = int(2.72**(random.randint(0,6)*1.1)+400)
                Heroes[self.name].attributes['Strength'] = str(random.randint(40,100))
                Heroes[self.name].attributes['Speed'] = str(random.randint(5,100))
                Heroes[self.name].attributes['XP'] = str(random.randint(5,20))
                Heroes[self.name].attributes['Gold'] = str(random.randint(150,500))

                Heroes[self.name].attributes['Weapon'] = ['Empty','Basic_Sword'][random.randint(0,1)]
                Heroes[self.name].attributes['Breastplate'] = 'Empty'
            
            elif self.game.difficulty == 2:

                Heroes[self.name].attributes['Health'] = int(2.72**(random.randint(0,6)*1.2)+500)
                Heroes[self.name].attributes['Strength'] = str(random.randint(100,150))
                Heroes[self.name].attributes['Speed'] = str(random.randint(80,150))
                Heroes[self.name].attributes['XP'] = str(random.randint(20,100))
                Heroes[self.name].attributes['Gold'] = str(random.randint(1000,2500))

                Heroes[self.name].attributes['Weapon'] = 'Expensive_Sword'
                Heroes[self.name].attributes['Breastplate'] = 'Basic_Steel_Breastplate'
            

class SPAWNBarrier(Barrier):

    def __init__(self,x,y,w,h,game):

        Barrier.__init__(self,x,y,w,h,game) # run its parent's (Barrier) __init__ procedure

        #self.sprite.fill(ORANGE) # colour it orange

class TK(Character):

    def __init__(self,x,y,w,h,game,name):

        Character.__init__(self,x,y,w,h,game,name)
        self.ID = 'TK'
        self.sprite = entityList[1][self.ID].animationList[0]

class INNBarrier(Barrier):

    def __init__(self,x,y,w,h,game):
        
        Barrier.__init__(self,x,y,w,h,game) # run its parent's (Barrier) __init__ procedure

        #self.sprite.fill(CYAN) # colour it cyan

class DOORABarrier(Barrier):

    def __init__(self,x,y,w,h,game):
        
        Barrier.__init__(self,x,y,w,h,game) # run its parent's (Barrier) __init__ procedure

        #self.sprite.fill(GREEN) # colour it green

class DOORBBarrier(Barrier):

    def __init__(self,x,y,w,h,game):
        
        Barrier.__init__(self,x,y,w,h,game) # run its parent's (Barrier) __init__ procedure

        #self.sprite.fill(GREEN) # colour it green

class TELEPORTOUTSHOPBarrier(Barrier):

    def __init__(self,x,y,w,h,game):
        
        Barrier.__init__(self,x,y,w,h,game) # run its parent's (Barrier) __init__ procedure

        #self.sprite.fill(BLUE) # colour it blue

class TELEPORTTOSHOPBarrier(Barrier):

    def __init__(self,x,y,w,h,game):
        
        Barrier.__init__(self,x,y,w,h,game) # run its parent's (Barrier) __init__ procedure

        #self.sprite.fill(BLUE) # colour it blue

class ShopKeeper(Character):

    def __init__(self,x,y,w,h,game,name):

        Character.__init__(self,x,y,w,h,game,name)
        self.ID = 'Friend'
        self.sprite = entityList[3][self.ID].animationList[0]

    def update(self): # stop shop keeper from running away

        pass

class KeyDealerA(Character):

    def __init__(self,x,y,w,h,game,name):

        Character.__init__(self,x,y,w,h,game,name)
        self.ID = 'Friend'
        self.sprite = entityList[0][self.ID].animationList[0]

    def update(self): # stop key dealer from running away

        pass

class KeyDealerB(Character):

    def __init__(self,x,y,w,h,game,name):

        Character.__init__(self,x,y,w,h,game,name)
        self.ID = 'Friend'
        self.sprite = entityList[0][self.ID].animationList[0]

    def update(self): # stop key dealer from running away

        pass

class Michael(Character):

    def __init__(self,x,y,w,h,game,name):

        Character.__init__(self,x,y,w,h,game,name)
        self.ID = 'Friend'
        self.sprite = entityList[0][self.ID].animationList[0]

class NOCHARACTERBarrier(Barrier):
    
    def __init__(self,x,y,w,h,game):
        
        Barrier.__init__(self,x,y,w,h,game) # run its parent's (Barrier) __init__ procedure

        #self.sprite.fill(YELLOW) # colour it yellow

class Harry(Character):

    def __init__(self,x,y,w,h,game,name):

        Character.__init__(self,x,y,w,h,game,name)
        self.ID = 'Friend'
        self.sprite = entityList[0][self.ID].animationList[0]

class Clear:

    def __init__(self,*arg):

        pass
    
