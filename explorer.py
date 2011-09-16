#import scipy.stats
#from scipy.stats.stats import kendalltau
import hyperneat
import random
from guppy import hpy

import pygame
from pygame.locals import *
import gc
from art_basics import *

#gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
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
   pygame.draw.circle(background, (px,0,0), (x+xc*pxsize,y+yc*pxsize),pxsize,0)

def render_critic(x,y,pxsize,artist):
 global render,screen,background,SX,SY
 if(not render):
  return
 render_picture(x,y,pxsize,artist.get_weight())

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
art_pop = []
critic_pop = []

import sys
load_flag=False
load_gen=0

if (len(sys.argv)>1):
 load_flag=True
 load_gen=int(sys.argv[1])

objectives=[]
popsize=16
for k in range(10):
 if(not load_flag):
  newobj=objective(popsize)
  newobj.evaluate()
  objectives.append(newobj)
 else:
  objectives.append(load_objective(16,load_gen,k))
  objectives[-1].evaluate()

def create_new_pop(oldpop,delete=0.2):
 fits = [k.fitness for k in oldpop]
 fit_sum=sum([k.fitness for k in oldpop])
 #com_sum=sum([k.complexity() for k in oldpop])
 #print "fitness: ", fits
 #print "complexity: ", com_sum
 newpop=[]
 size=len(oldpop)
 oldpop.sort(key=lambda x:x.fitness)
 remove=int(delete*len(oldpop))
 oldpop=oldpop[remove:]
 for k in oldpop:
  new = make_new(k)
  new.fitness=0
  newpop.append(new)
 for k in range(remove):
  new = make_new(random.choice(oldpop))
  new.fitness=0
  newpop.append(new)
 del oldpop
 return newpop

quit=False
cur_obj_num=0
render_art=True
optimize=False
while(not quit):
 cur_obj = objectives[cur_obj_num]
 gs=4
 cur_obj.evolve()
 #if(optimize):
  #for z in xrange(50):
   #cur_obj.artists[0].optimize(dummy)
   #cur_obj.artists[k].optimize(cur_obj.critic)
 for k in range(16):
  if(render_art):
   render_artist(25+(k%gs)*180,25+(k/gs)*180,PXS,cur_obj.artists[k])
  elif k<10:
   render_critic(25+(k%gs)*180,25+(k/gs)*180,PXS,objectives[k].critic)
   
 if(render):
  screen.blit(background,(0,0))
  pygame.display.flip()
 background.fill((255, 255, 255))
 
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

