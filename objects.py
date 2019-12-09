#GAME OBJECTS

import pygame
import math
import random
from os import path
from constants import *

#Classes for in-game sprites
class Arrow(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        self.image_orig = pygame.transform.scale(game.arrow_img, ARROW_SIZE)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.centerx = self.WIDTH/2
        self.rect.bottom = self.HEIGHT-100
        self.rot = 0
        self.speedx = 0
        self.speedy = 0
        self.range = 0
        self.max_height = 0
        self.release_angle = 0
        self.set_vel = False
        self.Released = False
        self.releasex = self.rect.centerx
        self.releasey = self.rect.bottom
        self.cy = self.rect.centery
        self.game = game

    def update(self):
        if self.Released:
            self.speedy -= GRAVITY
            self.rect.bottom -= self.speedy
            self.rect.centerx += self.speedx
            self.rot = (-math.atan2(self.speedx, self.speedy)*180/3.14) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)

            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            # print "moving"

        else:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if mouse[1] > self.rect.centery and click[0] == 1:
                self.set_vel = True
                dist = math.sqrt(
                    math.pow(self.rect.centerx-mouse[0], 2)+math.pow(self.rect.bottom-mouse[1], 2))
                # print dist

                self.rect.centerx = mouse[0]
                self.rect.centery = mouse[1]
                # print(2*GRAVITY*(self.rect.centery-mouse[1]))
                self.speedy = math.sqrt(2*GRAVITY*(-self.cy+mouse[1]))*4
                self.speedx = self.speedy * \
                    (mouse[0]-self.releasex)/(self.cy-mouse[1])
                self.rot = (-math.atan2(self.speedx, self.speedy)
                            * 180/3.14*0.5) % 360
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center

                # print "setting velocity"

            else:
                if self.set_vel:
                    self.Released = True
                    self.game.last_arrow_time = pygame.time.get_ticks()
                    self.max_height = (self.rect.bottom-mouse[1])
                    self.range = (mouse[0]-self.rect.centerx)*2
                    # print "releasing"
                # math.sqrt(math.pow(mouse[0]-self.rect.centerx,2)+math.pow(mouse[1]-self.rect.centery,2)) < 200:
                else:
                    if (mouse[0]-self.rect.centerx) != 0:
                        theta = math.atan(
                            (mouse[1]-self.rect.bottom)/(self.rect.centerx-mouse[0]))
                    else:
                        theta = PI
                    move = theta-self.rot
                    self.rot = math.degrees(theta)
                    new_image = pygame.transform.rotate(
                        self.image_orig, self.rot)
                    old_center = self.rect.center
                    self.image = new_image
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    # print "rotating"
                    # print self.rot
                    # print theta


class Baloon(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        bcolor = random.choice(game.baloon_color)
        temp = "assets/balloon_{}.png".format(bcolor)
        self.image_orig = pygame.image.load(
            path.join(path.dirname(__file__), temp))
        if bcolor == "blue":
            self.image_orig.set_colorkey(BLUE)
        elif bcolor == "black":
            self.image_orig.set_colorkey(BLACK)
        elif bcolor == "green":
            self.image_orig.set_colorkey(BRIGHT_GREEN)
        elif bcolor == "red":
            self.image_orig.set_colorkey(BRIGHT_RED)

        self.image_orig = pygame.transform.scale(self.image_orig, BALOON_SIZE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = HIT_RADIUS

        temp = random.randrange(self.WIDTH - self.rect.width)
        while (-150 < temp-self.WIDTH/2 < 150):
            temp = random.randrange(self.WIDTH - self.rect.width)
        self.rect.x = temp
        self.rect.y = random.randrange(self.HEIGHT+100, self.HEIGHT+150)
        self.speedy = random.randrange(-4, -1)
        self.speedx = random.randrange(-3, 3)
        self.game = game
        self.last_update = pygame.time.get_ticks()
        # print "baloon"

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top < -20 or self.rect.left < -25 or self.rect.right > self.WIDTH + 20:
            self.kill()
            self.game.misses += 1