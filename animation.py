import pygame
from os import path
from constants import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self,position,size,game):
        pygame.sprite.Sprite.__init__(self)
        self.pos = position
        self.size = size
        self.game = game
        self.image = pygame.transform.scale(self.game.explosion[0], (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.current = pygame.time.get_ticks()
        self.frame_rate = FPS
        self.i = 0
        self.game.explosion_sound.play()
        # print(self.i)

    def update(self):
        if(pygame.time.get_ticks()-self.current > self.frame_rate):
            self.i += 1
            # print(self.i)
            if self.i >= len(self.game.explosion):
                self.kill()
                return
            self.current = pygame.time.get_ticks()
            self.image = pygame.transform.scale(
                self.game.explosion[self.i], (self.size, self.size))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        self.image.set_colorkey(BLACK)