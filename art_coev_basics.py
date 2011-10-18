import hyperneat
from art_basics import *

def create_flowers(size):
 nectar_pop=[]
 nectarless_pop=[]
 for k in range(size):
  new_art=hyperneat.artist()
  new_art.fitness=0
  nectar_pop.append(new_art)
  new_art=hyperneat.artist()
  new_art.fitness=0
  nectarless_pop.append(new_art)
 return nectar_pop,nectarless_pop

def create_critics(size): 
 critic_pop=[]
 for k in range(size):
   new_critic=critic_class()
   new_critic.fitness=0
   critic_pop.append(new_critic)
 return critic_pop

def save_pop(pop,fname):
 count=0
 for k in pop:
  k.save(fname%count)
  count+=1

def load_pop(fn,size,cname):
 pop=[]
 for k in range(size):
  pop.append(cname.load(fn%k))
 return pop

