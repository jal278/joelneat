import hyperneat
import random

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

class feature_critic:
 def __init__(self):
   pass
 def evaluate_artist(self,a):
   avg=hyperneat.feature_detector.chop(a,6)
   #avg= (hyperneat.feature_detector.compression(a) + hyperneat.feature_detector.wavelet(a))/2
   #avg=hyperneat.feature_detector.wavelet(a)
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
 def __init__(self,size):
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
  for k in range(5):
   self.artists = fuss_create_new_pop(self.artists,self.evalind)
   self.evaluate()
 def mutate(self):
  self.critic.mutate()
 def copy(self):
  new = objective(self.size)
  for k in range(self.size):
   new.artists[k]=self.artists[k].copy()
  new.critic=self.critic.copy()
  return new

def herit_measure(h):
 h1,h2=zip(*h)
 return rankdist(get_ranks(h1),get_ranks(h2))

def fuss_create_new_pop(oldpop,evalf):
 herit=[] 

 newpop=oldpop[:]
 tot_size=len(newpop) 
 for k in range(50): 
  fits = [k.fitness for k in newpop]
  minf=min(fits)
  maxf=max(fits)
  rval = random.uniform(minf-0.01,maxf+0.01)

  j=0
  while(j<(tot_size-1) and newpop[j].fitness>rval):
   j+=1
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
 print "Heritability:",herit_measure(herit)
 return newpop

def make_new(ind):
 child=ind.copy()
 if(random.random()>0.2):
  child.mutate()
 return child
