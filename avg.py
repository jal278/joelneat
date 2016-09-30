import sys
tot=0.0
cnt=0
for k in sys.argv[1:]:
 x=float(open(k).read())
 print k,x
 tot+=x
 cnt+=1
print tot/cnt
