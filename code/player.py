import pygame
from settings import *
from support import import_folder
from timer import *
from pygame.sprite import Sprite

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
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(1, 1)
        self.on_ground = True
        self.jump_strength = 1000
        self.gravity_strength = 8
        self.default_speed = 500

        # Collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy() # Copy our rectangle and shrink it

        # Timers
        self.timers = {
            "jump": Timer(50) # Cooldown on jumping
        }


    def input(self):
        """ Handles player input """

        # Return list with keys being pressed
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed.x = self.default_speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed.x = -self.default_speed
        else:
            self.speed.x = 0

        # Jump if on ground and timer not active
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground and not self.timers["jump"].active:
            self.speed.y = -self.jump_strength



    def collision(self, direction, dt=None):
        """ Handle player collision with collision sprites,
        and check if player is on ground for gravity """

        if direction == "vertical":
            # If player is on ground or not
            on_ground = False
            # Make another rect right below our player rect
            # to check if our player is on ground
            ground_rect = self.hitbox.copy()
            ground_rect.center = (ground_rect.centerx, ground_rect.centery + 1)

            for sprite in self.collision_sprites.sprites():
                if hasattr(sprite, "hitbox"):
                    if sprite.hitbox.colliderect(ground_rect):
                        on_ground = True

                    # Check general sprite collision with player
                    if sprite.hitbox.colliderect(self.hitbox):

                        if self.speed.y > 0: # Moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.speed.y < 0: # Moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                            
            # Gravity calculation
            self.on_ground = on_ground
            if not on_ground:
                self.speed.y += self.gravity_strength * (1 + dt)
                if not self.timers["jump"].active: self.timers["jump"].activate()
            if on_ground:
                self.speed.y = 0

        # No ground collision test
        elif direction == "horizontal":
            for sprite in self.collision_sprites.sprites():
                if hasattr(sprite, "hitbox"):
                    # Check general sprite collision with player
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.speed.x > 0: # Moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.speed.x < 0: # Moving left
                            self.hitbox.left = sprite.hitbox.right

                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    

    def move(self, dt):
        # Horizontal movement
        self.pos.x += self.speed.x * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        # Horizontal collision
        self.collision("horizontal")

        # Vertical movement
        self.pos.y += self.speed.y * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        # Vertical collision, True because we want to do a ground collision test at the end
        self.collision("vertical", dt)
        self.speed.y *= 1 - dt


    def import_assets(self):
        self.animations = {
            "down_idle": []
        }

        for animation in self.animations.keys():
            full_path = "../graphics/player/" + animation
            self.animations[animation] = import_folder(full_path)


    def update_timers(self):
        # Update our timers if they are active
        for timer in self.timers:
            if self.timers[timer].active:
                self.timers[timer].update()


    def update(self, dt):
        # Collect player input
        self.input()
        self.update_timers()
        # Move player
        self.move(dt)



