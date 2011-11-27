import hyperneat
import random
import pickle

#class for speciation, normalizes fitness by species size
#TODO: does not handle species elitism yet though
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
  
  #print "species: ", len(self.species)



def herit_measure(h):
 h1,h2=zip(*h)
 return rankdist(get_ranks(h1),get_ranks(h2))

def create_rankings(vals):
 ranks=zip(vals,range(len(vals)))
 ranks.sort()
 a,ranks=zip(*ranks)
 return ranks
def rankdist(d1,d2):
 sz = len(d1)
 d = 0 
 for k in xrange(sz):
  d+=abs(d1[k]-d2[k])
 return d

def get_ranks(a1):
  ranks=zip(a1,range(len(a1)))
  ranks.sort()
  a,ranks=zip(*ranks)
  return ranks

class feature_critic_frozen:
 def __init__(self):
   pass
 def evaluate_artist(self,a):
   #avg=hyperneat.feature_detector.average(a) #chop(a,3)
   #avg= (hyperneat.feature_detector.compression(a) + hyperneat.feature_detector.wavelet(a))/2
   avg=hyperneat.feature_detector.symmetry_x(a)+hyperneat.feature_detector.symmetry_y(a)-hyperneat.feature_detector.compression(a)
   return avg
 def mutate(self):
   pass
 def copy(self):
   return feature_critic()
 def complexity(self):
   return 0.0
 def save(self,fn):
   pass
 def load(self,fn):
   pass

class novelty_mapper:
 def __init__(self):
  self.critic = feature_critic()
 def evaluate_artist(self,a):
  #return map(lambda k:k(a),self.features)
  return self.critic.map_all(a)

class feature_critic:  
 def __str__(self):
   string=""
   for k in range(len(self.active)):
    string+=str((self.features[self.active[k]],self.targets[k],self.weights[k]))+"\n"
   return string

 def distance(self,other):
   dist=0.0
   for k in range(len(self.features)):
    s_ind=o_ind=None
    if k in self.active:
     s_ind = self.active.index(k)
    if k in other.active:
     o_ind = other.active.index(k)
    if (s_ind==None and o_ind==None):
     pass
    elif (s_ind!=None and o_ind!=None): 
     dist+=abs(self.targets[s_ind]-other.targets[o_ind])
    else:
     dist+=1.0    
   return dist

 def __init__(self):
   self.names=["avg","compression","wavelet","std","sym_x","sym_y","chop"]
   self.features=[hyperneat.feature_detector.average,hyperneat.feature_detector.compression,hyperneat.feature_detector.wavelet,hyperneat.feature_detector.std,hyperneat.feature_detector.symmetry_x,hyperneat.feature_detector.symmetry_y,hyperneat.feature_detector.chop]
   self.active=[]
   self.weights=[]
   self.targets=[]
   self.add_feature()
 def add_feature(self):
   tries=5
   feature=None
   #make sure we are not duplicating an existing feature
   found=None
   for k in range(tries):
    feature = random.randint(0,len(self.features)-1)
    found=False
    for a in self.active:
     if a==feature:
      found=True
      break
    if found:
     continue
    else:
     break
   if found:
    return
   self.active.append(feature)
   self.targets.append(random.uniform(0.0,1.0))
   self.weights.append(random.uniform(0.0,3.0)) 

 def del_feature(self):
   if(len(self.active)>1):
    to_rem=random.randint(0,len(self.active)-1)
    del self.active[to_rem]
    del self.weights[to_rem]
    del self.targets[to_rem]

 def map_all(self,a):
  vals=[]
  for k in self.features:
   vals.append(k(a))
  a.mapped=vals
  return vals

 def evaluate_map(self,m):
   fit=0.0
   for k in range(len(self.active)):
    fit+= (1.0 - abs(m[self.active[k]]-self.targets[k]))*self.weights[k] 
   return fit
 def evaluate_all(self,a):
   return self.evaluate_artist(a)
 def evaluate_artist(self,a):
   vals=[]
   if not hasattr(a,'mapped'):
    vals=self.map_all(a)
   else:
    vals=a.mapped
   return self.evaluate_map(vals)

 def mutate_feature(self):
   to_mutate=random.randint(0,len(self.weights)-1)
   if(random.random()<0.5):
    self.weights[to_mutate]+=random.uniform(-0.2,0.2) 
    if(self.weights[to_mutate]>3.0):
     self.weights[to_mutate]=3.0
    if(self.weights[to_mutate]<0.01):
     self.weights[to_mutate]=0.01
   else:
    self.targets[to_mutate]+=random.uniform(-0.1,0.1)
    if(self.targets[to_mutate]>1.0):
     self.targets[to_mutate]=1.0
    if(self.targets[to_mutate]<0.0):
     self.targets[to_mutate]=0.0

 def mutate(self):
   if(random.random()<0.1):
    if(random.random()<0.75): #add new
     self.add_feature()
    else:
     self.del_feature()
   elif(random.random()<0.5):
     self.mutate_feature()
 def copy(self):
   new=feature_critic()
   new.weights=self.weights[:]
   new.active=self.active[:]
   new.targets=self.targets[:]
   return new
 def complexity(self):
   return len(self.active)
 def save(self,fn):
   a=open(fn,"w")
   pickle.dump(self,a)
 def load(self,fn):
   new=pickle.load(open(fn))
   self.weights=new.weights
   self.active=new.active
   self.targets=new.targets
 def to_string(self):
  return pickle.dumps(self)

 @staticmethod
 def load(fn):
  new=pickle.load(open(fn))
  return new

 @staticmethod
 def from_string(string):
   new=pickle.loads(string)
   return new

critic_class = feature_critic
#critic_class = hyperneat.evaluator

