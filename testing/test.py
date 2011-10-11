import hyperneat

def stress():
 while(True):
  a=hyperneat.artist()
  c=a.copy()
  del a
  del c

a=hyperneat.artist()
a.random_seed()
a.mutate()
b=hyperneat.evaluator()
a.render_picture()
c=a.get_picture()
import numpy

carr= numpy.array(c)
print carr.min()
print carr.max()
print carr[31,31]
print carr[28:,28:]
from pylab import *
matshow(numpy.array(c))
show()
