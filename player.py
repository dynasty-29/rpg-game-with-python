import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Load a single player image
        self.original_image = pygame.image.load('assets/player.jpg').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Set mask for better collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # Player stats
        self.speed = 5
        self.max_health = 100
        self.health = self.max_health
        self.invincible = False
        self.invincible_timer = 0
        self.facing_right = True
        
    def update(self):
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Reset movement variables
        dx, dy = 0, 0
        
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.facing_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            
        # Update position
        self.rect.x += dx
        self.rect.y += dy
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            
        # Handle facing direction
        if not self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image
        
        # Handle invincibility frames
        if self.invincible:
            self.invincible_timer += 1
            # Flash the player to indicate invincibility
            if self.invincible_timer % 6 < 3:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
                
            if self.invincible_timer >= 60:  # 1 second of invincibility
                self.invincible = False
                self.invincible_timer = 0
                self.image.set_alpha(255)
        
        # Update mask for better collision
        self.mask = pygame.mask.from_surface(self.image)
        
    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)