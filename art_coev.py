#import scipy.stats
#from scipy.stats.stats import kendalltau
import os
import hyperneat
import random
from guppy import hpy

import pygame
import gc
from art_basics import *
from art_coev_basics import *
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

direc="coev2"
nectar_pop,nectarless_pop,critic_pop= ([],[],[])
if(False):
 load_dir=direc+"/generation800/"
 nectar_pop=load_pop(load_dir+"nart%d",100,hyperneat.artist)
 nectarless_pop=load_pop(load_dir+"art%d",100,hyperneat.artist)
 critic_pop=load_pop(load_dir+"crit%d",100,critic_class)
else:
 nectar_pop,nectarless_pop = create_flowers(100)
 critic_pop = create_critics(100)

gen=0
migrate=0.01
migrate_count=3
cycle_len=5
ART=0
CRITIC=1
cycle=ART
while(True):
 print "generation:" ,gen
 gen+=1

 print "starting."  
 if(cycle==ART):
  print "rendering art"
 for art in nectar_pop:
  if(not art.isrendered()):
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

 random.shuffle(total_pop)

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
 nec_tot =  sum([k.fitness for k in nectar_pop])
 nectarless_pop.sort(key=lambda k:k.fitness,reverse=True)
 nonec_tot = sum([k.fitness for k in nectarless_pop])
 ratio = float(nec_tot)/float(nonec_tot)
 print "nec:" , nec_tot
 print nectar_pop[0].mapped
 print "no nec:", nonec_tot
 print nectarless_pop[0].mapped
 print "ratio:" , ratio
 print critic_pop[0]
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

 if(gen%cycle_len==0):
  if(cycle==ART):
   cycle=CRITIC
  else:
   cycle=ART

 if(cycle==CRITIC):
  print "critic reproduction"
  critic_pop = create_new_pop_gen(critic_pop,0.3)
 else:
  print "artist reproduction"
  #migration
  new_migrate=migrate
  if(ratio>2):
   new_migrate*=10
  if random.random()<new_migrate:
   print "migrating..."
   for k in range(migrate_count):
    del nectarless_pop[-1]
   for k in range(migrate_count):
    nectarless_pop.insert(0,nectar_pop[k].copy())
    nectarless_pop[0].fitness=100000
  #new pops
  nectar_pop = create_new_pop_gen(nectar_pop,0.3)
  nectarless_pop = create_new_pop_gen(nectarless_pop,0.3)

for k in art_pop:
 del k
for k in critic_pop:
 del k
gc.collect()
