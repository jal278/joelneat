import os
import hyperneat
import random

import gc
from art_basics import *
from art_coev_basics import *

render=False
screen,background=None,None
if(render):
 import pygame

#PYGAME SETUP
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

direc="test"
nectar_pop,nectarless_pop,critic_pop= ([],[],[])

critic_pop_size=200
flower_pop_size=200
speciation=True
critic_speciator=Speciator(2.0,8)
nectar_speciator=Speciator(20.0,8)
nectarless_speciator=Speciator(20.0,8)

if(False):
 load_dir=direc+"/generation800/"
 nectar_pop=load_pop(load_dir+"nart%d",flower_pop_size,hyperneat.artist)
 nectarless_pop=load_pop(load_dir+"art%d",flower_pop_size,hyperneat.artist)
 critic_pop=load_pop(load_dir+"crit%d",critic_pop_size,critic_class)
else:
 nectar_pop,nectarless_pop = create_flowers(flower_pop_size)
 critic_pop = create_critics(critic_pop_size)

bestcount=20
critic_best=critic_pop[:bestcount]
best_art=nectar_pop[:bestcount]+nectarless_pop[:bestcount]
gen=0
migrate=0.0 #0.01
migrate_count=3
cycle_len=1
ART=0
CRITIC=1
cycle=CRITIC

while(True):
 print "generation:" ,gen
 gen+=1

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

 if(cycle==CRITIC):
  for crit in critic_pop:
   crit.fitness=0.0


 #random.shuffle(critic_best)
 if(cycle==ART):
  total_pop=nectar_pop+nectarless_pop
  random.shuffle(total_pop)
  for crit in critic_best:
   ranks=[]
   fits=[]
   for art in total_pop:
    fit=crit.evaluate_artist(art)
    fits.append((fit,art.nectar))
   ranks=zip(fits,range(len(total_pop)))
   ranks.sort()
   a,ranks=zip(*ranks)
 
   for k in range(len(total_pop)):
    art = total_pop[ranks[k]]
    art.fitness+=k
 
  for art in total_pop:
   if(art.get_nanflag()):
    art.fitness = -100.0
    art.clear_picture()

  nectar_pop.sort(key=lambda k:k.fitness,reverse=True)
  nectarless_pop.sort(key=lambda k:k.fitness,reverse=True)
  best_art=nectar_pop[:bestcount]+nectarless_pop[:bestcount]

 if(cycle==CRITIC):
  random.shuffle(best_art)
  #now to calculate fitnesses for artists and critics
  for crit in critic_pop:
   fits=[]
   for art in best_art:
    fit=crit.evaluate_artist(art)
    fits.append((fit,art.nectar))
   ranks=zip(fits,range(len(best_art)))
   ranks.sort()
   count=0
   for k in ranks:
    if k[0][1]==1:
     crit.fitness+=count
    else:
     crit.fitness-=count
    count+=1 

  #extract best critics for next round
  critic_pop.sort(key=lambda k:k.fitness,reverse=True)
  critic_best = critic_pop[:bestcount] 
 
 if(cycle==ART):  
  nectar_pop.sort(key=lambda k:k.fitness,reverse=True)
  nec_tot =  sum([k.fitness for k in nectar_pop])
  nectarless_pop.sort(key=lambda k:k.fitness,reverse=True)
  nonec_tot = sum([k.fitness for k in nectarless_pop])
  ratio = float(nec_tot)/(float(nonec_tot)+0.000000001)
  print "---"
  print "nec:" , nec_tot
  print nectar_pop[0].mapped
  print "no nec:", nonec_tot
  print nectarless_pop[0].mapped
  print "ratio:" , ratio
 if(cycle==CRITIC): 
  print "Crit best:" , critic_best[0].fitness
  print critic_best[0]

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

 if(cycle==CRITIC):
  print "critic reproduction"
  if(speciation):
   critic_speciator.speciate(critic_pop)
  critic_pop = create_new_pop_gen(critic_pop,0.5)
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
  if(speciation):
   nectar_speciator.speciate(nectar_pop)
   nectarless_speciator.speciate(nectarless_pop)

  nectar_pop = create_new_pop_gen(nectar_pop,0.5)
  nectarless_pop = create_new_pop_gen(nectarless_pop,0.5)
 
 if(gen%cycle_len==0):
  if(cycle==ART):
   cycle=CRITIC
   continue
  else:
   cycle=ART
   continue
