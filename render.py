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
 arcsize=len(glob.glob("%s/generation%d/archive*" %(direc,gen)))
 for k in range(arcsize):
  to_render = "%s/generation%d/archive%d"%(direc,gen,k)
  out_image = "%s/generation%d/rend_archive%d.png"%(direc,gen,k)
  print to_render,out_image
  render(to_render,out_image)
  if(k%50==0):
   print k

def render(in_fname,out_fname):
 newartist=hyperneat.artist.load(in_fname)
 newartist.render_big()
 obj=numpy.array(newartist.get_big(),'|i1')
 out=Image.fromarray(obj)
 out=out.convert("RGB")
 out.save(out_fname)

"""
for k in range(10,15):
 print "rendering ", k
 outdir = "render/nov%d/" % k
 #os.system("mkdir %s" % outdir)
 render_nov("res/artnov/run%d"%k,500,outdir)
"""
