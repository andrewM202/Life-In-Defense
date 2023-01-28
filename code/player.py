import pygame
from settings import *
from support import import_folder
from timer import *
from pygame.sprite import Sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group, collision_sprites):
        super().__init__(group)

        self.import_assets()
        self.animation_status = "ready_right" # Player's current animation state
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
        self.jump_strength = 15
        self.default_gravity = 0.55 # We increase self.gravity_gravity by dt every frame we jump. After the jump is done, we set self.gravity_strength back to this default
        self.gravity_strength = self.default_gravity
        self.default_speed = 12

        # Collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy() # Copy our rectangle and shrink it

        # Timers
        self.timers = {
            "jump": Timer(250) # Cooldown on jumping
        }


    def animate(self, dt):
        """ Create the player animations """

        # Increment our frame index by an arbitrary amount: 4
        self.frame_index = self.frame_index + 6 * dt

        # If wour frame goes over the amount of animation states we have, 
        # reset it to 0 so we restart the animation
        if self.frame_index >= len(self.animations[self.animation_status]):
            self.frame_index = 0

        self.image = self.animations[self.animation_status][int(self.frame_index)]


    def input(self, dt):
        """ Handles player input """

        # Return list with keys being pressed
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed.x = self.default_speed
            if not self.timers["jump"].active:
                if self.animation_status != "run_right": self.frame_index = 0
                self.animation_status = "run_right"
            else:
                self.animation_status = "jump_right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed.x = -self.default_speed
            if not self.timers["jump"].active:
                if self.animation_status != "run_left": self.frame_index = 0
                self.animation_status = "run_left"
            else:
                self.animation_status = "jump_left"
        else:
            if not self.timers["jump"].active:
                if self.animation_status not in ["ready_right", "ready_left"]: self.frame_index = 0
                if self.animation_status not in ["ready_right", "ready_left"]: 
                    if self.speed.x > 0 or self.animation_status in ["jump_right"]:
                        self.animation_status = "ready_right"
                    elif self.speed.x <= 0:
                        self.animation_status = "ready_left"

            self.speed.x = 0

        # Jump if on ground and timer not active
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground and not self.timers["jump"].active:
            self.speed.y = -self.jump_strength
            if self.animation_status != "jump": self.frame_index = 0
            self.animation_status = "jump_right" if self.speed.x > 0 else "jump_left"


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
                self.gravity_strength *= 1 + dt # Correct gravity with dt so jumping is framerate independent
                self.speed.y += self.gravity_strength
                if not self.timers["jump"].active: self.timers["jump"].activate()
            if on_ground:
                self.speed.y = 0
                self.gravity_strength = self.default_gravity

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
        self.pos.x += self.speed.x * (1 - dt)
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        # Horizontal collision
        self.collision("horizontal")

        # Vertical movement
        self.pos.y += self.speed.y # We do not multiply by dt here since the gravity is increased by dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        # Vertical collision, True because we want to do a ground collision test at the end
        self.collision("vertical", dt)


    def import_assets(self):
        self.animations = {
            "run_right": [],
            "run_left": [],
            "ready_right": [],
            "ready_left": [],
            "jump_right": [],
            "jump_left": [],
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
        self.input(dt)
        self.update_timers()
        # Move player
        self.move(dt)
        self.animate(dt)



