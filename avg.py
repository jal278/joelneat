import pickle
from collections import defaultdict
gen=0
def get_selections(dname,gen):
 fname="/home/joel/mturk/mturk/%s/genmap%d.dat" % (dname,gen)
 a=open(fname)
 print pickle.load(a)

#get_selections("old3",10)
#afd

def get_ratings(gen,dname):
 fname="/home/joel/mturk/mturk/%s/gen%d/loadhits-results.csv" % (dname,gen)
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
 return user_list
dname=["old","old2","old3","seeded1","seeded2","seeded3"]
for d in dname:
 gt=0
 for k in range(0,11):
  user_list=get_ratings(k,d)
  t=0
  for r in user_list:
   zz=[float(z[0]) for z in r]
   t+=sum(zz)/len(zz)
  gt+=t/len(user_list)
 print d,gt/10
