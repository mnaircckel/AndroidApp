from math import pi

TILE_SIZE = 32
SPRITE_POS = 60     #At default field of view and a depth of 60, the screen
SCREEN_X = 20       #Screen goes from -20 to 20 on X
SCREEN_Y = 15       #Screen goes from -15 to 15 on Y
TURN_RATE = 100     #Degrees ship can turn in 1 second
ACCELERATION = 10    #Ship acceleration in units/sec/sec
MAX_VEL = 20         #Maximum ship velocity in units/sec
MAX_VEL_SQ = MAX_VEL ** 2  #Square of the ship velocity
DEG_TO_RAD = pi/180 #translates degrees to radians for sin and cos
BULLET_LIFE = 2     #How long bullets stay on screen before removed
BULLET_REPEAT = .2  #How often bullets can be fired
BULLET_SPEED = 10   #Speed bullets move
AST_INIT_VEL = 1    #Velocity of the largest asteroids
AST_INIT_SCALE = 3  #Initial asteroid scale
AST_VEL_SCALE = 2.2 #How much asteroid speed multiplies when broken up
AST_SIZE_SCALE = .6 #How much asteroid scale changes when broken up
AST_MIN_SCALE = 1.1 #If and asteroid is smaller than this and is hit,
                    #it disapears instead of splitting up