from config import *
from panda3d.core import Point2,Point3,Vec3,Vec4
#This helps reduce the amount of code used by loading objects, since all of the
#objects are pretty much the same.
def loadObject(tex = None, pos = Point2(0,0), depth = SPRITE_POS, scale = 1,
               transparency = True):
  obj = loader.loadModel("models/plane") #Every object uses the plane model
  obj.reparentTo(camera)              #Everything is parented to the camera so
                                      #that it faces the screen
  obj.setPos(Point3(pos.getX(), depth, pos.getY())) #Set initial position
  obj.setScale(scale)                 #Set initial scale
  obj.setBin("unsorted", 0)           #This tells Panda not to worry about the
                                      #order this is drawn in. (it prevents an
                                      #effect known as z-fighting)
  obj.setDepthTest(False)             #Tells panda not to check if something
                                      #has already drawn in front of it
                                      #(Everything in this game is at the same
                                      #depth anyway)
  if transparency: obj.setTransparency(1) #All of our objects are trasnparent
  if tex:
    tex = loader.loadTexture("textures/"+tex+".png") #Load the texture
    obj.setTexture(tex, 1)                           #Set the texture

  return obj