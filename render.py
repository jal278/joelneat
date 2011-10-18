import hyperneat
import numpy
import sys
from art_basics import *

nm = novelty_mapper() 

load_gen=int(sys.argv[1])
import glob
from PIL import Image
arts=glob.glob("generation%d/art*"%load_gen)
for k in arts:
 newartist=hyperneat.artist()
 newartist.load(k)
 newartist.render_big()
 obj=newartist.get_big()
 for x in range(len(obj)):
  for y in range(len(obj[x])):
   val=obj[x][y]
   val*=255
   val=int(val)
   obj[x][y]=val
 out=Image.fromarray(numpy.array(obj))
 out=out.convert("RGB")
 out.save("render/%s.jpg" % k)
