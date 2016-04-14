import numpy
import sys
import math
f=sys.argv[1]
a=open(f).read().split("\n")[:-1]
ind=0
rdict={}
for t in range(3):
 name=a[ind]
 print name
 ind+=1
 ores=[]
 for k in range(3):
  line=map(float,a[ind].split(","))
  z,res=line[0],line[1:]
  ores+=res
  ind+=1
 print sum(ores)/len(ores),numpy.array(ores).var()/math.sqrt(len(ores))
 rdict[name]=ores

import scipy
import scipy.stats

k=rdict.keys()

for a in k:
 for b in k:
  z1=rdict[a]
  z2=rdict[b]
  p=scipy.stats.ttest_ind(z1,z2)[1]
  print a,b,p
