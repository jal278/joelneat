import hyperneat
from art_basics import *

hyperneat.artist.random_seed()
direc="coev2"

critic = critic_class.load(direc+"/generation1000/crit0")

population=[]
for k in range(200):
 population.append(hyperneat.artist())

class Speciator:
 def __init__(self,threshold,target):
  self.threshold=threshold
  self.species=[]
  self.species_dir=dict()
  self.target=target

 def add_new_species(self,ind):
  self.species.append([ind,])
  self.species_dir[ind]=self.species[-1]

 def add_to_species(self,ind,species):
  species.append(ind)
  self.species_dir[ind]=species

 def speciate(self,population):
  self.species=[]
  self.species_dir=dict()
  
  for k in population:
   k.raw_fitness=k.fitness
   found=False
   for s in self.species:
    if s[0].distance(k)<self.threshold:
     self.add_to_species(k,s)
     found=True
     break
   if not found:
    self.add_new_species(k)
   
  #sort species by fitness to get easy access to champs
  #then normalize fitness by species size 
  for s in self.species:
   s.sort(key=lambda k:k.fitness,reverse=True)
   spec_size = len(s)
   for ind in s:
    ind.fitness/=spec_size
  
  if len(self.species)<self.target:
   self.threshold*=0.9
  elif len(self.species)>self.target:
   self.threshold*=1.1
  
  print "species: ", len(self.species)

speciator = Speciator(20.0,5)

gen=0
while(True):
 for k in population:
  k.render_picture()
  k.fitness =  critic.evaluate_artist(k)
 max_fit = max([k.fitness for k in population])
 print gen, max_fit 
 #speciator.speciate(population)
 population = create_new_pop_gen(population,0.3)
 gen+=1

