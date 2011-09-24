import hyperneat
import sys
from art_basics import *

nm = novelty_mapper() 

load_gen=int(sys.argv[1])
import glob
arts=glob.glob("generation%d/art*"%load_gen)
a=open("generation%d/features" % load_gen,"w")
for k in arts:
 newartist=hyperneat.artist()
 newartist.load(k)
 newartist.render_picture()
 a.write(" ".join([str(x) for x in nm.evaluate_artist(newartist)]))
 a.write("\n")
a.close()
