import os
import hyperneat
import random
import pygame
import sys
import gc
from art_basics import *
from art_coev_basics import *

hyperneat.artist.random_seed()

direc=sys.argv[1] #"coev2"
load_dir_base=direc+"/generation%s/"

def set_base(dname):
 global load_dir_base
 load_dir_base=dname 

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
 nectar = hyperneat.artist.load(load_dir+"nart0")
 nectarless= hyperneat.artist.load(load_dir+"art0")
 critic = critic_class.load(load_dir+"crit0")
 return (nectar,nectarless,critic)

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
 for k in range(50,1050,50):
  print "Rendering ",k
  nectar,nectarless,critic=load_best(k)
  render_artist(nectar,"render/%s_nectar%d.png" % (direc,k))
  render_artist(nectarless,"render/%s_nonectar%d.png" % (direc,k))
  open("render/%s_critic%d.txt"%(direc,k),"w").write(str(critic))

def hillclimb_test():
 outfile=open(direc+".out","w")
 
 for k in range(50,1050,50):
  nectar,nectarless,critic=load_best(k)
  #print critic
  nectar.render_picture()
  nectarless.render_picture()
  f1=critic.evaluate_artist(nectar)
  f2=critic.evaluate_artist(nectarless)
  print "---"
  #print nectar.mapped
  #print nectarless.mapped
  print f1,f2
  trialsum=0
 
  for z in range(1):
   trials,fitness = hillclimb(5000,critic,f1)
   trialsum+=trials
  outfile.write("%d %d\n" % (k,trialsum))
 
def load_maps(fname):
 lines=open(fname).read().split("\n")[:-1]
 return [[float(l) for l in k.split()] for k in lines]

def sample_test(): 
 samples=load_maps(sys.argv[2])
 outfile=open(direc+"_sample.out","w")
 for k in range(50,1050,50):
  nectar,nectarless,critic=load_best(k)
  #print critic
  nectar.render_picture()
  nectarless.render_picture()
  f1=critic.evaluate_artist(nectar)
  f2=critic.evaluate_artist(nectarless)
  print "---"
  #print nectar.mapped
  #print nectarless.mapped
  outstr = " ".join(map(str,(k,f1,max(map(critic.evaluate_map,samples)),"\n")))
  print outstr
  outfile.write(outstr)

gen=600
test_pop=load_pop("ns4/generation%d/" % gen+ "art%d" ,400,hyperneat.artist)
nectar,nectarless,critic=load_best(1000)
nectar.render_picture()
benchmark =critic.evaluate_artist(nectar)
print benchmark
best=0.0
count=0
for k in test_pop:
 count+=1
 print k.complexity()
 k.render_picture()
 fit = critic.evaluate_artist(k)
 if fit>best:
  best=fit
  print benchmark,best

