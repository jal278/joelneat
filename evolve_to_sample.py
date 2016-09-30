import evolve_to
import pickle
import sys
import hyperneat

if(len(sys.argv)>4):
 print "seeding..."
 hyperneat.artist.seed(int(sys.argv[4]))

fn="samples.dat"
if(len(sys.argv)>5):
 print "overwriting fn"
 fn=sys.argv[5]

a=open(fn,"r")
samples =pickle.load(a)

gen=int(sys.argv[1])
index=int(sys.argv[2])
run=int(sys.argv[3])

feature = samples[(gen,run)][index]
#print feature
trials=[]
for k in range(5):
 trials.append(evolve_to.evolve_to(feature[1]))
prefix=fn[:3]
b=open("res/%s-res%d_%d_%d.txt"%(prefix,gen,index,run),"w")
b.write(str(sum(trials)/len(trials)))
