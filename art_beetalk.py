import sys
import os
import hyperneat
import random

from art_basics import *
from art_coev_basics import *


hyperneat.initialize()

def grade_flowers(flower_pop,best_critics):
 for crit in best_critics:
   ranks=[]
   fits=[]

   #evaluate all the artists by the best critics
   for art in flower_pop:
    fit=crit.evaluate_all(art)
    fits.append(fit)
   
   #rank the artists by their critic assessments
   ranks=zip(fits,range(len(flower_pop)))
   ranks.sort()
   scores,ranks=zip(*ranks)
 
   #give an individual fitness proportional to its rank
   for k in range(len(flower_pop)):
    art = flower_pop[ranks[k]]
    if(art.nectar==crit.nectar):
     art.fitness+=scores[k]
    #else:
    # art.fitness-=(k/50.0)

 for k in flower_pop:
  k.raw_fitness=k.fitness

def flower_iteration(flower_pops,best_critics,specs):
 flower_best=[]
 nectartypes=range(len(flower_pops))
 print "# critics",len(best_critics)

 count=0
 for flower_pop in flower_pops:
  for art in flower_pop:
   if(not art.isrendered()):
    art.render()
  if(art.get_nanflag()):
    art.fitness = -10000.0
    art.clear()
   else:
    art.fitness=0.0
   art.nectar=nectartypes[count]
  count+=1
 
 flower_pop=reduce(lambda x,y:x+y,flower_pops)
 random.shuffle(flower_pop)
 grade_flowers(flower_pop,best_critics)

 best_art=[]
 pop_tots=[]
 for pop in flower_pops:
  pop.sort(key=lambda k:k.fitness,reverse=True)
  best_art.append(pop[:1])
  flower_best.append(pop[0])
  pop_tots.append(sum([k.fitness for k in pop[:2]]))

 flower_repro(flower_pops,specs)
 return best_art,pop_tots,flower_best

def flower_repro(flower_pops,speciators):
 migrate=0.00
 migrate_count=1
 global speciation 
 global health
 global flower_pop_size
 
 
 if health>8 and random.random()<migrate:
  print "migrating..."
  for i in range(1,len(flower_pops)):
   pop=flower_pops[i]
   for k in range(migrate_count):
    del pop[-1]
    pop.insert(0,flower_pops[0][k].copy())
    pop[0].fitness=100000

 for i in range(len(flower_pops)):
   psize=flower_pop_size
   #new pops
   speciator=speciators[i]
   pop=flower_pops[i]
   if(speciation):
    speciator.speciate(pop)
   flower_pops[i]  = create_new_pop_gen(pop,0.5,psize)
   
def grade_critics(critic_pops,best_art):
 global flower_archive

 random.shuffle(best_art)
 trial_pop = best_art #+ flower_archive

 for critic_pop in critic_pops:
  for crit in critic_pop:
   fits=[]
   for art in trial_pop:
    fit=crit.evaluate_all(art)
    fits.append((fit,art.nectar))
   
   ranks=zip(fits,range(len(trial_pop)))
   if max(fits)[0]==min(fits)[0]:
    print "ALLSAME"
    crit.fitness-=100000
   random.shuffle(ranks)
   ranks.sort()
   count=1
   for k in ranks:
    if k[0][1]==crit.nectar:
     crit.fitness+=count**2
    count+=1 
   crit.raw_fitness=crit.fitness
 #if random.random()<0.3:
 # best.nectar=-1 
 # flower_archive.append(best)
 # print "added to archive..."
 
def critic_iteration(critic_pops,best_art):
 global speciation

 nectartypes=range(len(critic_pops))
 count=0

 for critic_pop in critic_pops:
  for crit in critic_pop:
   crit.fitness=0.0
   crit.nectar=nectartypes[count]
  count+=1

 random.shuffle(best_art)
 grade_critics(critic_pops,best_art)

 #extract best critics for next round
 critic_best=[]

 for critic_pop in critic_pops:
  critic_pop.sort(key=lambda k:k.raw_fitness,reverse=True)
  critic_best+= critic_pop[:1] 

 score_critic=sum([k.fitness for k in critic_best])
 print "critic score:", score_critic
 count=0
 for critic_pop in critic_pops:
  if(speciation):
   critic_speciators[count].speciate(critic_pop)
  critic_pops[count] = create_new_pop_gen(critic_pop,0.5)
  count+=1

 return critic_pops,critic_best,score_critic


render=True
screen,background=None,None
if(render):
 import pygame

#PYGAME SETUP
if(render):
 pygame.init()
 screen = pygame.display.set_mode((900, 700))
 background = pygame.Surface(screen.get_size())
 background = background.convert()
 background.fill((255, 255, 255))
 screen.blit(background, (0, 0))
 pygame.display.flip()

small=False
SX=SY=64
PXS=2
if small:
 SX=SY=16
 PXS = 8

