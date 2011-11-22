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

def bee_create_critics(size,count): 
 critic_pops=[]
 for j in range(count):
  critic_pop=[]
  for k in range(size):
   new_critic=critic_class()
   new_critic.fitness=0
   new_critic.nectar=j
   critic_pop.append(new_critic)
  critic_pops.append(critic_pop)
 return critic_pops

def add_new_pops(fpop,fsize,cpop,csize):
 newc = create_critics(csize)
 for k in newc:
  k.nectar=len(cpop)
 cpop.append(newc)

 newf = create_flowers(fsize,1)[0]
 for k in newf:
  k.nectar=len(fpop)
 fpop.append(newf)
