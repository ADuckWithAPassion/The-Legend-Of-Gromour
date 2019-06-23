from Settings import *

class getEntity:

    def __init__(self,entity,spriteLocation):

        self.animationList=[] # stores different frames of the animation 
        self.entity=pygame.image.load(entity) # load in the spritesheet

        for animation in spriteLocation: # loop through all of the sprite locations

            self.animationList.append(pygame.transform.smoothscale(self.entity.subsurface(animation), (int(16*1.5),int(22*1.5)))) # append all of the frames to a list

entityList=[{},{},{},{}] # stores each direction for every character


entityList[0]['Player']=getEntity('spritesheet7.png',[(0,0,16,22),(16,0,16,22),(32,0,16,22),(0,0,16,22)])
entityList[1]['Player']=getEntity('spritesheet7.png',[(0,22,16,21),(16,22,16,21),(32,22,16,21),(0,22,16,21)])
entityList[2]['Player']=getEntity('spritesheet7.png',[(0,43,16,22),(16,43,16,22),(32,43,16,22),(0,43,16,22)])
entityList[3]['Player']=getEntity('spritesheet7.png',[(0,65,16,22),(16,65,16,22),(32,65,16,22),(0,65,16,22)])

entityList[0]['Enemy']=getEntity('spritesheet7.png',[(48,0,16,22),(64,0,16,22),(80,0,16,22),(48,0,16,22)])
entityList[1]['Enemy']=getEntity('spritesheet7.png',[(48,22,16,21),(64,22,16,21),(80,22,16,21),(48,22,16,21)])
entityList[2]['Enemy']=getEntity('spritesheet7.png',[(48,43,16,22),(64,43,16,22),(80,43,16,22),(48,43,16,22)])
entityList[3]['Enemy']=getEntity('spritesheet7.png',[(48,65,16,22),(64,65,16,22),(80,65,16,22),(48,65,16,22)])

entityList[0]['Friend']=getEntity('spritesheet7.png',[(96,0,16,22),(112,0,16,22),(128,0,16,22),(96,0,16,22)])
entityList[1]['Friend']=getEntity('spritesheet7.png',[(96,22,16,21),(112,22,16,21),(128,22,16,21),(96,22,16,21)])
entityList[2]['Friend']=getEntity('spritesheet7.png',[(96,43,16,22),(112,43,16,22),(128,43,16,22),(96,43,16,22)])
entityList[3]['Friend']=getEntity('spritesheet7.png',[(96,65,16,22),(112,65,16,22),(128,65,16,22),(96,65,16,22)])

entityList[0]['TK']=getEntity('spritesheet7.png',[(144,0,16,22),(160,0,16,22),(176,0,16,22),(144,0,16,22)])
entityList[1]['TK']=getEntity('spritesheet7.png',[(144,22,16,21),(160,22,16,21),(176,22,16,21),(144,22,16,21)])
entityList[2]['TK']=getEntity('spritesheet7.png',[(144,43,16,22),(160,43,16,22),(176,43,16,22),(144,43,16,22)])
entityList[3]['TK']=getEntity('spritesheet7.png',[(144,65,16,22),(160,65,16,22),(176,65,16,22),(144,65,16,22)])

entityList[0]['Player'].animationList[0] = pygame.transform.smoothscale(entityList[0]['Player'].animationList[0], (int(16*1.5),int(22*1.5)))
