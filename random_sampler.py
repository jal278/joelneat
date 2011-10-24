import hyperneat
import random
from art_basics import *

hyperneat.artist.random_seed()

artists = []
import sys
evals = int(sys.argv[1])
outfile = sys.argv[2]
fc = feature_critic() 
out = open(outfile,"w")
for x in range(evals):
 artist=hyperneat.artist()
 artist.make_random()
 artist.render_picture()
 vals = fc.map_all(artist)
 outstring= " ".join(map(str,vals))+"\n"
 out.write(outstring)
