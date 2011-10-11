#import scipy.stats
#from scipy.stats.stats import kendalltau
import hyperneat
import random
from guppy import hpy

import pygame
from pygame.locals import *
import gc
from art_basics import *
offset=0
render=True
#PYGAME SETUP
screen,background=None,None
if(render):
 pygame.init()
 screen = pygame.display.set_mode((700, 700))
 background = pygame.Surface(screen.get_size())
 background = background.convert()
 background.fill((255, 255, 255))
 screen.blit(background, (0, 0))
 pygame.display.flip()

SX=SY=64
PXS=2

def render_picture(x,y,pxsize,data):
 global render,screen,background,SX,SY
 if(not render):
  return
 for xc in range(SX):
  for yc in range(SY):
   px=int ( (data[xc][yc])*256)
   px=min(px,255)
   px=max(px,0)
   pygame.draw.circle(background, (px,0,0), (x+xc*pxsize,y+yc*pxsize),pxsize,0)

def render_critic(x,y,pxsize,artist):
 global render,screen,background,SX,SY
 if(not render):
  return
 render_picture(x,y,pxsize,artist.get_weight())

def render_artist(x,y,pxsize,artist):
 global render,screen,background,SX,SY
 if(not render):
  return
 render_picture(x,y,pxsize,artist.get_picture())
 ycoord = y+SY*pxsize+5
 xcoord = x
 xlen = 0 #int(SX*pxsize * artist.fitness)
 if (xlen<0 or xlen>SX*pxsize):
  xlen=0
 pygame.draw.line(background, (0,255,0), (xcoord,ycoord),(xcoord+xlen,ycoord),5) 
a=hyperneat.artist()
a.random_seed()
artists = []

import sys

path=sys.argv[2]
load_gen=int(sys.argv[1])
import glob
arts=glob.glob("%s/generation%d/art*"%(path,load_gen))
for k in arts:
 newartist=hyperneat.artist()
 newartist.load(k)
 artists.append(newartist)

quit=False
render_art=True
while(not quit):
 gs=4
 #if(optimize):
  #for z in xrange(50):
  #cur_obj.artists[0].optimize(dummy)
   #cur_obj.artists[k].optimize(cur_obj.critic)
 for k in range(16):
  if(render_art):
   if(not artists[offset+k].isrendered()):
    artists[offset+k].render_picture()
   render_artist(25+(k%gs)*180,25+(k/gs)*180,PXS,artists[offset+k])
   
 if(render):
  screen.blit(background,(0,0))
  pygame.display.flip()
 background.fill((255, 255, 255))
 
 for event in pygame.event.get():
  if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
   quit=True
  elif event.type==KEYDOWN:
   if(event.key==K_t):
    render_art=not render_art
   if(event.key==K_e):
    cur_obj.evolve()
   if(event.key==K_f):
    cur_obj.evaluate()
   if(event.key==K_q):
    offset+=16
   if(event.key==K_w):
    offset-=16
