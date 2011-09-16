import glob

#env = Environment(CPPFLAGS = ' -g `sdl-config --cflags`',LINKFLAGS = ' `sdl-config --libs`')
#-O3

current=glob.glob('*.cpp')
tinyxml=glob.glob('tinyxml/*.cpp')

allsrc=current+tinyxml

evolve=allsrc[:]
env=Environment(CPPFLAGS='-O3 -I /usr/include/python2.6/ -I /usr/lib/python2.6')
#env=Environment(CPPFLAGS='-g -I /usr/include/python2.6/ -I /usr/lib/python2.6')
#env.Program(source=evolve)
evolve+=glob.glob('*.cxx')
env.SharedLibrary(target="_hyperneat",source=evolve, SHLIBPREFIX='',LIBS=['gsl','gslcblas','bz2'])
