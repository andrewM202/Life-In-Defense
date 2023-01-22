import pygame
from settings import *
from noise import generate_fractal_noise_2d
from player import Player
from sprites import GenericSprite, GroundBlock


class World:
    def __init__(self):

        # Get display surface
        self.display_surface = pygame.display.get_surface()
        self.noise = generate_fractal_noise_2d((Screen_Tile_Width, Screen_Tile_Height), (4, 4))

        # Sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # World settings
        self.ground_level = 12

        # Load tiles in
        self.load_world()

        # Create player
        self.player = Player((600, self.ground_level * Tile_Size), self.all_sprites, self.collision_sprites)

    def load_world(self):
        """ Load all the tiles in the world in """
        # Load a block in
        ground_center = pygame.image.load("../graphics/ground/ground_center.png").convert_alpha()
        ground_top = pygame.image.load("../graphics/ground/ground_top.png").convert_alpha()

        # If we pass this threshold in our 
        # noise generation we are drawing a block
        block_gen_threshold = -0.1

        for x in range(0, Screen_Tile_Width):
            for y in range(0, Screen_Tile_Height):
                if self.noise[x][y] >= block_gen_threshold and y >= self.ground_level:
                    # If there is no block above make this a top block
                    if (y > 0 and self.noise[x][y-1] < block_gen_threshold) or y == self.ground_level:
                        GroundBlock((x * Tile_Size , y * Tile_Size), ground_top, [self.all_sprites, self.collision_sprites])
                    else:
                        GroundBlock((x * Tile_Size , y * Tile_Size), ground_center, [self.all_sprites, self.collision_sprites])
                        # self.display_surface.blit(ground_center, (x * Tile_Size , y * Tile_Size))


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
        # of the playe rinto the center of the screen
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