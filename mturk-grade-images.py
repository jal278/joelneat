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

gen=int(sys.argv[1])
fname="/home/joel/mturk/mturk/gen%d/loadhits-results.csv" % gen
gnome="/home/joel/mturk/mturk/gen%d/gnome%d.txt"
gnome_pic="/home/joel/mturk/mturk/gen%d/gnome%d.png"
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

best_overall = avg_dict(res_dict,avg)
print best_overall
most_div = avg_dict(res_dict,div)
best_overall.sort(reverse=True)
most_div.sort(reverse=True)


