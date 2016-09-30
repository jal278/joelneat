import pylab
from pylab import *
import matplotlib
pylab.ion()
import glob
import cPickle as pickle
files=glob.glob("z*.hist")
learn_states=[]
goal=(6,2)
cnt=0
for f in files:
 state=pickle.load(open(f,"r"))
 learn_states.append(state)
 if goal in state:
  pylab.clf()
  axes=pylab.gca()
  pylab.xlim([0,20])
  pylab.ylim([0,20])
  cnt+=1
  state[goal].append(goal)
  stuff=state[goal]
  x,y=stuff[0]
  for xn,yn in stuff[1:]:
   dx=xn-x
   dy=yn-y
   print x,y,dx,dy
   axes.arrow(x,y,dx,dy,head_width=0.2,head_length=0.3)
   x=xn
   y=yn
  pylab.draw()
  k=raw_input()
  print state[goal]
print cnt,len(files)
