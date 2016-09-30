import os
import glob
query={0:0.8,2:1.4}

d_filt="com/comm%d/generation%d/"

d1=d_filt%(0,2500)



def run_closest(directory,rec,com=" 1 ",pause=""):
 os.system("./arena_vis %s" % (directory+("archive%d" % rec[-1])+com+pause))

def closest_in_file(d1):
 lines=open(d1+"arc_behaviorlist").read().split("\n")[:-1]
 lines=[[float(k) for k in z.split()] for z in lines]
 dist=[]
 for line in lines:
  d=0
  for z in query:
   delta=query[z]-line[z]
   d+=delta*delta
  dist.append(d)
 tot=zip(dist,lines,range(len(dist)))
 tot.sort()
 return tot[0]

def closest_in_files(d_filt,run_range,generation=2500):
 best_scr=10000.0
 best=None
 best_d=None
 for k in run_range:
  d=d_filt%(k,generation)
  rec=closest_in_file(d)
  if rec[0]<best_scr:
   best_scr=rec[0]
   best=rec
   best_d=d
 return best,best_d

rec,d=closest_in_files(d_filt,range(20))
print rec,d
run_closest(d,rec,pause="k")
