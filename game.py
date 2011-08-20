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
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Caveman Escape!')

clock = pygame.time.Clock()

graphics_path = './media/graphics/spritelib_gpl/platform/'

class Spritesheet(object):
    """Adapted from: http://pygame.org/wiki/Spritesheet"""
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Player(object):
    def __init__(self, screen):
        self.screen = screen
        self.pos = (0, 0)
        self.sheet = Spritesheet(graphics_path + 'char4.png')
        self.standing_right = self.sheet.image_at((395, 143, 48, 64), -1)
        self.standing_left = pygame.transform.flip(
                self.standing_right, True, False)
        self.running_right = self.sheet.images_at((
            (0, 12, 48, 64), (127, 12, 48, 64), (255, 12, 48, 64),
            (391, 12, 48, 64), (0, 143, 48, 64), (127, 143, 48, 64),
            (259, 143, 48, 64)), -1)
        self.running_left = [
            pygame.transform.flip(s, True, False) for s in self.running_right]
        self.current = self.running_right
        self.current_frame = 0

    def draw(self):
        self.screen.blit(self.current[self.current_frame], self.pos)
        self.current_frame += 1
        if self.current_frame >= len(self.current):
            self.current_frame = 0


def quit():
    pygame.quit()
    sys.exit()

player = Player(screen)

while True:
    t = clock.tick(10) / 1000.0
    for event in pygame.event.get():
        print event
        if event.type == QUIT:
            quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
            elif event.key == K_LEFT:
                player.current = player.running_left
                player.current_frame = 0
                #player.current_frame -= 1
                #if player.current_frame <= 0:
                #    player.current_frame = len(player.current)-1
            elif event.key == K_RIGHT:
                player.current = player.running_right
                player.current_frame = 0
                #player.current_frame += 1
                #if player.current_frame >= len(player.current):
                #    player.current_frame = 0


    screen.fill((0, 0, 0))
    player.draw()
    pygame.display.flip()
