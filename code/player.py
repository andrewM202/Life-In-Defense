import pygame
from settings import *
from support import import_folder
from timer import *

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
        self.speed = 500
        self.acceleration = pygame.math.Vector2(0, 0)
        self.on_ground = True
        self.jump_strength = -1.4
        self.gravity_strength = 0.008
        self.gravity_max = 2

        # Collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy() # Copy our rectangle and shrink it

        # Timers
        self.timers = {
            "jump": Timer(150) # Cooldown on jumping
        }


    def input(self):
        """ Handles player input """

        # Return list with keys being pressed
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # Jump if on ground and timer not active
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground and not self.timers["jump"].active:
            self.acceleration.y = self.jump_strength


    def collision(self, direction):
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

                        if self.direction.y > 0: # Moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: # Moving up
                            self.hitbox.top = sprite.hitbox.bottom

                        self.acceleration.y = 0
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                            
            # Gravity calculation
            self.on_ground = on_ground
            if not on_ground and self.acceleration.y < self.gravity_max:
                self.acceleration.y += self.gravity_strength
                if not self.timers["jump"].active: self.timers["jump"].activate()
            if on_ground:
                self.acceleration.y = 0

            # If gravity is on us change our direction so collision calculations work
            if self.acceleration.y < 0:
                self.direction.y = -1
            elif self.acceleration.y == 0:
                self.direction.y = 0
            else:
                self.direction.y = 1

        # No ground collision test
        elif direction == "horizontal":
            for sprite in self.collision_sprites.sprites():
                if hasattr(sprite, "hitbox"):
                    # Check general sprite collision with player
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0: # Moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # Moving left
                            self.hitbox.left = sprite.hitbox.right

                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                            


    def move(self, dt):
        # Normalize the direction vector so speed is constant
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.x += self.acceleration.x * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        # Horizontal collision
        self.collision("horizontal")

        # Vertical movement
        self.pos.y += self.direction.y * self.speed *  dt
        self.pos.y += self.acceleration.y * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        # Vertical collision, True because we want to do a ground collision test at the end
        self.collision("vertical")


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
