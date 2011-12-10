import sys
import pickle
import numpy
import math

def load_maps(fname):
 lines=open(fname).read().split("\n")[:-1]
 return [[float(l) for l in k.split()] for k in lines]

class histogram:
 def map_to(self,pt):
  ret=[]
  for k in self.features:
   v = int(pt[k]/self.delta)
   v=min(v,self.gran-1)
   ret.append(v)
  return tuple(ret)
 def __init__(self,data,features,granularity):
  self.db=numpy.zeros([granularity]*len(features))
  self.features=features
  self.gran=granularity
  self.delta=1.0/granularity
  for k in data:
   index=self.map_to(k)
   self.db[index]+=1.0
  self.total=len(data)
 def get_freq(self,pt):
  index=self.map_to(pt)
  return float(self.db[index])/self.total

def make_choices(dims,maxv):
 feats=maxv
 index=list(range(dims))
 indexs=[]
 done=False
 st=0
 l=dims

 while(not done):
  st=0
  while(st<(l-1)):
   if(index[st]>=index[st+1]):
    index[st+1]=index[st]+1
    if(index[st+1]>=feats):
     done=True
     break
   st+=1
  if(not done):
   indexs.append(index[:])
  index[st]+=1
  while(index[st]>=feats):
   index[st]=0
   if(st==0):
    done=True
    break
   index[st-1]+=1
   st-=1 
 return indexs
import numpy
import cPickle as pickle
def make_db():
 feature_set=[]
 for k in range(1,5):
  feature_set+=make_choices(k,7)

 samples=[]
 for k in range(40):
  samples+=load_maps("samples%d.txt"%k)
 histograms=dict()
 for k in feature_set:
  print k,len(samples)
  x=histogram(samples,k,20)
  histograms[tuple(k)]=x

 a=open("db.out","wb")
 pickle.dump(histograms,a)
 print "saved!"

#make_db()

def load_hist():
 a=open("db.out","rb")
 hists = pickle.load(a)
 return hists

if(__name__=='__main__'):
 a=open("db.out","rb")
 hists = load_hist() # pickle.load(a)

 fn="arc_behaviorlist"
 if(len(sys.argv)>1):
  fn=sys.argv[1]
 
 archive=load_maps(fn)
 x=range(len(archive))
 y=[]

 for k in archive:
  best_feature=[]
  best_prob=1.0
  for h in hists:
    if (len(h)>3): 
     continue
    new=hists[h].get_freq(k)
    if(new<best_prob):
     best_prob = new
     best_feature = h
  print best_prob,best_feature
  print k
  if(best_prob==0.0):
   best_prob=10**-8
  y.append(math.log(best_prob))
 print sum(y)/len(y)

"""
from pylab import *
plot (x,y,'r+')
show()
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
(a_s,b_s,r,tt,stderr)=stats.linregress(x,y)
print a_s,b_s,r,tt
"""
