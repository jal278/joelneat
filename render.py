import hyperneat
import numpy
import os
import sys
from art_basics import *
from render_help import *

nm=novelty_mapper() 

import glob
from PIL import Image

def render_nov(direc,gen,out):
 arts=glob.glob("%s/generation%d/archive*"%(direc,gen))
 count=0
 for k in arts:
  count+=1
  render(k, out+k.split("/")[-1]+".png")
  if(count%50==0):
   print count

def render(in_fname,out_fname):
 newartist=hyperneat.artist.load(in_fname)
 newartist.render_big()
 obj=newartist.get_big()
 out=Image.fromarray(numpy.array(obj))
 out=out.convert("RGB")
 out.save(out_fname)

for k in range(20):
 print "rendering ", k
 outdir = "render/nov%d/" % k
 os.system("mkdir %s" % outdir)
 render_nov("artnov/run%d"%k,500,outdir)
