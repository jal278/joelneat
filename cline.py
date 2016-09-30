import hyperneat
import random

import pygame
from pygame.locals import *
from art_basics import *

render=False

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
PXS = 2

a=hyperneat.artist()
a.random_seed()

import sys
argv=sys.argv
if(argv[1]=='new'):
 n=hyperneat.artist()
 n.save(argv[2])

if(argv[1]=='mutate'):
 n=hyperneat.artist.load(argv[2])
 n.mutate()
 n.save(argv[3])


if(argv[1]=='render'):
 import render
 render.render(argv[2],argv[3])