def load_objective(size,gen,n):
 d = "generation%s/" % gen
 art = "art%d"
 crit = "crit%d"
 a=objective(size)
 for k in range(size):
  fn=d+art%k
  print fn
  a.artists[k].load(fn)
 fn=d+crit%n
 print fn
 a.critic.load(fn)
 return a

class objective:
 def __init__(self,size,evals):
  self.evol_length=evals
  self.artists=[]
  self.critic=critic_class()
  self.size=size
  for k in range(size):
   self.artists.append(hyperneat.artist())
 def evaluate(self):
  for k in self.artists:
   self.evalind(k)
  self.artists.sort(key=lambda k:k.fitness,reverse=True)
 def evalind(self,k):
  if not k.isrendered():
   k.render_picture()
  if not k.get_nanflag():
   k.fitness=self.critic.evaluate_artist(k)
  else:
   k.fitness= -100
   k.clear_picture()

 def evolve(self):
  self.artists,self.herit = fuss_create_new_pop(self.artists,self.evalind,self.evol_length)
 def mutate(self):
  self.critic.mutate()
 def copy(self):
  new = objective(self.size,self.evol_length)
  for k in range(self.size):
   new.artists[k]=self.artists[k].copy()
  new.critic=self.critic.copy()
  return new
 def __str__(self):
  return str(self.critic)
 def save(self,fn):
  self.artist_xml=[]
  for k in self.artists:
   artist_xml = k.save_xml()
   self.artist_xml.append(artist_xml)
  self.critic_str=self.critic.to_string()
  a=open(fn,"w")
  pickle.dump(self,a) 

 @staticmethod
 def load(fn):
  a=open(fn,"r")
  new=pickle.load(a)
  new.artists=[]
  new.critic=critic_class.from_string(new.critic_str)
  #print new
  for k in new.artist_xml:
   if k!='':
    new.artists.append(hyperneat.artist.load_xml(k))
  return new

 def __getstate__(self):
  odict = self.__dict__.copy()
  del odict['artists']
  del odict['critic']
  return odict

def multiobjective_select(pop):
 num_objectives=len(pop[0].objectives)
 rankings=[]
 avg=[]
 for k in range(num_objectives):
  avg.append(sum([l.objectives[k] for l in pop])/len(pop))
  rankings.append(create_rankings([l.objectives[k] for l in pop]))

 print "avg:", " ".join([str(x) for x in avg])

 newpop=[]
 poplen=len(pop)
 thresh=int(len(pop)*0.7)
 for k in range(len(pop)):
  obj=random.randint(0,num_objectives-1)
  repro=rankings[obj][random.randint(0,thresh-1)]
  newpop.append(make_new(pop[repro]))
 return newpop


def save_pop(pop,fname):
 count=0
 for k in pop:
  k.save(fname%count)
  count+=1

def load_pop(fn,size,cname):
 pop=[]
 for k in range(size):
  pop.append(cname.load(fn%k))
 return pop

def create_new_pop_gen(oldpop,rate=0.3,psize=None):
 if(psize==None):
  psize=len(oldpop)
 newpop=[]
 oldpop.sort(key=lambda k:k.raw_fitness)

 #elitism
 newpop.append(oldpop[-1].copy())


 oldpop.sort(key=lambda k:k.fitness)
 eligpop=oldpop[int(rate*len(oldpop)):]
  
 for k in range(psize-1):
  new=make_new(random.choice(eligpop))
  newpop.append(new)
 return newpop

def create_new_pop(oldpop,evalf,count=50):
 herit=[] 

 newpop=oldpop[:]
 tot_size=len(newpop) 

 fits = [k.fitness for k in newpop]
 #print "range ",maxf,minf,maxf-minf

 for k in range(count): 
  fits = [k.fitness for k in newpop]
 
  #right now any individual is eligble for reproduction
  #perhaps restrict later 
  new=make_new(random.choice(newpop))
  evalf(new)

  newfit = new.fitness
  herit.append((oldfit,newfit))

  if(newfit!=-100):
   newpop.append(new)
   newpop.sort(key=lambda k:k.fitness,reverse=True)
   #delete worst
   del newpop[-1]
  else:
   print "rejected"
 del oldpop
 return newpop,herit

def fuss_create_new_pop(oldpop,evalf,count=50):
 herit=[] 

 newpop=oldpop[:]
 tot_size=len(newpop) 

 fits = [k.fitness for k in newpop]
 minf=min(fits)
 maxf=max(fits)
 #print "range ",maxf,minf,maxf-minf

 for k in range(count): 
  fits = [k.fitness for k in newpop]
  minf=min(fits)
  maxf=max(fits)
  rval = random.uniform(minf-0.01,maxf+0.01)
 
  j=0
  while(j<(tot_size-1) and newpop[j].fitness>rval):
   j+=1
  if(j>0 and abs(newpop[j].fitness-rval)>abs(newpop[j-1].fitness-rval)):
   j-=1
  oldfit = newpop[j].fitness

  new=make_new(newpop[j])
  evalf(new)

  newfit = new.fitness
  herit.append((oldfit,newfit))

  if(newfit!=-100):
   j=0
   worst_sc=10000.0
   worst=None
   while j<(tot_size-1):
    sc=fits[j]-fits[j+1]
    #print sc,worst_sc
    if(sc<worst_sc):
     worst_sc=sc
     worst=j
    j+=1
   del newpop[worst]
  
   newpop.append(new)
   newpop.sort(key=lambda k:k.fitness,reverse=True)
  else:
   print "rejected"
 del oldpop
 return newpop,herit

def make_new(ind):
 child=ind.copy()
 if(random.random()>0.2):
  child.mutate()
 #make random offspring
 if(random.random()<0.01):
  child=ind.__class__()
 return child
