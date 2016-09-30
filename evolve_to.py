import hyperneat
from art_basics import *

class target_critic:
 def __init__(self,targets,dist):
  self.dist=dist
  self.sq_d=self.dist**2
  self.targets=targets
  self.mapper=novelty_mapper() 
 def compare_vec(self,img):
  features = self.mapper.evaluate_artist(img)
  tvec=[]
  ivec=[]
  sqd=[]
  for k in self.targets:  
   ivec.append(features[k])
   tvec.append(self.targets[k]) 
   sqd.append((features[k]-self.targets[k])**2)
  #print ivec
  #print tvec
  #print sqd
 def evaluate_artist(self,img):
  features = self.mapper.evaluate_artist(img)
  success=True
  error=0
  for k in self.targets:   
   #print features[k],self.targets[k]
   sq_d = (features[k]-self.targets[k])**2
   if(sq_d>self.sq_d):
    success=False
   error -= sq_d
 
  if(success):
    return 0.0
  else:
    return error

def neatclimb(trials,critic,target,popsize):
 population=[]
 for k in range(popsize):
  population.append(hyperneat.artist())
 evals=0
 max_fit=-1000
 gen=0
 speciator = Speciator(20.0,5)
 while(evals<trials and max_fit<0):
  best=None
  max_fit=-10000
  for k in population:
   k.render_picture()
   k.fitness =  critic.evaluate_artist(k)
   k.raw_fitness =  k.fitness # critic.evaluate_artist(k)
   if(k.fitness>max_fit):
    max_fit=k.fitness
    best=k
  #print gen, max_fit,len(speciator.species)
  critic.compare_vec(best)
  speciator.speciate(population)
  evals+=popsize
  population = create_new_pop_gen(population,0.3)
  gen+=1
 return evals

def hillclimb(trials,critic,target):
 starter = hyperneat.artist()
 starter.render_picture()
 fitness = critic.evaluate_artist(starter)
 trial=0
 print fitness
 while(trial<trials and fitness<target):
  offspring = make_new(starter)
  offspring.render_picture()
  nfit = critic.evaluate_artist(offspring)
  if(nfit>fitness):
   print nfit,target
   fitness=nfit
   starter=offspring
  trial+=1
 print trial
 return trial,fitness

def evolve_to(feature):
 crit = target_critic(feature,0.05)
 return neatclimb(25000,crit,0,100)
