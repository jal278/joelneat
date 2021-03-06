import os
import hyperneat
import random
from art_basics import *

SX=SY=64
PXS = 2

a=hyperneat.artist()
a.random_seed()

import render as r2
def mk_new(fname):
 n=hyperneat.artist()
 n.save(fname)
def clone(inf,outf):
 os.system("cp %s %s" % (inf,outf))
def mutate(inf,outf):
  n=hyperneat.artist.load(inf)
  n.mutate()
  n.save(outf)
import subprocess
def render(inf,outf):
 r2.render(inf,outf)
 params = ['convert',outf,"-scale","128x128","-bordercolor","#0000FF","-border","2",outf]
 subprocess.check_call(params)

if(__name__=="__main__"):
 import sys
 argv=sys.argv
 
 if(argv[1]=='new'):
  mk_new(argv[2])

 if(argv[1]=='mutate'):
  mutate(argv[2],argv[3])

 if(argv[1]=='render'):
  render(argv[2],argv[3])
