import hyperneat
from art_basics import *

hyperneat.artist.random_seed()
direc="coev2"

critic = critic_class.load(direc+"/generation1000/crit0")

population=[]
for k in range(200):
 population.append(hyperneat.artist())

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

