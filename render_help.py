import hyperneat
from PIL import Image
import PIL
from array import array

def to_image(obj):
 out_array = []
 sz=len(obj)
 for row in obj:
  out_array+=row
 arr=array('B',out_array)
 return PIL.Image.fromstring('L',(sz,sz),arr.tostring())

def render_critic(critic,fn):
 data = critic.get_weights()
 out = []
 maxv=0.0
 minv=0.0
 sz = len(data)
 for xc in range(sz):
  maxv = max(maxv,max(data[xc]))
  minv = min(minv,min(data[xc]))
 
 if(maxv==0.0):
  print "maxv zero"
  maxv=0.001
 if(minv==0.0):
  minv=0.001

 if(not render):
  return
 for xc in range(sz):
  for yc in range(sz):
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
   out+=[r,g,b]

 arr=array('B',out)
 img=PIL.Image.fromstring('RGB',(sz,sz),arr.tostring())
 img=img.resize((128,128),Image.BICUBIC)
 img=img.convert("RGB")
 img.save(fn)

def render(in_fname,out_fname):
 newartist=hyperneat.artist()
 newartist.load(in_fname)
 render_artist(newartist,out_fname)
def render_small(newartist,out_fname,opt):
 newartist.render_opt(opt)
 obj=newartist.get_picture()
 out=Image.fromarray(numpy.array(obj)*255)
 out=out.convert("RGB")
 out=out.resize((128,128),Image.BICUBIC)
 out.save(out_fname)

def render_artist(newartist,out_fname):
 print "rendering..."
 newartist.render_big()
 print "converting..."
 obj=newartist.get_big()
 out=to_image(obj)
 #out=Image.fromarray(numpy.array(obj))
 out=out.convert("RGB")
 out.save(out_fname)
