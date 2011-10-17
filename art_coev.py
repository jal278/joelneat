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

nectar_pop = []
nectarless_pop = []
critic_pop = []
direc="coev3"
for k in range(100):
 print k
 new_art=hyperneat.artist()
 new_art.fitness=0
 nectar_pop.append(new_art)
 new_art=hyperneat.artist()
 new_art.fitness=0
 nectarless_pop.append(new_art)

for k in range(100):
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
 print "rendering art"
 for art in nectar_pop:
  art.render_picture()
  art.fitness=0.0
  art.ranks=[]
  art.best=0
  art.nectar=1
  art.worst=10000
  art.selected=None
 
 for art in nectarless_pop:
  art.render_picture()
  art.fitness=0.0
  art.ranks=[]
  art.best=0
  art.nectar=0
  art.worst=10000
  art.selected=None

 total_pop=nectar_pop+nectarless_pop
 print "critiquing art"
 for crit in critic_pop:
  ranks=[]
  fits=[]
  for art in total_pop:
   fit = crit.evaluate_artist(art)
   fits.append((fit,art.nectar)) 

  ranks=zip(fits,range(len(total_pop)))
  ranks.sort()
  contextranks=ranks 
  a,ranks=zip(*ranks)
  #crit's order of artwork
  crit.ranks=contextranks
  crit.fits=fits
  for k in range(len(total_pop)):
   art = total_pop[ranks[k]]
   art.ranks.append(k)
   if(art.best<k):
    art.best=k
    art.selected=crit
   if(art.worst>k):
    art.worst=k
 print "calculating fitness"
 #now to calculate fitnesses for artists and critics
 for art in total_pop:
  if(art.get_nanflag()):
   art.fitness = -100.0
   art.clear_picture()
  else:
   art.ranks.sort(reverse=True)
   art.fitness = sum(art.ranks) #sum(art.ranks[:3])
 
 for crit in critic_pop:
  crit.fitness=0
  counter=0
  for (f,n) in crit.ranks:
   (fit,nect) = f
   if nect==1:
    crit.fitness+=counter
   counter+=1
  #dists=[kendalltau(crit.ranks,k`.ranks)[0] for k in critic_pop]
  #dists=[rankdist(crit.ranks,k.ranks) for k in critic_pop]
  #dists.sort(reverse=True)
  #crit.fitness += sum(dists[:15])
  #crit.fitness = random.random()

 nectar_pop.sort(key=lambda k:k.fitness,reverse=True)
 print "nectar total:" , sum([k.fitness for k in nectar_pop])
 nectarless_pop.sort(key=lambda k:k.fitness,reverse=True)
 print "nectarless_total:" , sum([k.fitness for k in nectarless_pop])

 gs=4
 for k in range(16):
  total_pop=nectar_pop[:8]+nectarless_pop[:8]
  render_picture(25+(k%gs)*180,25+(k/gs)*180,PXS,total_pop[k].get_picture())
 
 if(render):
  screen.blit(background,(0,0))
  pygame.display.flip()
 if((gen)%50==0):
  directory="%s/generation%d"%(direc,gen)
  os.system("mkdir %s" % directory)
  afname = directory+"/nart%d"
  afname2 = directory+"/art%d"
  cfname = directory+"/crit%d"
  save_pop(critic_pop,cfname)
  save_pop(nectar_pop,afname)
  save_pop(nectarless_pop,afname2)
 critic_pop = create_new_pop_gen(critic_pop,0.3)
 nectar_pop = create_new_pop_gen(nectar_pop,0.3)
 nectarless_pop = create_new_pop_gen(nectarless_pop,0.3)

for k in art_pop:
 del k
for k in critic_pop:
 del k
gc.collect()
