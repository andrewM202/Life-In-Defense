import pygame
from settings import *


class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, position, surf, groups, z = 1):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = position)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)



class GroundBlock(GenericSprite):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy()

