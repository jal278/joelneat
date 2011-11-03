import os
import hyperneat
import random
import pygame
import sys
import gc
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

def load_best(gen):
 global load_dir_base
 load_dir = load_dir_base % gen
 bests=[]
 for k in range(3):
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

def render():
 for k in range(2000,0,-50):
  print "Rendering ",k
  nectar,nectarless,critic=load_best(k)
  render_artist(nectar,"render/%s_nectar%d.png" % (direc,k))
  render_artist(nectarless,"render/%s_nonectar%d.png" % (direc,k))
  open("render/%s_critic%d.txt"%(direc,k),"w").write(str(critic))

def evol_test():
 critic = critic_class.load(direc+"/generation850/crit0")

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

def sample_test(): 
 samples=load_maps(sys.argv[2])
 outfile=open(direc+"_sample.out","w")
 for k in range(50,350,50):
  bests,critic=load_best(k)
  #print critic
  f=[]
  for art in bests:
   art.render_picture()
   f.append(critic.evaluate_artist(art))
  #print nectar.mapped
  #print nectarless.mapped
  sampled_fit = map(critic.evaluate_map,samples)
  mfit = max(sampled_fit)
  firstbeat=0
  for j in xrange(0,len(sampled_fit)):
   if sampled_fit[j]>f[0]:
    firstbeat=j
    break
  outstr = " ".join(map(str,(k,f[0],mfit,firstbeat)))
  print outstr

  outfile.write(outstr)

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

sample_test()
