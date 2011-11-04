import hyperneat
from art_basics import *

def create_flowers(size,num):
 pops=[]
 for j in range(num):
  tpop=[]
  for k in range(size):
   new_art=hyperneat.artist()
   new_art.fitness=0
   tpop.append(new_art)
  pops.append(tpop)
 return pops

def create_critics(size): 
 critic_pop=[]
 for k in range(size):
   new_critic=critic_class()
   new_critic.fitness=0
   critic_pop.append(new_critic)
 return critic_pop

