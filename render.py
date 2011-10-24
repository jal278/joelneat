import hyperneat
import numpy
import sys
from art_basics import *

nm = novelty_mapper() 

load_gen=int(sys.argv[1])
import glob
from PIL import Image
arts=glob.glob("ns/generation%d/art*"%load_gen)
count=0
for k in arts:
 count+=1
 print count

def render(in_fname,out_fname):
 newartist=hyperneat.artist()
 newartist.load(in_fname)
 newartist.render_big()
 obj=newartist.get_big()
 out=Image.fromarray(numpy.array(obj))
 out=out.convert("RGB")
 out.save(out_fname)

