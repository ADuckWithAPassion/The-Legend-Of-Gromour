# Run the overworld
from Barriers import *

class Game: 

    def __init__(self):
        
        pygame.init() # initialize pygame. Allows use of its modules

        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # create a window with the dimensions SCREEN_WIDTH by SCREEN_HEIGHT
        self.clock = pygame.time.Clock() # create a pygame clock - used to measure time between frames
        pygame.key.set_repeat(1)
        self.font = pygame.font.SysFont('Comic Sans MS', CHAT_SIZE)

        self.background = pygame.image.load('map.png') # load an image 
        self.death_screen = pygame.image.load('death2.png')
        self.victory_screen = pygame.image.load('victory2.png')
        self.death_screen = pygame.transform.scale(self.death_screen, (SCREEN_WIDTH,SCREEN_HEIGHT))
        
        self.startup()
        
    def startup(self):

        self.entities_group = pygame.sprite.Group() # create a group to contain every entity
        self.blitable_group = pygame.sprite.Group() # create a group to contain all blitable entities (must have a surface)
        self.barrier_group = pygame.sprite.Group() # create a group to contain all barrier entities
        self.devbarrier_group = pygame.sprite.Group() # create a group to contain all devbarrier entities
        self.character_group = pygame.sprite.Group() # create a group to contain all character entitites
        self.collide_group = pygame.sprite.Group() # create a group to contain anything that should have a collision test

        self.player = Player(Heroes['Player'].attributes['x'],Heroes['Player'].attributes['y'],Heroes['Player'].attributes['w'],Heroes['Player'].attributes['h'],self,'Player') # create the player manually
        self.chatbox = ChatBox(self) # create chatbox manually
        
        classes = {'Player':Player,'Character':Character,'Enemy':Enemy,'Friend':Friend,'SpawnableEnemy':SpawnableEnemy,'TK':TK,'Clear':Clear,'ShopKeeper':ShopKeeper,'KeyDealerA':KeyDealerA, 'KeyDealerB':KeyDealerB,'Michael':Michael,'Harry':Harry} # a dictionary linking strings to their classes
        self.respawning = [] # a list of all enemies waiting to respawn
        self.difficulty = 0
        
        for hero in Heroes:

            if Heroes[hero].attributes['Class'] != 'Player': # don't create a second version of the player

                classes[Heroes[hero].attributes['Class']](Heroes[hero].attributes['x'],Heroes[hero].attributes['y'],Heroes[hero].attributes['w'],Heroes[hero].attributes['h'],self,Heroes[hero].attributes['Name']) # create object in game
                                
        load_barriers(self)

        self.collide_group.add(self.barrier_group.sprites()+self.character_group.sprites())
        self.entities_group.add(self.devbarrier_group.sprites())

        self.loop = True
        while self.loop: # loop until self.loop is set to false

            self.dt = self.clock.tick(FPS)/1000 # get the difference in time since last called. limit fps to 60 

            if self.dt >= 0.05: # if the user's FPS is below 20

                self.dt = 0.05 # set dt to as if the user was running at 20 FPS

            for hero in self.respawning:
                
                hero.spawn()
                    
            self.update() # update entities
            self.render() # render to screen
            
    def update(self):

        for entity in self.entities_group.sprites(): # loop through all entities in entities_group.sprites()

            temp = entity.pos - self.player.pos # a vector from player's position pointing to entity's position
            
            if temp.length() >= UPDATE_RANGE: # if the entity is too far

                continue # go to the next entity 

            entity.update() # run the entity's update procedure
            
    def render(self):

        self.screen.fill(BLACK) # clears the screen
        self.screen.blit(self.background,(self.player.offset)) # displays the background as the base layer
        
        for entity in self.entities_group.sprites(): # loop through all entities in self.entities_group

            if entity == self.player: # if the entity is the player

                continue # exit

            entity.draw(self.screen) # draw the entity to the screen

        self.player.draw(self.screen) # draw the player to the screen after (to prevent the player from appearing underneath other characters)
        
        self.chatbox.render() # draw the chatbox
    
        pygame.display.flip() # update any changes to the screen

    def leave(self):

        for sprite in self.character_group: # loop through all characters existing in the game
            
            Heroes[sprite.name].attributes['x'] = str(int(sprite.pos.x)) # update the x position
            Heroes[sprite.name].attributes['y'] = str(int(sprite.pos.y)) # update the y position

            Heroes[sprite.name].save_data() # save the changes made
        
        pygame.quit() # exit pygame
        sys.exit() # end python
    
game = Game() # launch the game
