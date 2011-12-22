import pickle
a=open("samples.dat","rb")
features=pickle.load(a)
features[500].sort()
for k in range(15):
 a=open("fitness_targets/target%d.dat"%k,"wb")
 pickle.dump(features[500][k],a)

