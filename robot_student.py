import math
import mazepy
import array
import random
from collections import defaultdict


#render distance function
def plot_pop(population):
 global rank
 pylab.clf()
 axes=pylab.gca()
 axes.set_xlim(0,20)
 axes.set_ylim(0,20)
 for key in dists.keys():
  if target in dists[key]:
   sz=dists[key][target] #math.log(rarity[key]+1)/10
   size=(rank.index(key))/float(500)
   axes.add_artist(pylab.Circle(key,size))
 for i in population:
  axes.add_artist(pylab.Circle(i.coord,1.0,color=(1,0,0,0.2)))
 pylab.draw()
 pylab.show()

def to_grid(x):
 return int(x/10)

import cPickle as p
a=open("maze_dist.out","rb")

results=p.load(a)

mazepy.mazenav.initmaze("hard_maze_list.txt")
mazepy.mazenav.random_seed()

robot=mazepy.mazenav()
robot.init_rand()
robot.mutate()
robot.previous=None
robot.map()
coord=(to_grid(robot.get_x()),to_grid(robot.get_y()))

target=(3,2)
dists=results["dists"]

fitness_table=[]
for k in dists.keys():
 if target in dists[k]:
  fitness_table.append((-dists[k][target],k))
fitness_table.sort()
(fit,rank)=zip(*fitness_table)
rank=list(rank)
population=[]

psize = 20
for k in xrange(psize):
 new=robot.copy()
 population.append(new)
  
mx_fit=-10000000
evals=0

import pylab
import matplotlib
from matplotlib.patches import CirclePolygon
pylab.ion()

mx_fit=-100000
while True:
 print mx_fit,evals
 for indiv in population:
  indiv.map()
  evals+=1
  indiv.coord=(to_grid(indiv.get_x()),to_grid(indiv.get_y()))
  if(indiv.coord==target):
   print "solved"
 
 plot_pop(population)
 tfit=0.0
 mx_fit=-100000
 for indiv in population:
  #if indiv.coord in dists and target in dists[indiv.coord]:
  # indiv.fitness= -dists[indiv.coord][target]
  #else:
  # indiv.fitness= -1000000
  indiv.fitness=rank.index(indiv.coord) #(indiv.coord[0]-target[0])**2+(indiv.coord[1]-target[1])**2
  tfit+=indiv.fitness
  if(indiv.fitness>mx_fit):
   mx_fit=indiv.fitness

 population.sort(key=lambda k:k.fitness)
 thresh=int((psize*4)/5.0)

 population=population[thresh:]
 new_population=[]
 for k in xrange(psize):
  new=None
  if k==0:
   new=population[-1].copy()
  else:
   new=random.choice(population).copy()
   if random.random()<0.6:
    new.mutate()
  new_population.append(new)
 population=new_population
 print tfit/psize
