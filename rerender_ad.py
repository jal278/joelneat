import cline_ad as cline
import sys
gnome="/home/joel/mturk/mturk/ad-revised3/gen%d/gnome%d.txt"
gnome_pic="/home/joel/mturk/mturk/ad-revised3/gen%d/new-gnome%d.png"
for gen in range(0,12):
 for k in range(9):
  gn=gnome%(gen,k) 
  gnp=gnome_pic%(gen,k)
  print gn
  cline.render(gn,gnp)
