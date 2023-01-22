import pygame
from settings import *
from player import Player
from chunk import Chunk
from pygame.math import Vector2


class World:
    def __init__(self):

        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # Chunks
        # Level the ground will spawn at when generating chunks
        self.ground_level = 12
        self.chunks = {}

        # Load blocks
        self.blocks = {}
        self.load_blocks()

        # Load tiles in
        self.load_world()

        # Create player
        self.player = Player((600, self.ground_level * Tile_Size), self.all_sprites, self.collision_sprites)

    def load_blocks(self):
        """ Load all of our blocks in as surfaces """
        for block in Block_Ids:
            self.blocks[Block_Ids[block]] = pygame.image.load(f"../graphics/ground/{block}.png").convert_alpha()

    def load_world(self):
        """ Load all the tiles in the world in """
        # Create our chunks

        for x in range(-1, 1):
            for y in range (0, 1):
                chunk_position = (x, y)
                self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.blocks, self.ground_level, chunk_position)

        # Test delete a chunk
        chunk_position = (-1, 0)
        # self.chunks[chunk_position].__del__()
        del self.chunks[chunk_position] # Free memory

        # Test restore the chunk
        self.chunks[chunk_position] = Chunk(self.all_sprites, self.collision_sprites, self.blocks, self.ground_level, chunk_position, True)

    def run(self, dt):
        # Set background color 
        sky_bg_color = (92, 76, 255)
        self.display_surface.fill(sky_bg_color)

        # Draw player
        self.all_sprites.custom_draw(self.player)

        # Update our sprites
        self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Get position of player, then calculate the offset 
        # of the player into the center of the screen
        self.offset.x = player.rect.centerx - Screen_Width / 2
        self.offset.y = player.rect.centery - Screen_Height / 2

        for layer in Layers.values():
            # Loop through all of our sprites, sorting them so player can appear behind
            # objects
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    # Make a rect of the player's offset then subtract it 
                    # from the sprite's position to make effect of movement
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)



