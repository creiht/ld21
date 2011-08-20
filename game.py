# Copyright (C) 2011 by Chuck Thier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import os
import sys
import time

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((480, 640))
pygame.display.set_caption('Something cool goes here!')

clock = pygame.time.Clock()

class Ship(object):
    def __init__(self):
        self.pos = (10,10)
        self.image = pygame.transform.smoothscale(
            pygame.image.load('./media/ship.png'), (16, 24))
        self.rect = self.image.get_rect()

def quit():
    pygame.quit()
    sys.exit()

ship = Ship()

while True:
    t = clock.tick(30) / 1000.0
    for event in pygame.event.get():
        print event
        if event.type == QUIT:
            quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
    screen.fill((0, 0, 0))
    screen.blit(ship.image, ship.pos)
    pygame.display.flip()
