#images=['s1.png','s2.png','s3.png','s4.png']
images=['z1.png','z2.png','z3.png','z6.png']

import random
from PIL import Image
ims=[Image.open(x).convert('RGBA') for x in images]


x='x'
y='y'
scale='scale'
rotate='rotate'
arrangement=[{x:130,y:30,scale:0.1,rotate:45},{x:50,y:160,scale:0.02,rotate:60},{x:10,y:10,scale:0.1,rotate:180}]
import cPickle as pickle
import copy
class ad_genome:
 def save(self,f):
  a=open(f,"w")
  pickle.dump(self.a,a)

 @staticmethod
 def load(f):
  a=open(f)
  k=ad_genome()
  k.a=pickle.load(a) 
  return k

 def copy(self):
  new=ad_genome()
  new.a=copy.deepcopy(self.a)
  return new
 def mutate(self):
  mp=1.0
  #for k in range(len(self.a)):
  if(True):
   k=random.randint(0,len(self.a)-1)
   record=self.a[k]
   if(random.random()<mp):
    record['x']+=random.randint(-50,50)
    record['y']+=random.randint(-50,50)
   #if(random.random()<mp):
   # factor=random.uniform(1.0,1.5)
   # if random.random()<0.5:
   #  factor=1.0/factor
   #record['scale']*=factor
   #if(random.random()<mp):
   # record['rotate']+=random.randint(-60,60)
   self.a[k]=record

 def __init__(self):
  self.a=[]
  for k in range(4):
   record={}
   record['x']=random.randint(0,200)
   record['y']=random.randint(0,200)
   record['scale']=0.05 #random.uniform(0.05,0.15)
   record['rotate']=0 #random.uniform(0,360)
   if k==3:
    record['scale']=0.1
   self.a.append(record)
 def render(self,fname):
  render_out(self.a,fname)

def render_out(arrangement,fn):
 fin=Image.new('RGBA',(200,200))
 fin.paste((255,255,255),None)
 minx = min([k['x'] for k in arrangement])
 miny = min([k['y'] for k in arrangement])
 for k in range(len(ims)):
  im=ims[k].copy()
  sz=im.size
  sc=arrangement[k]['scale']
  newsize=(int(sz[0]*sc),int(sz[1]*sc))
  im=im.rotate(arrangement[k]['rotate'],resample=Image.BICUBIC,expand=True)
  im=im.resize(newsize,Image.ANTIALIAS)
  fin.paste(im,(arrangement[k]['x']-minx,arrangement[k]['y']-miny),mask=im)
 fin.save(fn)
 return fin

#k=ad_genome()
#k.mutate()
#render_out(k.a,"out.png").show()
