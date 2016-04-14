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

def gen_novelty(indiv,num):
 indiv.render_picture()
 indiv.fitness=0.0
 indiv.behavior=numpy.array(nov_crit.evaluate_artist(indiv))
 art_pop=[]
 for k in range(200):
  n=make_new(indiv)
  art_pop.append(n)

 for art in art_pop:
   art.render_picture()
   art.fitness=0.0
   art.ranks=[]
   art.behavior=numpy.array(nov_crit.evaluate_artist(art))
   if(art.get_nanflag() or not art.get_valid()):
	  art.behavior[:]=0.0
 for art in art_pop:
   if(art.get_nanflag() or not art.get_valid()):
    art.fitness = -100.0
    art.clear_picture()
    art_pop.remove(art)
    continue
   else:
    art.fitness=[sum((art.behavior-x.behavior)**2) for x in [indiv]]
    art.fitness=art.fitness[0]
    art.raw_fitness = art.fitness
 indivs=[]
 art_pop.sort(key=lambda x:x.fitness)
 for k in range(num):
  idx=int(float(k)*len(art_pop)/num)
  indivs.append(art_pop[idx])
 return indivs

best_overall = avg_dict(res_dict,avg)
most_div = avg_dict(res_dict,div)
best_overall.sort(reverse=True)
most_div.sort(reverse=True)

import cline_ad as cline
import random
#to_reproduce=[(5,best_overall[0][1]),(4,best_overall[1][1])]
elitism=False

mx_e=max(best_list)
best_choices=[]
for k in range(len(best_list)):
 if best_list[k]==mx_e:
  best_choices.append(k)

best=random.choice(best_choices)
print best
#todo: novelty gunk

tot_create=9
nov_create=0
reg_create=tot_create-nov_create

#n=hyperneat.artist.load(gnome%(gen,best))
res=[]
# gen_novelty(n,nov_create)
order=range(tot_create)
import random
random.shuffle(order)
cnt=0
gmap=[]
for k in res:
 gmap.append(('nov',best,order[cnt]))
 k.save(gnome%(gen+1,order[cnt]))
 cnt+=1

to_reproduce=[]
for k in range(reg_create):
 #better for more diverse search
 to_reproduce.append((1,random.choice(top_ratings)))
 #to_reproduce.append((1,best))
print to_reproduce

for amt,idnum in to_reproduce:
 if(elitism):
  amt-=1
  cline.clone(gnome%(gen,idnum-1),gnome%(gen+1,order[cnt]))
  gmap.append(('clone',idnum-1,order[cnt]))
  cnt+=1
 for k in range(amt):
  cline.mutate(gnome%(gen,idnum-1),gnome%(gen+1,order[cnt]))
  gmap.append(('mutate',idnum-1,order[cnt]))
  cnt+=1

import cPickle as pickle
a=open("/home/joel/mturk/mturk/genmap%d.dat" % gen,"w")
pickle.dump(gmap,a)

for k in range(9):
 gn=gnome%(gen+1,k) 
 gnp=gnome_pic%(gen+1,k)
 print gn
 cline.render(gn,gnp)

#for k in range(9):
# gnome=+"/gnome%d" % k
# cline.mk_new(gnome+".txt")
# cline.render(gnome+".txt",gnome+".png"
