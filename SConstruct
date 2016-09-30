import glob
ode_path = '/home/joel/ode-0.11.1/'

#env = Environment(CCFLAGS = ' -DPLOT_ON -DdTRIMESH_ENABLED -DdDOUBLE -DGRAPHICS -g -I./include')
env = Environment(CCFLAGS = ' -march=native -DdTRIMESH_ENABLED -DdDOUBLE -DGRAPHICS -O3 -g -I./include') #was -O2
env.AppendENVPath('CPLUS_INCLUDE_PATH', ode_path+'include')

#current=['biped.cpp',"biped_stuff.cpp","ConfigFile.cpp"] 
#rtneat=glob.glob('rtneat/*.cpp')


current=glob.glob('*.cpp')
current+=glob.glob('*.cxx')
current+=glob.glob('tinyxml/*.cpp')
#current.remove("mazeDlg.cpp")
#current.remove("mazeApp.cpp")

lib_src=current[:]
vis_src=current[:]

env=Environment(CPPFLAGS='-g -I /usr/include/python2.7/ -I /usr/lib/python2.7')
#env=Environment(CPPFLAGS='-g -I /usr/include/python2.6/ -I /usr/lib/python2.6 -march=native -O2')
env.SharedLibrary(target="_hyperneat",source=lib_src, SHLIBPREFIX='',LIBS=['pthread','m','gsl','gslcblas','bz2','libpython2.7','curses'],LIBPATH=['.','/usr/lib/','/usr/local/lib'])

#env.Program('arena_vis',source=vis_src, SHLIBPREFIX='',LIBS=['pthread','gsl','bz2','gslcblas','m','ode','libpython2.6','curses'],LIBPATH=['.','/usr/lib/','/usr/local/lib'])
