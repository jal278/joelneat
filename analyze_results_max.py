import hyperneat
from art_basics import *
import evolve_to
from viewer import histogram,load_hist,observe,translate
import math

def load_maps(fname):
 lines=open(fname).read().split("\n")[:-1]
 return [[float(l) for l in k.split()] for k in lines]

#fn_temp = "res/trade%d/generation%d/arc_behaviorlist"
#ofn_temp = "res/trade%d/generation%d/arc_raritylist"
fn_temp = "res/trade%d/generation%d/pop_behaviorlist"
ofn_temp = "res/trade%d/generation%d/pop_raritylist"
#fn_temp = "res/nov%d/generation%d/pop_behaviorlist"
#ofn_temp = "res/nov%d/generation%d/pop_raritylist"
#fn_temp = "res/nov%d/generation%d/arc_behaviorlist"
#ofn_temp = "res/nov%d/generation%d/arc_raritylist"
#fn_temp = "res/rand%d/generation%d/pop_behaviorlist"
#ofn_temp = "res/rand%d/generation%d/pop_raritylist"
hist = load_hist()

import random
sample_dict=dict()

#for g in range(50,2050,50):
for g in range(500,2500,500):
 avg=[]
 for r in [0,1,10,11]: #range(20):
  sample_dict[(g,r)]=[]
  ofn=open(ofn_temp%(r,g),"w")
  fn=fn_temp%(r,g)
  #print fn
  load=load_maps(fn)
  t=100.0
  for k in load:
   (x,f)=observe(k,hist)
   sample_dict[(g,r)].append((x,f))
   f=translate(f)
   if(x>0):
    x=math.log(x)
   else:
    x-=18.0
   t=min(t,x)
   ofn.write(str(x)+" "+str(f)+"\n")
  avg.append(t)
 print g,sum(avg)/len(avg)

"""
samples=dict()
sample_size=800
for g in range(0,550,50):
 for r in range(40):
  sample_dict[(g,r)].sort()
  samples[(g,r)]=sample_dict[(g,r)][:40]
  #print (g,r),sample_dict[(g,r)][:5]
 #random.sample(sample_dict[g],sample_size)

#import pickle
#a=open("randsamples.dat","w")
#pickle.dump(samples,a)
"""

