numeric=False

if(numeric):
 import Numeric as numpy
else:
 import numpy

import os
import sys
import hyperneat
import random
import evolve_to
from art_basics import *

render=True

screen,background=None,None

def save_pop_behaviors(pop,fname):
 outstr=""
 for k in pop:
  vals = k.behavior
  outstr += " ".join(map(str,vals))+"\n"
 out = open(fname,"w")
 out.write(outstr)

if(render):
 import pygame
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
if(len(sys.argv)>2):
 print "seeding..."
 hyperneat.artist.seed(int(sys.argv[2]))

target_critic=None
randfit=False
targetfit=False
if(len(sys.argv)>3):
 if (sys.argv[3]=="rand"):
  print "random"
  randfit=True 
 elif(len(sys.argv)>3):
  print "target"
  target_fn = sys.argv[3]
  target=pickle.load(open(target_fn,"rb"))
  target_critic=evolve_to.target_critic(target[1],0.05)
  targetfit=True

art_pop = []

maze=False

nov_crit = novelty_mapper()
if(maze):
 nov_crit = maze_novelty_mapper()

pop_size = 250
speciator = Speciator(5.0,8)

for k in range(pop_size):
 new_art=hyperneat.artist()
 new_art.fitness=0
 art_pop.append(new_art)

gen=0

archive=[]
archive_threshold = 0.5
archive_add_count=0
archive_freeze_count=0
dname = sys.argv[1]

os.system("mkdir %s" % dname)
while(True):
 archive_add_count=0
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
  if(art.get_nanflag() or not art.get_valid()):
   art.fitness = -100.0
   art.clear_picture()
  else:
   art.dists=[sum((art.behavior-x.behavior)**2) for x in art_pop]
   arch_dists=[sum((art.behavior-x.behavior)**2) for x in archive]
   arch_dists.sort()
   if(len(arch_dists)<2 or arch_dists[1]>archive_threshold):
    archive.append(art)
    archive_add_count+=1

   art.dists+=arch_dists
   art.dists.sort()
   art.fitness = sum(art.dists[:20])   
   art.raw_fitness = art.fitness
  if randfit:
   art.fitness = random.random()*100.0
   art.raw_fitness=art.fitness
  if targetfit: 
   art.fitness = target_critic.evaluate_artist(art)
   art.raw_fitness = art.fitness
 #adjust archive threshold
 print "Archive size: ", len(archive), " threshold: ", archive_threshold 
 if(archive_add_count>4):
  archive_threshold*=1.3
 
 if(archive_add_count==0):
  archive_freeze_count+=1
  if(archive_freeze_count>=7):
   archive_freeze_count=0
   archive_threshold*=0.85
 else:
  archive_freeze_count=0

 speciator.speciate(art_pop)
 art_pop.sort(key=lambda k:k.raw_fitness,reverse=True)
 
 if(render):
  gs=4
  for k in range(16):
   render_picture(25+(k%gs)*180,25+(k/gs)*180,PXS,art_pop[k].get_picture())
  screen.blit(background,(0,0))
  pygame.display.flip()

 if((gen)%50==0):
  #if((gen)==1000):
  directory="%s/generation%d"%(dname,gen)
  os.system("mkdir %s" % directory)
  afname = directory+"/art%d"
  if(gen%500==0):
   save_pop(art_pop,afname)
   save_pop(archive,directory+"/archive%d")
  save_pop_behaviors(archive,directory+"/arc_behaviorlist" )
  save_pop_behaviors(art_pop,directory+"/pop_behaviorlist" )
  if(gen==1500):
   break
 art_pop = create_new_pop_gen(art_pop,0.3)
