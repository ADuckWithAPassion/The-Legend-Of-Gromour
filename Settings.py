# Contains any settings/constants for the game
from InventoryGUI import *

# SCREEN SETTINGS
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

#COLOURS
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)
ORANGE = (255,105,0)

#COLLISIONS
ALPHA = 150 # (0 - 255)

#VECTORS
vector = pygame.math.Vector2

#PLAYER
PLAYER_SPEED = 120
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_POS_X = 30
PLAYER_POS_Y = 30

#GAME SETTINGS
FPS = 60
UPDATE_RANGE = 250
DEV_MODE = True

#CHAT BOX
CHAT_WIDTH = SCREEN_WIDTH
CHAT_HEIGHT = 50
CHAT_OPACITY = 90
CHAT_SIZE = 16

### TO ESTABLISH A NEW COLLISION BOX IN GAME, YOU MUST FIRST ENSURE THAT DEV_MODE IS SET TO TRUE
### LAUNCH UP THE GAME AND WALK TO THE REGION WHERE YOU WANT TO CREATE A COLLISION BOX
### PRESS U IN BOTH CORNERS OF THE AREA YOU WANT
### A SHADED REGION SHOULD APPEAR - IF THIS WAS NOT THE AREA YOU WANTED, PRESS BACKSPACE TO REMOVE THE MOST RECENTLY CREATED COLLISION BOX FROM THE QUEUE
### YOU CAN SELECT MULTIPLE REGIONS
### ONCE ALL REGIONS HAVE BEEN SELECTED, PRESS ENTER. TEXT WILL APPEAR IN THE SHELL.
### COPY THIS TEXT INTO BARRIERS.PY
### IF YOU WANT TO CREATE A UNIQUE BARRIER (SUCH AS A TELEPORTER, DOOR, ECT), THEN YOU MUST RENAME 'BARRIER' TO THE NEW TYPE OF BARRIER
### UPDATE THE COLLISION DETECTION FUNCTION TO HANDLE THAT NEW EVENT
