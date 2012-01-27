import evolve_to
import pickle
import sys
import hyperneat

if(len(sys.argv)>3):
 print "seeding..."
 hyperneat.artist.seed(int(sys.argv[3]))

fn="samples.dat"
if(len(sys.argv)>4):
 print "overwriting fn"
 fn=sys.argv[4]

a=open(fn,"r")
samples =pickle.load(a)

gen=int(sys.argv[1])
index=int(sys.argv[2])

feature = samples[gen][index]
#print feature
trials=[]
for k in range(5):
 trials.append(evolve_to.evolve_to(feature[1]))
prefix=fn[:3]
b=open("res/%s-res%d_%d.txt"%(prefix,gen,index),"w")
b.write(str(sum(trials)/len(trials)))