def render_critic(x,y,pxsize,data):
 global render,screen,background,SX,SY
 maxv=0.0
 minv=0.0
 for xc in range(SX):
  maxv = max(maxv,max(data[xc]))
  minv = min(minv,min(data[xc]))
 
 if(maxv==0.0):
  print "maxv zero"
  maxv=0.001
 if(minv==0.0):
  minv=0.001

 if(not render):
  return
 for xc in range(SX):
  for yc in range(SY):
   neg=False
   dp = data[xc][yc]
   #print dp
   if (dp<0.0):
    neg=True
    dp/=minv
   else:
    dp/=maxv
   val=int(abs(dp)*255)
   val=min(val,255)
   val=max(0,val)
   r=0
   g=0
   b=0
   if(neg):
    r=val
   else:
    g=val
   pygame.draw.rect(background, (r,g,b), (x+xc*pxsize,y+yc*pxsize,pxsize,pxsize),0)


def render_picture(nectar,x,y,pxsize,data):
 global render,screen,background,SX,SY
 if(not render):
  return
 if(nectar==1):
  pygame.draw.rect(background,(0,255,0),(x-2,y-2,SX*pxsize+2,SY*pxsize+2),15)
 for xc in range(SX):
  for yc in range(SY):
   px=int ( (data[xc][yc]+1.0)*128)
   px=min(px,255)
   px=max(px,0)
   pygame.draw.rect(background, (px,0,0), (x+xc*pxsize,y+yc*pxsize,pxsize,pxsize),0)
  
hyperneat.artist.random_seed()
if(len(sys.argv)>2):
 print "seeding..."
 hyperneat.artist.seed(int(sys.argv[2]))

direc=sys.argv[1]
os.system("mkdir %s" % direc)

critic_pops=[]
critic_pop_size=10
critic_pop_count=2
flower_pop_size=10
flower_pop_count=2
speciation=True

critic_speciators=[Speciator(2.0,2) for k in range(1000)]
flower_speciators=[Speciator(20.0,2) for k in range(1000)]
flower_pops=[]
flower_archive=[]

"""
log_file=open(direc+"/log.dat","w")
log_file.write("##|##\n")
log_file.write("generation|")
for k in range(flower_pop_count):
 log_file.write("p%d|"%k)
log_file.write("critic\n")
"""

if(False):
 load_dir=direc+"/generation800/"
 nectar_pop=load_pop(load_dir+"nart%d",flower_pop_size,hyperneat.artist)
 nectarless_pop=load_pop(load_dir+"art%d",flower_pop_size,hyperneat.artist)
 critic_pop=load_pop(load_dir+"crit%d",critic_pop_size,critic_class)
else:
 flower_pops = create_flowers(flower_pop_size,flower_pop_count)
 critic_pops = bee_create_critics(critic_pop_size,critic_pop_count)

bestcount=1
critic_best=[]

for k in critic_pops:
 critic_best+=k[:bestcount]
 
print len(flower_pops)
best_art=reduce(lambda x,y:x+y,[pop[:1] for pop in flower_pops])

health=0
score_flowers=[]
score_critic=0
critic_cycles=1
gen=0
while(True):
 if(gen%5==0):
  add_new_pops(flower_pops,flower_pop_size,critic_pops,critic_pop_size) 
 print "generation:" ,gen
 print "pop length: ", len(flower_pops)

 gen+=1
 #score_nec = nec_tot
 #score_nonec = nonec_tot
 print "flower iteration."
 best_artworks,art_scores,flower_best=flower_iteration(flower_pops,critic_best,flower_speciators)
 best_art = reduce(lambda x,y:x+y,best_artworks)
 print "art score:", sum(art_scores)/len(art_scores)

 for k in range(int(critic_cycles)):
  print "critic iteration."
  critic_pops,best_critics,score_critic=critic_iteration(critic_pops,best_art)
 
 critic_best=best_critics
 best_crit=critic_best[:]
 best_art.sort(key=lambda k:k.raw_fitness,reverse=True)
 
 #health = sum([k.nectar for k in best_art[:10]])
 #print health

 if(render):
  background.fill((255, 255, 255))
  #note: use raw fitness for speciated pop
  gs=4
  for k in range(3):
   render_critic(725,0+180*k,PXS,critic_best[k].get_weights())
  for k in range(min(16,len(flower_pops))):
   ind = flower_best[k]
   render_picture(ind.nectar,25+(k%gs)*180,25+(k/gs)*180,PXS,ind.get_picture_num(0))
  screen.blit(background,(0,0))
  pygame.display.flip()

 if((gen)%50==0):
  directory="%s/generation%d"%(direc,gen)
  os.system("mkdir %s" % directory)
  for k in range(len(best_crit)):
   cfname = directory+"/crit%d" %k 
   best_crit[k].save(cfname)

  for k in range(len(best_art)):
   afname = directory+"/art%d" %k 
   best_art[k].save(afname)
 if(gen==1500):
  break
 #log_file.write("%f|%d|%d|%d|%d\n" % (gen,score_nec,score_nonec,score_critic,last_migration))
 #log_file.flush()
