#import scipy.stats
#from scipy.stats.stats import kendalltau
import os
import hyperneat
import random

import pygame
from pygame.locals import *
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

objectives=[]

obj_popsize=50
art_popsize=5
evals=20
debug=False
quit=False

out_dir="obj3"
gen=0
print_out=50

if debug:
 obj_popsize=16
 art_popsize=10
 evals=10
 print_out=1

for k in range(obj_popsize):
 newobj=objective(art_popsize,evals)
 objectives.append(newobj)

while(not quit):
 gen+=1
 print "generation ", gen
 print "evolving pictures for objectives"
 #evolve objectives for a bit
 for k in objectives:
  k.evaluate()
  k.evolve()
 #to assign fitness to an objective, we need to measure
 #it's heritability and its novelty

 print "measuring rankings for reference set"
 #to measure novelty, we create a reference group
 reference=[k.artists[0] for k in objectives]
 #and see how differently the objectives rank this group
 for k in objectives:
  fitnesses=[k.critic.evaluate_artist(z) for z in reference]
  k.ranks = create_rankings(fitnesses)
  k.novelty = 0.0

 #now measure an objective's novelty
 for k in objectives:
  dists=[rankdist(k.ranks,z.ranks) for z in objectives]
  dists.sort(reverse=True)
  k.novelty += sum(dists[:15])
  k.heritability = -herit_measure(k.herit) 
  k.objectives=[k.novelty] #,k.heritability]
  #print k.novelty,k.heritability
 
 if((gen-1)%print_out==0):
  print "saving progress..."
  os.system("mkdir %s/gen_%d" % (out_dir,gen))
  
  counter=0
  for k in objectives:
   k.save("%s/gen_%d/obj%d.dat" % (out_dir,gen,counter))
   counter+=1

 #now select objectives 
 objectives=multiobjective_select(objectives)
 arts=[k.artists[0] for k in objectives[:16]]
 
 gs=4
 #if(optimize):
  #for z in xrange(50)`:
  #cur_obj.artists[0].optimize(dummy)
   #cur_obj.artists[k].optimize(cur_obj.critic)
   
 for k in range(16):
  if(not arts[k].isrendered()):
   arts[k].render_picture()
  if(not arts[k].get_nanflag()):
   render_picture(25+(k%gs)*180,25+(k/gs)*180,PXS,arts[k].get_picture())
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

