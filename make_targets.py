import pickle
a=open("novsamples.dat","rb")
features=pickle.load(a)
for k in range(40):
 a=open("fitness_targets/target%d.dat"%k,"wb")
 pickle.dump(features[(500,k)][0],a)
