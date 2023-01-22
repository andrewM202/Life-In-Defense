import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group, collision_sprites):
        super().__init__(group)

        self.import_assets()
        self.animation_status = "down_idle" # Player's current animation state
        self.frame_index = 0 # The current frame of the current animation state

        # General setup
        self.image = self.animations[self.animation_status][self.frame_index]
        self.rect = self.image.get_rect(midbottom = position)
        self.z = Layers["player"]

        # Movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

        # Collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy() # Copy our rectangle and shrink it

    def input(self):
        """ Handles player input """

        # Return list with keys being pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0


    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "hitbox"):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == "horizontal":
                        if self.direction.x > 0: # Moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # Moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == "vertical":
                        if self.direction.y > 0: # Moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: # Moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery


    def move(self, dt):
        # Normalize the direction vector so speed is constant
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        # Horizontal collision
        self.collision("horizontal")

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        # Vertical collision
        self.collision("vertical")


    def import_assets(self):
        self.animations = {
            "down_idle": []
        }

        for animation in self.animations.keys():
            full_path = "../graphics/player/" + animation
            self.animations[animation] = import_folder(full_path)


    def update(self, dt):
        # Collect player input
        self.input()
        # Move player
        self.move(dt)
