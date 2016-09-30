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
   a,ranks=zip(*ranks)
 
   #give an individual fitness proportional to its rank
   for k in range(len(flower_pop)):
    art = flower_pop[ranks[k]]
    art.fitness+=k
 for k in flower_pop:
  k.raw_fitness=k.fitness

def flower_iteration(flower_pops,best_critics,specs):
 count=0

 nectartypes=[0]*len(flower_pops)
 nectartypes[0]=1
 print "# critics",len(best_critics)

 for flower_pop in flower_pops:
  for art in flower_pop:
   if(not art.isrendered()):
    art.render_all()
   if(art.get_nanflag()):
    art.fitness = -10000.0
    art.clear_all()
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
  best_art.append(pop[:10])
  pop_tots.append(sum([k.fitness for k in pop[:10]]))

 flower_repro(flower_pops,specs)
 return best_art,pop_tots

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
   if (i==0):
    if (health>8):
      psize=int(flower_pop_size/1.5)
   else:
    if (health<8):
      psize=int(flower_pop_size*1.5) 
   #new pops
   speciator=speciators[i]
   pop=flower_pops[i]
   if(speciation):
    speciator.speciate(pop)
   flower_pops[i]  = create_new_pop_gen(pop,0.5,psize)
   
def grade_critics(critic_pop,best_art):
 global flower_archive
 best=best_art[0]
 random.shuffle(best_art)
 trial_pop = best_art+flower_archive
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
    if k[0][1]==1:
     crit.fitness+=count**2
    count+=1 
   crit.raw_fitness=crit.fitness
 if random.random()<0.3:
  best.nectar=-1 
  flower_archive.append(best)
  print "added to archive..."
 
def critic_iteration(critic_pop,best_art):
 global speciation
 for crit in critic_pop:
  crit.fitness=0.0
 random.shuffle(best_art)
 grade_critics(critic_pop,best_art)
 #extract best critics for next round
 critic_pop.sort(key=lambda k:k.raw_fitness,reverse=True)
 critic_best = critic_pop[:3] 
 score_critic=sum([k.fitness for k in critic_best])
 print "critic score:", score_critic
 if(speciation):
  critic_speciator.speciate(critic_pop)
  critic_pop = create_new_pop_gen(critic_pop,0.5)

 return critic_pop,critic_best,score_critic


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

critic_pop=[]
critic_pop_size=80
flower_pop_size=80
flower_pop_count=4
speciation=True

critic_speciator=Speciator(2.0,4)
flower_speciators=[Speciator(20.0,4) for k in range(flower_pop_count)]
flower_pops=[]
flower_archive=[]

log_file=open(direc+"/log.dat","w")
log_file.write("##|##\n")
log_file.write("generation|")
for k in range(flower_pop_count):
 log_file.write("p%d|"%k)
log_file.write("critic\n")
if(False):
 load_dir=direc+"/generation800/"
 nectar_pop=load_pop(load_dir+"nart%d",flower_pop_size,hyperneat.artist)
 nectarless_pop=load_pop(load_dir+"art%d",flower_pop_size,hyperneat.artist)
 critic_pop=load_pop(load_dir+"crit%d",critic_pop_size,critic_class)
else:
 flower_pops = create_flowers(flower_pop_size,flower_pop_count)
 critic_pop = create_critics(critic_pop_size)

bestcount=10
critic_best=critic_pop[:bestcount]
print len(flower_pops)
best_art=reduce(lambda x,y:x+y,[pop[:bestcount] for pop in flower_pops])

health=0
score_flowers=[]
score_critic=0
critic_cycles=1
gen=0
while(True):
 print "generation:" ,gen
 gen+=1
 #score_nec = nec_tot
 #score_nonec = nonec_tot
 print "flower iteration."
 best_artworks,art_scores=flower_iteration(flower_pops,critic_best,flower_speciators)
 best_art = reduce(lambda x,y:x+y,best_artworks)
 print art_scores

 for k in range(int(critic_cycles)):
  print "critic iteration."
  critic_pop,best_critics,score_critic=critic_iteration(critic_pop,best_art)
 
 critic_best=best_critics
 if(health<3):
  critic_cycles=5
 elif(health>9):
  critic_cycles=1
 else:
  critic_cycles=3 

 best_art.sort(key=lambda k:k.raw_fitness,reverse=True)
 health = sum([k.nectar for k in best_art[:10]])
 print health
 if(render):
  background.fill((255, 255, 255))
  #note: use raw fitness for speciated pop
  gs=4
  for k in range(3):
   render_critic(725,0+180*k,PXS,critic_best[k].get_weights())
  for k in range(16):
   total_pop=best_art[:16]
   render_picture(total_pop[k].nectar,25+(k%gs)*180,25+(k/gs)*180,PXS,total_pop[k].get_picture_num(0))
  screen.blit(background,(0,0))
  pygame.display.flip()

 if((gen)%50==0):
  directory="%s/generation%d"%(direc,gen)
  os.system("mkdir %s" % directory)
  cfname = directory+"/crit%d"
  save_pop(critic_pop,cfname)
  for k in range(len(best_artworks)):
   afname = directory+"/art%d" %k +"_%d"
   save_pop(best_artworks[k],afname)
 if(gen==1500):
  break
 #log_file.write("%f|%d|%d|%d|%d\n" % (gen,score_nec,score_nonec,score_critic,last_migration))
 log_file.flush()
