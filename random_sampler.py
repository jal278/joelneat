import hyperneat
import random
from art_basics import *


artists = []
import sys
hyperneat.artist.random_seed()
if(len(sys.argv)>3):
 print "seeding.."
 hyperneat.artist.seed(int(sys.argv[3]))
evals = int(sys.argv[1])
outfile = sys.argv[2]
fc = feature_critic() 
outstr=""

for x in range(evals):
 artist=hyperneat.artist()
 artist.make_random()
 artist.render_picture()
 vals = fc.map_all(artist)
 outstr += " ".join(map(str,vals))+"\n"

out = open(outfile,"w")
out.write(outstr)
