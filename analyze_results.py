import hyperneat
from art_basics import *
import evolve_to
from viewer import histogram,load_hist,observe,translate
import math

def load_maps(fname):
 lines=open(fname).read().split("\n")[:-1]
 return [[float(l) for l in k.split()] for k in lines]

#fn_temp = "res/artrand/run%d/generation%d/arc_behaviorlist"
#ofn_temp = "res/artrand/run%d/generation%d/arc_raritylist"
fn_temp = "res/artnov/run%d/generation%d/arc_behaviorlist"
ofn_temp = "res/artnov/run%d/generation%d/arc_raritylist"
hist = load_hist()

import random
sample_dict=dict()

for g in range(100,750,50):
 avg=[]
 sample_dict[g]=[]
 for r in range(15):
  ofn=open(ofn_temp%(r,g),"w")
  fn=fn_temp%(r,g)
  #print fn
  load=load_maps(fn)
  t=0.0
  for k in load:
   (x,f)=observe(k,hist)
   sample_dict[g].append((x,f))
   f=translate(f)
   t+=math.log(x)
   ofn.write(str(math.log(x))+" "+str(f)+"\n")
  avg.append(t/len(load))
 print g,sum(avg)/len(avg)

samples=dict()
sample_size=200
for g in range(100,600,100):
 #samples[g]=[]
 #for k in range(sample_size):
 # samples[g].append(random.choice(sample_dict[g]))
 samples[g]=random.sample(sample_dict[g],sample_size)
import pickle
a=open("samples.dat","w")
pickle.dump(samples,a)

