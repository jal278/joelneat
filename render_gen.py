import cline
import sys
gnome="/home/joel/mturk/mturk/gen%d/gnome%d.txt"
gnome_pic="/home/joel/mturk/mturk/gen%d/gnome%d.png"
gen=int(sys.argv[1])
for k in range(9):
 gn=gnome%(gen,k) 
 gnp=gnome_pic%(gen,k)
 print gn
 cline.render(gn,gnp)
