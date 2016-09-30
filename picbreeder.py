import hyperneat
import random

import pygame
from pygame.locals import *
from art_basics import *

render=True

#PYGAME SETUP
screen,background=None,None
if(render):
 pygame.init()
 screen = pygame.display.set_mode((700, 700))
 background = pygame.Surface(screen.get_size())
 background = background.convert()
 background.fill((255, 255, 255))
 screen.blit(background, (0, 0))
 pygame.display.flip()

SX=SY=64
PXS = 2

def render_picture(x,y,pxsize,data):
 global render,screen,background,SX,SY
 if(not render):
  return
 for xc in range(SX):
  for yc in range(SY):
   px=int ( (data[xc][yc])*256)
   px=min(px,255)
   px=max(px,0)
   pygame.draw.circle(background, (px,px,px), (x+xc*pxsize,y+yc*pxsize),pxsize,0)

def render_artist(x,y,pxsize,artist):
 global render,screen,background,SX,SY
 if(not render):
  return
 render_picture(x,y,pxsize,artist.get_picture())
 ycoord = y+SY*pxsize+5
 xcoord = x
 xlen = int(SX*pxsize * artist.fitness)
 if (xlen<0 or xlen>SX*pxsize):
  xlen=0
 pygame.draw.line(background, (0,255,0), (xcoord,ycoord),(xcoord+xlen,ycoord),5) 
a=hyperneat.artist()
a.random_seed()
artists = []

import sys
popsize=9

for k in range(popsize):
 n = hyperneat.artist()
 n.fitness=0
 n.render_picture()
 artists.append(n)

quit=False
render_art=True

while(not quit):
 gs=3
 #if(optimize):
  #for z in xrange(50):
  #cur_obj.artists[0].optimize(dummy)
   #cur_obj.artists[k].optimize(cur_obj.critic)
 for k in range(popsize):
  if(render_art):
   render_artist(25+(k%gs)*180,25+(k/gs)*180,PXS,artists[k])
   
 if(render):
  screen.blit(background,(0,0))
  pygame.display.flip()
 background.fill((0, 0, 255))
 
 for event in pygame.event.get():
  if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
   quit=True
  elif event.type==KEYDOWN:
   if(event.key==K_t):
    render_art=not render_art
   if(event.key==K_o):
    optimize=not optimize
   if(event.key==K_e):
    cur_obj.evolve()
   if(event.key==K_f):
    cur_obj.evaluate()
    print [k.fitness for k in cur_obj.artists]
   elif(event.key>=K_0 and event.key<=K_9):
    cur_obj_num = event.key-K_0
   elif(event.key==K_s):
    objectives=[]
    for k in range(10):
     print "creating objective ",k
     newobj=make_new(cur_obj)
     newobj.evaluate()
     newobj.evolve()
     objectives.append(newobj)

