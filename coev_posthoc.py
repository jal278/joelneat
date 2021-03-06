import os
import hyperneat
import random
import sys
import glob
from art_basics import *
from art_coev_basics import *
from render_help import *
hyperneat.artist.random_seed()

direc="test"
load_dir_base=direc+"/generation%s/"

def set_base(dname):
 global direc,load_dir_base
 direc=dname
 load_dir_base=direc+"/generation%s/"

def load_all(gen):
 global load_dir_base
 load_dir = load_dir_base % gen
 nectar_pop=load_pop(load_dir+"nart%d",100,hyperneat.artist)
 nectarless_pop=load_pop(load_dir+"art%d",100,hyperneat.artist)
 critic_pop=load_pop(load_dir+"crit%d",100,critic_class)
 return (nectar_pop,nectarless_pop,critic_pop)

def load_beeart(gen):
 global load_dir_base
 load_dir = load_dir_base % gen
 arts = load_dir+"art*"
 artfn = load_dir+"art%d"
 amt = len(glob.glob(arts))
 art=[]
 for l in range(amt):
  k = artfn%l
  art.append(hyperneat.artist.load(k))
 return art

def load_beecrit(gen):
 global load_dir_base
 load_dir = load_dir_base % gen
 arts = load_dir+"crit*"
 artfn = load_dir+"crit%d"
 amt = len(glob.glob(arts))
 art=[]
 for l in range(amt):
  k = artfn%l
  art.append(critic_class.load(k))
 return art

def load_best(gen,amt=4):
 global load_dir_base
 load_dir = load_dir_base % gen
 bests=[]
 for k in range(amt):
  bests.append(hyperneat.artist.load(load_dir+"art%d_0" % k))
 critic = critic_class.load(load_dir+"crit0")
 return (bests,critic)

def hillclimb(trials,critic,target):
 starter = hyperneat.artist()
 starter.render_picture()
 fitness = critic.evaluate_artist(starter)
 trial=0
 print fitness
 while(trial<trials and fitness<target):
  offspring = make_new(starter)
  offspring.render_picture()
  nfit = critic.evaluate_artist(offspring)
  if(nfit>fitness):
   print nfit,target
   fitness=nfit
   starter=offspring
  trial+=1
 print trial
 return trial,fitness

hyperneat.artist.random_seed()

def render_bee(outdir):
 for k in range(0,700,50):
  print "Rendering ",k
  arts=load_beeart(k)
  #crits=load_beecrit(k)
  #render_critic(critic,"%s/crit%d.png" % (outdir,k))
  scores=[]
  for j in range(len(arts)):
   arts[j].render_all()
   render_artist(arts[j],"%s/art%d_%d.png" % (outdir,k,j))
   #score = critic[j].evaluate_all(arts[j])    
   #scores.append((score,j))
  #scores.sort(reverse=True)
  #scores,ranks=zip(*scores)
  #score_out = open("%s/scores%d.txt"%(outdir,k),"w")
  #for ind in range(len(scores)):
  # num=ranks.index(ind)
  # score_out.write(str(num+1)+": " + str(scores[num])+"\n")

def render_novelty(outdir,gen):
 global load_dir_base
 load_dir = load_dir_base % gen
 archive=glob.glob(load_dir+"archive*")
 archive_fn=(load_dir+"archive%d")
 cnt=len(archive)
 inds = []
 for k in range(cnt):
  fn = archive_fn%k
  print fn
  inds.append(hyperneat.artist.load(fn))
  render_artist(inds[-1],"%s/archive%d_%d.png" % (outdir,gen,k))

def render(outdir):
 for k in range(0,1200,50):
  print "Rendering ",k
  bests,critic=load_best(k,4)
  render_critic(critic,"%s/crit%d.png" % (outdir,k))
  scores=[]
  for j in range(len(bests)):
   bests[j].render_all()
   render_artist(bests[j],"%s/art%d_%d.png" % (outdir,k,j))
   score = critic.evaluate_all(bests[j])    
   scores.append((score,j))
  scores.sort(reverse=True)
  scores,ranks=zip(*scores)
  score_out = open("%s/scores%d.txt"%(outdir,k),"w")
  for ind in range(len(scores)):
   num=ranks.index(ind)
   score_out.write(str(num+1)+": " + str(scores[num])+"\n")
  
  #open("%s/critic%d.txt"%(outdir,k),"w").write(str(critic))

"""
#for rendering a whole coev set of runs
basedir="test2"
set_base(basedir)
outdir="render2"
render_bee(outdir)
"""

"""
for k in range(30,40):
 print "rendering %d" % k
 basedir = "hartcov/run%d" % k
 set_base(basedir)
 outdir = "render/hcov%d/" %k
 os.mkdir(outdir)
 render(outdir)
"""

