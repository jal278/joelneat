import mazepy
import array
from collections import defaultdict

mazepy.mazenav.initmaze("medium_maze_list.txt")

def defint():
 return defaultdict(int)

transition_table=defaultdict(defint)
grid=defaultdict(list)
sampled=defaultdict(int)
solved=False

def to_grid(x):
 return int(x/10)

def insert_new_robot(x,grid):
 global solved
 x.map()
 coord=(to_grid(x.get_x()),to_grid(x.get_y()))
 if(x.solution()):
  solved=True
  print coord,x.history
  x.save("solution.dat")
 if(len(grid[coord])<1): 
  grid[coord].append(x)
 #else:
 # grid[coord].pop()
 # grid[coord].insert(0,x)
 if (x.previous):
  prev_c = x.previous
  new_c = coord
  transition_table[prev_c][new_c]+=1
 
evals=0
robot=mazepy.mazenav()
robot.init_rand()
robot.previous=None
robot.history=[]
insert_new_robot(robot,grid)

import random
import pylab
import matplotlib
pylab.ion()

def draw_links():
  global grid,transition_table
  cur_keys=grid.keys()

  pylab.clf()
  x,y=zip(*cur_keys)
  pylab.plot(x,y,"o")
  axes=pylab.gca()
  for key in cur_keys:
   robot=grid[key][0]
   if(robot.previous):
     prev=robot.previous
     dx=key[0]-prev[0]
     dy=key[1]-prev[1]
     axes.arrow(prev[0],prev[1],dx,dy,head_width=0.3,head_length=0.5)
  pylab.draw()

def draw_table():
  global grid,transition_table
  cur_keys=grid.keys()

  pylab.clf()
  x,y=zip(*cur_keys)
  pylab.plot(x,y,"o")
  line_segs=[]
  colors=[]
  for key in transition_table:
   tot=0
   temp_colors=[]
   for dest in transition_table[key]:
     line_segs.append((key,dest))
     v=transition_table[key][dest]
     tot+=v
     temp_colors.append(v)
   for n in temp_colors:
    colors.append((1,0,0,float(v)/tot))
  lc = matplotlib.collections.LineCollection(line_segs,colors=colors)
  axes=pylab.gca()
  axes.add_collection(lc)
  pylab.draw()
  print evals,len(cur_keys)

import sys
fname=sys.argv[1]
mx_fit=-100000
while evals<30000: #and not solved:
 evals+=1
 
 if(evals%1000==0):
  print evals,solved
  #draw_table()
  #draw_links()

 #inject fresh meat
 if(random.random<0.05):
  robot=mazepy.mazenav()
  robot.init_rand()
  robot.previous=None
  robot.history=[]
  insert_new_robot(robot,grid)
 else:
  cur_keys = grid.keys()
  #choose what niche to sample and perturb
  niche_coord=random.choice(cur_keys)
  for x in xrange(5):
   second_coord=random.choice(cur_keys)
   if sampled[second_coord]<sampled[niche_coord]:
    niche_coord=second_coord

  sampled[niche_coord]+=1
  niche=grid[niche_coord]
  robot=random.choice(niche)
  newbot = robot.copy()
  newbot.mutate()
  newbot.previous = niche_coord
  newbot.history=robot.history[:]
  newbot.history.append(niche_coord)
  insert_new_robot(newbot,grid)

if(True):
 histories={}
 for k in grid:
  for a in grid[k]:
   histories[k]=a.history
 import cPickle as p
 a=open(fname+".tt","wb")
 p.dump(transition_table,a)
 a=open(fname+".hist","wb")
 p.dump(histories,a)
else:
 a=open(fname,"w")
 a.write(str(evals))
