import math
import mazepy
import array
import random
from collections import defaultdict
import sys
fname=sys.argv[1]

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


solved=False

def to_grid(x):
 return int(x/10)

def insert_new_robot(x,grid):
 global solved
 x.map()
 if(x.solution()):
	solved=True
 coord=(to_grid(x.get_x()),to_grid(x.get_y()))
 if(len(grid[coord])<1): 
  grid[coord].append(x)

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
fit_dict={}
for k in dists.keys():
 if target in dists[k]:
  fitness_table.append((-dists[k][target],k))
  fit_dict[k]=-dists[k][target]
fitness_table.sort()
(fit,rank)=zip(*fitness_table)
rank=list(rank)

grid=defaultdict(list)

 
mx_fit=-10000000
evals=0

import pylab
import matplotlib
from matplotlib.patches import CirclePolygon
pylab.ion()
 
evals=0
robot=mazepy.mazenav()
for k in range(5):
 robot.init_rand()
 robot.previous=None
 insert_new_robot(robot,grid)

while evals<75000 and not solved:
 evals+=1
 if evals%1000==0:
  print evals,mx_fit
 
 #inject fresh meat
 if(random.random<0.05):
  robot=mazepy.mazenav()
  robot.init_rand()
  robot.previous=None
  insert_new_robot(robot,grid)
 else:
  cur_keys = grid.keys()
  #choose what niche to sample and perturb
  niche_coord=random.choice(cur_keys)
  for x in xrange(5):
   second_coord=random.choice(cur_keys)
   if fit_dict[second_coord]>fit_dict[niche_coord]:
    niche_coord=second_coord
  f= ((niche_coord[0]-target[0])**2+(niche_coord[1]-target[1])**2)
  if -f>mx_fit:
   mx_fit=-f
  #if fit_dict[niche_coord]>mx_fit:
  # mx_fit=fit_dict[niche_coord]
  niche=grid[niche_coord]
  robot=random.choice(niche)
  newbot = robot.copy()
  newbot.mutate()
  insert_new_robot(newbot,grid)

a=open(fname,"w")
a.write(str(evals))