def evol_test(index):
 critic = critic_class.load(direc+"/generation1050/crit%d" % index)

 population=[]
 for k in range(200):
  population.append(hyperneat.artist())

 speciator = Speciator(20.0,5)

 gen=0
 while(True):
  for k in population:
   k.render_picture()
   k.fitness =  critic.evaluate_artist(k)
  max_fit = max([k.fitness for k in population])
  print gen, max_fit 
  speciator.speciate(population)
  population = create_new_pop_gen(population,0.3)
  gen+=1

def hillclimb_test():
 outfile=open(direc+".out","w")
 
 for k in range(850,0,-50):
  bests,critic=load_best(k)
  #print critic
  f=[]
  for art in bests:
   art.render_picture()
   f.append(critic.evaluate_artist(art))

  print "---"
  #print nectar.mapped
  #print nectarless.mapped
  print f
  trialsum=0
 
  for z in range(5):
   trials,fitness = hillclimb(5000,critic,f[0])
   trialsum+=trials
  outfile.write("%d %d\n" % (k,trialsum))
 
def load_maps(fname):
 lines=open(fname).read().split("\n")[:-1]
 return [[float(l) for l in k.split()] for k in lines]

def sample_beetest(outf,gen):
 global samples
 art=load_beeart(gen)
 crit=load_beecrit(gen)
 print len(art),len(crit)
 #outfile=open(outf,"w")
 print "rendering"

 for k in range(len(art)):
  art[k].render_picture()
  print k

 for index in range(len(art)):
  a = art[index]
  c = crit[index]
  
  a.render_picture()
  f=c.evaluate_artist(a)

  fs=[]
  for k in range(len(art)):
   fs.append(c.evaluate_artist(art[k]))
  bet=len(filter(lambda x:x>f,fs))

  print "summary:",f,bet
  
  sampled_fit = map(c.evaluate_map,samples)
  mfit = max(sampled_fit)
  firstbeat=len(samples)
  for j in xrange(0,len(sampled_fit)):
   if sampled_fit[j]>f:
     firstbeat=j
     break
  outstr = " ".join(map(str,(index,f,mfit,firstbeat)))
  print outstr

 #outfile.write(outstr+"\n")
def sample_test(outf): 
 global samples
 outfile=open(outf,"w")
 for k in range(50,550,50):
  bests,critic=load_best(k)
  #print critic
  f=[]
  for art in bests:
   art.render_picture()
   f.append(critic.evaluate_artist(art))
  sampled_fit = map(critic.evaluate_map,samples)
  mfit = max(sampled_fit)
  firstbeat=len(samples)
  for j in xrange(0,len(sampled_fit)):
   if sampled_fit[j]>f[0]:
    firstbeat=j
    break
  outstr = " ".join(map(str,(k,f[0],mfit,firstbeat)))
  print outstr

  outfile.write(outstr+"\n")

"""
samples=[]
print "loading samples..."


for k in [0,10]: #range(10):
 print k
 samples+=load_maps("samples/samples%d.txt"%k)
"""

"""
for k in range(20):
 print k
 samples+=load_maps("artnov/run%d/generation500/arc_behaviorlist"%k)
 samples+=load_maps("artnov/run%d/generation500/pop_behaviorlist"%k)
"""

for k in range(15,1,-1):
 print k
 basedir="res/artnov/run%d" % k
 set_base(basedir)
 outdir="render/nov%d/"%k
 os.system("mkdir %s" % outdir)
 render_novelty(outdir,500)
#sample_beetest("test.out",650)

"""
for k in range(20):
 print "sample testing %d" % k
 basedir = "artcov/run%d" % k
 set_base(basedir)
 outf = "artcov%d_sample.out" % k
 sample_test(outf)
"""

def map_novelty(direc,gen,outfile):
 test_pop=load_pop(direc+"/generation%d/" % gen+ "art%d" ,400,hyperneat.artist)
 outstr=""
 fc=feature_critic()
 for artist in test_pop:
  artist.render_picture()
  vals = fc.map_all(artist)
  outstr += " ".join(map(str,vals))+"\n"
 open(outfile,"w").write(outstr)

def test_novelty():
 gen=600
 test_pop=load_pop("ns4/generation%d/" % gen+ "art%d" ,400,hyperneat.artist)
 bests,critic=load_best(200)
 f=[]
 for k in range(len(bests)):
  bests[k].render_picture()
  f.append(critic.evaluate_artist(bests[k]))

 benchmark=f[0]
 print f
 print critic

 best=0.0
 count=0
 bcount=0
 for k in test_pop:
  count+=1
  k.render_picture()
  fit = critic.evaluate_artist(k)
  if fit>best:
   render_artist(k,"novelty%d.png" % (bcount))
   best=fit
   print count,benchmark,best
   bcount+=1

