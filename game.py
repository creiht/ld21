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
import random

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Caveman Escape!')

clock = pygame.time.Clock()

graphics_path = './media/graphics/spritelib_gpl/platform/'

LEFT = 0
RIGHT = 1


class SpriteSheet(object):
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


class Blocks(object):

    def __init__(self):
        self.sheet = SpriteSheet(graphics_path + 'blocks1.png')
        self.rock = self.sheet.images_at((
            (2, 206, 32, 32), (36, 206, 32, 32)))

class Map(object):
    blocking = set('*')

    def __init__(self):
        with open('map.txt') as f:
            self.data = list(reversed(f.readlines()))
        self.screen_w = 20
        self.screen_h = 15
        self.screen_x = 0
        self.screen_y = 0
        self.blocks = Blocks()

    def render(self, screen):
        for y in range(self.screen_y, self.screen_y+self.screen_h+1):
            for x in range(self.screen_x, self.screen_x+self.screen_w+1):
                if self.data[y][x] == '*':
                    screen.blit(self.blocks.rock[0], (x*32, 480-(y+1)*32))

    def collision(self, sprite):
        # Check for head collision
        y = self.screen_y + (480-sprite.rect.top)/32
        x = self.screen_x + sprite.rect.centerx/32
        if sprite.jumping == True:
            if self.data[y][x] in self.blocking:
                sprite.jump_ticks = 0
                return True
        # Check falling collision
        y = self.screen_y + (480-sprite.rect.bottom)/32
        if sprite.jumping == True:
            if self.data[y][x] in self.blocking:
                sprite.jumping = False
                sprite.rect.bottom -= 2
                if sprite.images is None:
                    sprite.stop()
                return True
        else:
            if self.data[y-1][x] not in self.blocking:
                sprite.jumping = True
                sprite.jump_ticks = 0
        # Check for left/right collision
        if sprite.direction == RIGHT:
            x = self.screen_x + (sprite.rect.right)/32
            if ((self.data[y][x] in self.blocking) or
                    (self.data[y+1][x] in self.blocking)):
                #print (x,y)
                return True
        if sprite.direction == LEFT:
            x = self.screen_x + (sprite.rect.left)/32
            if ((self.data[y][x] in self.blocking) or
                    (self.data[y+1][x] in self.blocking)):
                #print (x,y)
                return True
        return False

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = SpriteSheet(graphics_path + 'char4.png')
        self.standing_right = self.sheet.image_at((395, 143, 48, 64), -1)
        self.standing_left = pygame.transform.flip(
                self.standing_right, True, False)
        self.running_right = self.sheet.images_at((
            (0, 12, 48, 64), (127, 12, 48, 64), (255, 12, 48, 64),
            (391, 12, 48, 64), (0, 143, 48, 64), (127, 143, 48, 64),
            (259, 143, 48, 64)), -1)
        self.running_left = [
            pygame.transform.flip(s, True, False) for s in self.running_right]
        self.jumping_right = self.running_right[0]
        self.jumping_left = self.running_left[0]
        self.frame = 0

        self.images = None
        self.image = self.standing_right
        self.direction = RIGHT
        self.movement = 2
        self.rect = pygame.Rect(0, 352, 48, 64)
        self.ticks = 60         # Ticks between animation change
        self.last_frame = 0     # ticks since last frame
        self.jumping = False
        self.blocked = False

    def update(self, t):
        if self.images:
            self.last_frame += t
            if self.last_frame > self.ticks:
                self.frame += 1
                if self.frame >= len(self.images):
                    self.frame = 0
                self.last_frame = 0
            if not self.blocked:
                if self.direction == RIGHT:
                    self.rect.left += self.movement
                elif self.direction == LEFT:
                    self.rect.left -= self.movement
            self.image = self.images[self.frame]
        if self.jumping:
            if self.jump_ticks > 0:
                self.rect.top -= self.movement
                self.jump_ticks -= 1
            else:
                self.rect.top += self.movement

    def run_right(self):
        self.direction = RIGHT
        player.images = player.running_right
        player.frame = 0

    def run_left(self):
        self.direction = LEFT
        player.images = player.running_left
        player.frame = 0

    def stop(self):
        self.images = None
        if self.direction == RIGHT:
            self.image = self.standing_right
        elif self.direction == LEFT:
            self.image = self.standing_left

    def jump(self):
        self.jumping = True
        self.jump_ticks = 40
        if self.direction == RIGHT:
            self.image = self.jumping_right
        elif self.direction == LEFT:
            self.image = self.jumping_left


def quit():
    pygame.quit()
    sys.exit()

def clear_screen(surf, rect):
    surf.fill((0, 0, 0), rect)

player = Player()
game_map = Map()
allsprites = pygame.sprite.RenderUpdates(player)

while True:
    t = clock.tick(60)
    for event in pygame.event.get():
        if event.type != MOUSEMOTION:
            print event
        if event.type == QUIT:
            quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
            elif event.key == K_LEFT:
                player.run_left()
            elif event.key == K_RIGHT:
                player.run_right()
            elif event.key == K_SPACE:
                if not player.jumping:
                    player.jump()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                if player.direction == LEFT:
                    player.stop()
            elif event.key == K_RIGHT:
                if player.direction == RIGHT:
                    player.stop()

    player.blocked = game_map.collision(player)
    allsprites.clear(screen, clear_screen)
    game_map.render(screen)
    allsprites.update(t)
    dirty = allsprites.draw(screen)
    pygame.display.flip()
