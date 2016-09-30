from multiprocessing import Process,Queue
import mazepy

mazepy.mazenav.initmaze("hard_maze_list.txt")

from multiprocessing import Process, Pipe
from itertools import izip

def spawn(f):
    def fun(pipe,x):
        pipe.send(f(x))
        pipe.close()
    return fun

def parmap(f,X):
    pipe=[Pipe() for x in X]
    proc=[Process(target=spawn(f),args=(c,x)) for x,(p,c) in izip(X,pipe)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [p.recv() for (p,c) in pipe]


if __name__=="__main__":

 population=[]
 proc=8
 for k in xrange(5000):
  robot=mazepy.mazenav()
  robot.init_rand()
  robot.mutate()
  population.append(robot)
 import time
 bef=time.time()
 print "?"
 parmap(lambda f:f.map(),population[0:8])
 #map(lambda f:f.map(),population[0:5000])
 print time.time()-bef
 print population[0].get_x()

