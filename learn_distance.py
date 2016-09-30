import math
import mazepy
import array
from collections import defaultdict


def defint():
 return defaultdict(int)

def to_grid(x):
 return int(x/10)

import cPickle as p
import glob

files=glob.glob("z*.tt")
transition_table=dict()

def normalize_table(t):
 for i in t:
  tot=0
  for j in t[i]:
   tot+=t[i][j]
  tot=float(tot)
  for j in t[i]:
   t[i][j]/=tot

def merge_table(a1,a2):
 for k in a2:
  if k not in a1:
   a1[k]=a2[k]
  else:
   for k2 in a2[k]:
    if k2 not in a1[k]:
     a1[k][k2]=a2[k][k2] 
    else:
     a1[k][k2]+=a2[k][k2] 

transition_table={}
for k in files:
 a=open(k,"rb")
 new_table=p.load(a)
 normalize_table(new_table)
 merge_table(transition_table,new_table)
normalize_table(transition_table)

rarity=defaultdict(int)
for state in transition_table:
 for dest in transition_table[state]:
  rarity[dest]+=transition_table[state][dest]

rarity_list=[(rarity[k],k) for k in rarity]
rarity_list.sort()
rare_states=[k[1] for k in rarity_list[:50]]

import networkx as nx

G=nx.DiGraph()

for key in transition_table:
   tot=0
   for dest in transition_table[key]:
     v=transition_table[key][dest]
     tot+=v
   for dest in transition_table[key]:
    v=transition_table[key][dest]
    G.add_edge(key,dest,weight=(tot/float(v)))

paths=nx.all_pairs_dijkstra_path(G)
dists=nx.all_pairs_dijkstra_path_length(G)

results_dict=dict()
results_dict["paths"]=paths
results_dict["dists"]=dists

import cPickle as p
a=open("maze_dist.out","wb")
p.dump(results_dict,a)

import pylab
import matplotlib
from matplotlib.patches import CirclePolygon

pylab.clf()

colors=[]
line_segs=[]
states=transition_table.keys()
target=(3,2)
for source in [(3,17)]: # states:
  for dest in [target,]:
     if source==dest:
	continue
     if source in paths and dest in paths[source]:
      line_segs.append(paths[source][dest])
      colors.append((1.0,0.0,0.0,0.3))
lc = matplotlib.collections.LineCollection(line_segs,colors=colors)
axes=pylab.gca()
axes.set_xlim(0,20)
axes.set_ylim(0,20)

for key in transition_table.keys():
 if target in dists[key]:
  print key
  sz=dists[key][target] #math.log(rarity[key]+1)/10
  print sz
  size=(sz+100.0)/5000
  axes.add_artist(pylab.Circle(key,size))

axes.add_collection(lc)

pylab.draw()
pylab.show()
