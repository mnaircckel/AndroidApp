import direct.directbase.DirectStart
from panda3d.core import TextNode
from panda3d.core import Point2,Point3,Vec3,Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from math import sin, cos, pi
from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait,Func
import cPickle, sys
from panda3d.core import GeoMipTerrain

from config import *
from object_loader import *

class World(DirectObject):

  def __init__(self):

    # Terrain
    # terrain = GeoMipTerrain("mySimpleTerrain")
    # terrain.setHeightfield("textures/terrain.png")
    # terrain.getRoot().reparentTo(render)
    # terrain.generate()

    # Accept escape as valid exit for game world
    self.accept("escape", sys.exit)

    # Disable default mouse-based camera control for 2D world
    base.disableMouse()

    # Background for world
    self.bg = loadObject("map", scale = 1200, depth = 200, transparency = False) #Load the background starfield

    # Initialize the player
    self.player = loadObject("ship", scale = 4)
    self.setVelocity(self.player, Vec3(0,0,0))

    # The key events update this list, and our task will query it as input
    self.keys = {"turnLeft" : 0, "turnRight": 0, "accel": 0, "fire": 0}

    # Other keys events set the appropriate value in our key dictionary
    self.accept("arrow_left",     self.setKey, ["turnLeft", 1])
    self.accept("arrow_left-up",  self.setKey, ["turnLeft", 0])
    self.accept("arrow_right",    self.setKey, ["turnRight", 1])
    self.accept("arrow_right-up", self.setKey, ["turnRight", 0])
    self.accept("arrow_up",       self.setKey, ["accel", 1])
    self.accept("arrow_up-up",    self.setKey, ["accel", 0])
    self.accept("space",          self.setKey, ["fire", 1])

    # Now we create the task. taskMgr is the task manager that actually calls
    # The function each frame. The add method creates a new task. The first
    # argument is the function to be called, and the second argument is the name
    # for the task. It returns a task object, that is passed to the function
    # each frame
    self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")
    # The task object is a good place to put variables that should stay
    # persistant for the task function from frame to frame
    self.gameTask.last = 0         # Task time of the last frame
    self.gameTask.nextBullet = 0   # Task time when the next bullet may be fired

    self.bullets = []       #This empty list will contain fired bullets

  # As described earlier, this simply sets a key in the self.keys dictionary to
  # the given value
  def setKey(self, key, val): 
    self.keys[key] = val

  # Handle Velocity Events
  def setVelocity(self, obj, val):
    list = [val[0], val[1], val[2]]
    obj.setTag("velocity", cPickle.dumps(list))

  def getVelocity(self, obj):
    list = cPickle.loads(obj.getTag("velocity"))
    return Vec3(list[0], list[1], list[2])

  # Handle Expires Events
  def setExpires(self, obj, val):
    obj.setTag("expires", str(val))
  
  def getExpires(self, obj):
    return float(obj.getTag("expires"))
        

  #This is our main task function, which does all of the per-frame processing
  #It takes in self like all functions in a class, and task, the task object
  #returned by taskMgr
  def gameLoop(self, task):
    #task contains a variable time, which is the time in seconds the task has
    #been running. By default, it does not have a delta time (or dt), which is
    #the amount of time elapsed from the last frame. A common way to do this is
    #to store the current time in task.last. This can be used to find dt
    dt = task.time - task.last
    task.last = task.time

    #update ship position
    self.updateShip(dt)

    #check to see if the ship can fire
    if self.keys["fire"] and task.time > task.nextBullet:
      self.fire(task.time)  #If so, call the fire function
      #And disable firing for a bit
      task.nextBullet = task.time + BULLET_REPEAT  
    self.keys["fire"] = 0   #Remove the fire flag until the next spacebar press

    #update bullets
    newBulletArray = []
    for obj in self.bullets:
      self.updatePos(obj, dt)         #Update the bullet
      #Bullets have an experation time (see definition of fire)
      #If a bullet has not expired, add it to the new bullet list so that it
      #will continue to exist
      if self.getExpires(obj) > task.time: newBulletArray.append(obj)
      else: obj.remove()              #Otherwise remove it from the scene
    #Set the bullet array to be the newly updated array
    self.bullets = newBulletArray     

    
    return Task.cont    #Since every return is Task.cont, the task will
                        #continue indefinitely

  #Updates the positions of objects
  def updatePos(self, obj, dt):
    vel = self.getVelocity(obj)
    newPos = obj.getPos() + (vel*dt)
    obj.setPos(newPos)

  #This updates the ship's position. This is similar to the general update
  #but takes into account turn and thrust
  def updateShip(self, dt):
    heading = self.player.getR() #Heading is the roll value for this model
    #Change heading if left or right is being pressed
    if self.keys["turnRight"]:
      heading += dt * TURN_RATE
      self.player.setR(heading % 360)
    elif self.keys["turnLeft"]:
      heading -= dt * TURN_RATE
      self.player.setR(heading % 360)

    #Thrust causes acceleration in the direction the ship is currently facing
    if self.keys["accel"]:
      heading_rad = DEG_TO_RAD * heading
      #This builds a new velocity vector and adds it to the current one
      #Relative to the camera, the screen in Panda is the XZ plane.
      #Therefore all of our Y values in our velocities are 0 to signify no
      #change in that direction
      newVel = (
        Vec3(sin(heading_rad), 0, cos(heading_rad)) * ACCELERATION * dt)
      newVel += self.getVelocity(self.player)
      #Clamps the new velocity to the maximum speed. lengthSquared() is used
      #again since it is faster than length()
      if newVel.lengthSquared() > MAX_VEL_SQ:
        newVel.normalize()
        newVel *= MAX_VEL
      self.setVelocity(self.player, newVel)
      
    #Finally, update the position as with any other object
    self.updatePos(self.player, dt)
    base.cam.setX(self.player.getX())
    base.cam.setZ(self.player.getZ())
    #base.cam.lookAt(self.player)

  #Creates a bullet and adds it to the bullet list
  def fire(self, time):
    direction = DEG_TO_RAD * self.player.getR()
    directions = [direction + pi/2, direction - pi/2, direction + 1.396, direction - 1.396, direction + 1.74, direction - 1.74]
    for dir in directions:
      pos = self.player.getPos()
      bullet = loadObject("bullet", scale = .6)  #Create the object
      bullet.setPos(pos)
      #Velocity is in relation to the ship
      vel = (self.getVelocity(self.player) + 
             (Vec3(sin(dir), 0, cos(dir)) *
              BULLET_SPEED))
      self.setVelocity(bullet, vel)

      #Set the bullet expiration time to be a certain amount past the current time
      self.setExpires(bullet, time + BULLET_LIFE)

      #Finally, add the new bullet to the list
      self.bullets.append(bullet)

World()
run()