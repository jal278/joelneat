import numpy
from art_basics import *
import random
import sys
from collections import defaultdict

a=hyperneat.artist()
a.random_seed()
artists = []
nov_crit = novelty_mapper()

def avg_dict(d,avgf):
 ret_list=[]
 for k in d:
  ret_list.append((avgf(d[k]),k))
 return ret_list
 
def avg(x):
 return float(sum(x))/len(x)

def div(x):
 a=avg(x)
 t=0.0
 for k in x: 
  t+=(k-a)**2
 return t
direct=sys.argv[1]
gen=int(sys.argv[2])
extract_name=sys.argv[3]


dir_prefix="/home/joel/mturk/mturk/%s/gen%d/" %(direct,gen)
imgname=dir_prefix+"gnome%d.png"
fname=dir_prefix+"loadhits-results.csv"
 
a=open(fname).read().split("\n")[:]
headers=a[0]
res_dict=defaultdict(list)

best_list=[0]*9

top_ratings=[]
user_list=[]
for k in a[1:]:
 fields=k.split(",")
 if fields[1]=='Rejected':
  print "rejected"
  continue
 user=[]
 for z in range(4,len(fields),2):
  try:
   user.append((int(fields[z+1]),int(fields[z])))
   res_dict[int(fields[z])].append(int(fields[z+1])) 
  except:
   print "field error."
 user.sort(reverse=True)
 rating=user[0][0]
 for r,pid in user:
  if rating !=r:
   break
  else:
   top_ratings.append(pid)
   best_list[pid-1]+=1
 user_list.append(user) 
#print res_dict
best_overall = avg_dict(res_dict,avg)
for k in res_dict:
 print ",".join(map(str,[k]+res_dict[k]))

print best_overall
best_ind=max(best_overall)[1]
best_file=imgname%(best_ind-1)
print "Best:",best_ind
print "fname:",best_file

import os
os.system("cp %s %s" % (best_file,extract_name))
#most_div = avg_dict(res_dict,div)
#best_overall.sort(reverse=True)
#most_div.sort(reverse=True)
