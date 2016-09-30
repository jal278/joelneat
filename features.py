import hyperneat
import sys
from art_basics import *

nm = novelty_mapper() 

load_gen=int(sys.argv[1])
path=sys.argv[2]

import glob
from PIL import Image
arts=glob.glob("%s/generation%d/art*"%(path,load_gen)
a=open("%s/generation%d/features" % (path,load_gen,"w")

for k in arts:
 newartist=hyperneat.artist()
 newartist.load(k)
 newartist.render_picture()
 a.write(k +" " + " ".join([str(x) for x in nm.evaluate_artist(newartist)]))
 a.write("\n")
a.close()
