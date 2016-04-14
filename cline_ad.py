import os
import hyperneat
import random
from art_basics import *
import ad

SX=SY=64
PXS = 2

def mk_new(fname):
 n=ad.ad_genome()
 n.save(fname)
def clone(inf,outf):
 os.system("cp %s %s" % (inf,outf))
def mutate(inf,outf):
  n=ad.ad_genome.load(inf)
  n.mutate()
  n.save(outf)

import subprocess
def render(inf,outf):
 a=ad.ad_genome.load(inf)
 a.render(outf)
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
