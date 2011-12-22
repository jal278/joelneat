import evolve_to
import pickle
import sys
import hyperneat

if(len(sys.argv)>3):
 print "seeding..."
 hyperneat.artist.seed(int(sys.argv[3]))

a=open("samples.dat","r")
samples =pickle.load(a)

gen=int(sys.argv[1])
index=int(sys.argv[2])

feature = samples[gen][index]
#print feature
trials=[]
for k in range(2):
 trials.append(evolve_to.evolve_to(feature[1]))

b=open("res%d_%d.txt"%(gen,index),"w")
b.write(str(sum(trials)/len(trials)))
