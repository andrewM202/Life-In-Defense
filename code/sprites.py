import pygame
from settings import *


class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, position, surf, groups, z = 1):
        super().__init__(groups)
        self.position = position
        self.image = surf
        self.rect = self.image.get_rect(topleft = position)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)



class Block(GenericSprite):
    def __init__(self, position, surface, groups, block_id):
        super().__init__(position, surface, groups)
        self.hitbox = self.rect.copy()
        self.block_id = block_id


class GroundBlock(Block):
    def __init__(self, position, surface, groups, block_id):
        super().__init__(position, surface, groups, block_id)

