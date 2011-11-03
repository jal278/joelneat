import numpy
import os
import hyperneat
import random

import pygame
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
   px=int ( (data[xc][yc]+1.0)*128)
   px=min(px,255)
   px=max(px,0)
   pygame.draw.circle(background, (px,0,0), (x+xc*pxsize,y+yc*pxsize),pxsize,0)

hyperneat.artist.random_seed()
art_pop = []
nov_crit = novelty_mapper()

for k in range(400):
 new_art=hyperneat.artist()
 new_art.fitness=0
 art_pop.append(new_art)

def make_new(ind):
 child=ind.copy()
 if(random.random()>0.2):
  child.mutate()
 return child

def save_pop(pop,fname):
 count=0
 for k in pop:
  k.save(fname%count)
  count+=1

def create_new_pop(oldpop,delete=0.2):
 fit_sum=sum([k.fitness for k in oldpop])
 com_sum=sum([k.complexity() for k in oldpop])
 print "fitness: ", fit_sum
 print "complexity: ", com_sum
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

gen=0

while(True):
 print "generation:" ,gen
 gen+=1
 print "rendering art"
 for art in art_pop:
  art.render_picture()
  art.fitness=0.0
  art.ranks=[]
  art.behavior=numpy.array(nov_crit.evaluate_artist(art))
 
 print "calculating fitness"
 #now to calculate fitnesses for artists and critics
 for art in art_pop:
  if(art.get_nanflag()):
   art.fitness = -100.0
   art.clear_picture()
  else:
   art.dists=[((art.behavior-x.behavior)**2).sum() for x in art_pop]
   art.dists.sort()
   art.fitness = sum(art.dists[:20])   

 art_pop.sort(key=lambda k:k.fitness,reverse=True)
 
 gs=4
 for k in range(16):
  render_picture(25+(k%gs)*180,25+(k/gs)*180,PXS,art_pop[k].get_picture())
 
 if(render):
  screen.blit(background,(0,0))
  pygame.display.flip()
 if((gen)%50==0):
  directory="ns4/generation%d"%gen
  os.system("mkdir %s" % directory)
  afname = directory+"/art%d"
  save_pop(art_pop,afname)
 art_pop = create_new_pop(art_pop,0.3)

for k in art_pop:
 del k
gc.collect()
