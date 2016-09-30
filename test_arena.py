import mazepy
mazepy.arenaorg.random_seed()
mazepy.arenaorg.init()
pop=[]

for x in range(50):
 new_art = mazepy.arenaorg()
 """
 new_art.init_rand()
 new_art.mutate()
 new_art.mutate()
 new_art.mutate()
 """
 new_art.load_new("seed")
 pop.append(new_art)

import random

gen=0

def fitness(x):
 x.map()
 x.fitness=mazepy.arena_feature_detector.total_constructed(x)

best=None
best_scr=-1

while gen<150:
 gen+=1
 for x in pop:
  fitness(x)
 fitnesses=[x.fitness for x in pop]
 best_scr=max(fitnesses)
 best=pop[fitnesses.index(best_scr)]
 print "max:",best_scr
 pop.sort(key=lambda x:x.fitness,reverse=True)
 new_pop=[]
 pop=pop[:10]
 new_pop.append(best.copy())
 best.save("bestbrain.txt")
 for x in range(100):
  new=random.choice(pop).copy()
  new.mutate()
  new_pop.append(new)
 pop=new_pop
best.print_structure()
