import os
import sys
import random
import cline
outdir=sys.argv[1]
os.system("mkdir %s" % outdir)
for k in range(9):
 gnome=outdir+"/gnome%d" % k
 cline.mk_new(gnome+".txt")
 cline.render(gnome+".txt",gnome+".png")
