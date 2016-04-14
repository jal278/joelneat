import hyperneat
import random
import numpy
import pygame
from pygame.locals import *
from art_basics import *
import ad

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

def render_picture(x,y,data):
 global render,screen,background,SX,SY
 if(not render):
  return
 data.render("image0.png")
 im=pygame.image.load("image0.png")
 imagerect=(x,y) #im.get_rect()
 background.blit(im,imagerect)
 """
 for xc in range(SX):
  for yc in range(SY):
   px=int ( (data[xc][yc])*256)
   px=min(px,255)
   px=max(px,0)
   pygame.draw.circle(background, (px,px,px), (x+xc*pxsize,y+yc*pxsize),pxsize,0)
 """

def render_artist(x,y,pxsize,artist):
 global render,screen,background,SX,SY
 if(not render):
  return
 render_picture(x,y,artist)
 
a=hyperneat.artist()
a.random_seed()
artists = []
nov_crit = novelty_mapper()

import sys
popsize=9
speciator = Speciator(5.0,8)


def gen_novelty(indiv,num):
 art_pop=[]
 for k in range(100):
  n=make_new(indiv)
  art_pop.append(n)

 for art in art_pop:
   art.render_picture()
   art.fitness=0.0
   art.ranks=[]
   art.behavior=numpy.array(nov_crit.evaluate_artist(art))
   if(art.get_nanflag() or not art.get_valid()):
	  art.behavior[:]=0.0
 for art in art_pop:
   if(art.get_nanflag() or not art.get_valid()):
    art.fitness = -100.0
    art.clear_picture()
    art_pop.remove(art)
    continue
   else:
    art.fitness=[sum((art.behavior-x.behavior)**2) for x in [indiv]]
    art.fitness=art.fitness[0]
    art.raw_fitness = art.fitness
 indivs=[]
 art_pop.sort(key=lambda x:x.fitness)
 for k in range(num):
  idx=int(float(k)*len(art_pop)/num)
  indivs.append(art_pop[idx])
 return indivs

#want to be able to do novelty search during
#interactive evolution so that user choice points
#are more efficiently exploited
def do_novelty(indiv,archive,speciator):
 art_pop=[]
 for k in range(100):
  n=make_new(indiv)
  art_pop.append(n)

 for g in range(10):
  for art in art_pop:
   art.render_picture()
   art.fitness=0.0
   art.ranks=[]
   art.behavior=numpy.array(nov_crit.evaluate_artist(art))
   print art.behavior
   if(art.get_nanflag() or not art.get_valid()):
	  art.behavior[:]=0.0
  for art in art_pop:
   if(art.get_nanflag() or not art.get_valid()):
    art.fitness = -100.0
    art.clear_picture()
   else:
    art.dists=[sum((art.behavior-x.behavior)**2) for x in art_pop]
    arch_dists=[sum((art.behavior-x.behavior)**2) for x in archive]
    arch_dists.sort()
    if(len(arch_dists)<2 or random.random()<0.01): #arch_dists[1]>archive_threshold):
     archive.append(art)

    art.dists+=arch_dists
    art.dists.sort()
    art.fitness = sum(art.dists[:20])   
    art.raw_fitness = art.fitness

  speciator.speciate(art_pop)
  art_pop.sort(key=lambda k:k.raw_fitness,reverse=True)
  print "maxf:", art_pop[0].raw_fitness 
  art_pop = create_new_pop_gen(art_pop,0.3)
  

if len(sys.argv)>1:
 a=hyperneat.artist.load(sys.argv[1])
 for k in range(popsize):
  n=make_new(a)
  n.fitness=0
  n.render_picture()
  n.behavior=numpy.array(nov_crit.evaluate_artist(n))
  artists.append(n)
else: 
 for k in range(popsize):
  n = ad.ad_genome() #hyperneat.artist()
  n.fitness=0
  n.gen="orig"
  artists.append(n)

novgen=False
quit=False
render_art=True
choices=[]
while(not quit):
 print choices
 gs=3
 #if(optimize):
  #for z in xrange(50):
  #cur_obj.artists[0].optimize(dummy)
   #cur_obj.artists[k].optimize(cur_obj.critic)
 for k in range(popsize):
  if(render_art):
   render_artist(25+(k%gs)*230,25+(k/gs)*230,PXS,artists[k])
   #print k,artists[k].behavior,((artists[k].behavior-artists[0].behavior)**2).sum()
 if(render):
  screen.blit(background,(0,0))
  pygame.display.flip()
 background.fill((0, 0, 255))
 for event in pygame.event.get():
  if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
   quit=True
  elif event.type==KEYDOWN:
   if(event.key==K_n):
    novgen=not novgen
   elif(event.key>=K_0 and event.key<=K_9):
    artist = artists[event.key-K_1]
    choices.append(artist.gen)
    if(novgen):
     artists=gen_novelty(artist,6)
     for k in artists:
      k.gen="nov"
     for k in range(3):
      n=make_new(artist)
      n.fitness=1.0
      n.render_picture()
      n.behavior=numpy.array(nov_crit.evaluate_artist(n))
      n.gen="reg"
      artists.append(n)
     random.shuffle(artists)
    else:
     artists=[]
     for k in range(popsize):
      n=make_new(artist)
      n.fitness=1.0
      n.gen="reg"
      artists.append(n)
    
   elif(event.key==K_s):
    objectives=[]
    for k in range(10):
     print "creating objective ",k
     newobj=make_new(cur_obj)
     newobj.evaluate()
     newobj.evolve()
     objectives.append(newobj)

