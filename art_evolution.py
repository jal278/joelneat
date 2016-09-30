#import scipy.stats
#from scipy.stats.stats import kendalltau
import os
import hyperneat
import random
from guppy import hpy

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

a=hyperneat.artist()
a.random_seed()
art_pop = []
critic_pop = []

for k in range(400):
 print k
 new_art=hyperneat.artist()
 new_art.fitness=0
 art_pop.append(new_art)

for k in range(50):
 new_critic=critic_class()
 new_critic.fitness=0
 critic_pop.append(new_critic)

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

gen=0
while(True):
 print "generation:" ,gen
 gen+=1
 critic_lifespan=10
 print "rendering art"
 for art in art_pop:
  art.render_picture()
  art.fitness=0.0
  art.ranks=[]
  art.best=0
  art.worst=10000
  art.selected=None
 print "critiquing art"
 for crit in critic_pop:
  ranks=[]
  fits=[]
  for art in art_pop:
   fits.append(crit.evaluate_artist(art))
 
  ranks=zip(fits,range(len(art_pop)))
  ranks.sort()
  
  a,ranks=zip(*ranks)
  #crit's order of artwork
  crit.ranks=ranks
  crit.fits=fits
  for k in range(len(art_pop)):
   art = art_pop[ranks[k]]
   art.ranks.append(k)
   if(art.best<k):
    art.best=k
    art.selected=crit
   if(art.worst>k):
    art.worst=k
 print "calculating fitness"
 #now to calculate fitnesses for artists and critics
 for art in art_pop:
  if(art.get_nanflag()):
   art.fitness = -100.0
   art.clear_picture()
  else:
   art.ranks.sort(reverse=True)
   art.fitness = art.best #sum(art.ranks[:3])
  
 for crit in critic_pop:  
  #dists=[kendalltau(crit.ranks,k.ranks)[0] for k in critic_pop]
  dists=[rankdist(crit.ranks,k.ranks) for k in critic_pop]
  dists.sort(reverse=True)
  crit.fitness += sum(dists[:15])
  #crit.fitness = random.random()

 art_pop.sort(key=lambda k:k.fitness,reverse=True)
 
 gs=4
 for k in range(16):
  render_picture(25+(k%gs)*180,25+(k/gs)*180,PXS,art_pop[k].get_picture())
 
 if(render):
  screen.blit(background,(0,0))
  pygame.display.flip()
 if((gen)%50==0):
  directory="generation%d"%gen
  os.system("mkdir %s" % directory)
  afname = directory+"/art%d"
  cfname = directory+"/crit%d"
  save_pop(critic_pop,cfname)
  save_pop(art_pop,afname)
 if(gen%critic_lifespan==0):
  print "criticgen: ",gen/critic_lifespan
  critic_pop = create_new_pop(critic_pop,0.3)
 art_pop = create_new_pop(art_pop,0.3)

for k in art_pop:
 del k
for k in critic_pop:
 del k
gc.collect()
