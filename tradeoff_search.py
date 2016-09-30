import os
from optparse import OptionParser
parser=OptionParser()
parser.add_option("-o","--output",dest="output")
parser.add_option("-s","--seed",dest="seed")
parser.add_option("-t","--type",dest="type")
(options,args)=parser.parse_args()

arch_pop=[]
art_pop=[]

dname = options.output
print_interval=500
record_interval=500
os.system("mkdir %s" % dname)

from art_basics import *
from viewer import make_choices
import random
import mazepy
import array
from collections import defaultdict

eval_no=0
mazepy.mazenav.random_seed()
mazepy.mazenav.initmaze("hard_maze_list.txt")
nov_mapper=mazenav_novelty_mapper
mapper=nov_mapper()

if(options.seed!=None):
  print "seed:" + options.seed
  mazepy.mazenav.seed(int(options.seed))

proto=[(0,1),2,3,4,5]
granularities=[20,20,20,3,20,20]

class storage_grid:
 def map_to(self,pt):
  ret=[]
  cnt=0
  for k in self.features:
   v=int(pt[k]/self.delta[cnt])
   v=min(v,self.gran[cnt]-1)
   ret.append(v)
   cnt+=1
  return tuple(ret)
 def __init__(self,features,proto,granularities):
  features_exp=[]
  self.discovered=[]
  for k in features:
   if isinstance(proto[k],int):
    features_exp.append(proto[k])
   else:
    features_exp+=proto[k]
  self.features=features_exp
  self.gran=[]
  self.delta=[]
  self.prior=1.0

  for k in features_exp:
   self.gran.append(granularities[k])
   self.delta.append(1.0/granularities[k])
   self.prior/=granularities[k]

  #print features_exp
  #print self.gran 
  self.db=defaultdict(list) #numpy.zeros(self.gran)

 def get_most_recent(self,cnt):
  ret=[]
  for (key,x) in self.discovered[-cnt:]:
   ret.append(random.choice(self.db[key]))
  return ret

 def sample(self):
  sz=10000
  best=None
  #favor less-sampled niches
  for z in xrange(10):
   key=random.choice(self.db.keys())
   n_sz=len(self.db[key])
   if(n_sz<sz):
    sz=n_sz
    best=key

  return random.choice(self.db[best])

 def insert(self,indiv,pt):
  global eval_no
  index=self.map_to(pt)
  freq=len(self.db[index])
  if(freq<5):
   if(freq==0):
    self.discovered.append((index,eval_no)) 
   self.db[index].append(indiv)

 def get_freq(self,pt):
  index=self.map_to(pt)
  return len(self.db[index])

def collect_recent(n,grids):
 ret=[]
 for k in grids:
  ret+=k.get_most_recent(n)
 return ret

def insert_new_robot(x,grids):
 global solved
 x.map()
 behavior=mapper.evaluate_artist(x)
 x.behavior=behavior
 for grid in grids:
  coord=grid.map_to(behavior)
  grid.insert(x,behavior)

grids=[]
feature_set=[]
for k in range(1,4):
 feature_set+=make_choices(k,len(proto))

for z in feature_set:
 sz=len(z)
 gran_scaled=[max(3,k/sz) for k in granularities]
 grids.append(storage_grid(z,proto,gran_scaled))

evals=0
robot=mazepy.mazenav()
robot.init_rand()
pop_size=250
evals=pop_size*2000+1

insert_new_robot(robot,grids)
for eval_no in range(evals):
 to_perturb=random.choice(grids).sample()
 newbot = to_perturb.copy()
 newbot.mutate()
 insert_new_robot(newbot,grids)

 #recording code
 if (eval_no%(20*pop_size)==0):
  arch_pop+=collect_recent(1,grids)
  print eval_no,sum([len(k.db.keys()) for k in grids])
 if (eval_no%(print_interval*pop_size)==0):
  art_pop=collect_recent(10,grids)
  if(eval_no%(record_interval*pop_size)==0):
   directory="%s/generation%d"%(dname,eval_no/pop_size)
   os.system("mkdir %s" % directory)
   afname = directory+"/art%d"
   arcname = directory+"/arc%d"
   if(eval_no%print_interval==0):
    save_pop(arch_pop,arcname)
    save_pop_behaviors(arch_pop,directory+"/arc_behaviorlist" )
    save_pop(art_pop,afname)
    save_pop_behaviors(art_pop,directory+"/pop_behaviorlist" )
