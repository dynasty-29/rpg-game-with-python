import pygame
import random
import math
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, level, player=None):
        super().__init__()
        
        # Load a single enemy image
        self.original_image = pygame.image.load('assets/enemy.jpg').convert_alpha()
        
        # Enemy stats based on level
        self.level = level
        self.size = 40 + (level * 5)  
        self.speed = 1 + (level * 0.2)  
        self.damage = 5 + (level * 2)  
        
        # Adding enemy health attribute
        self.health = 30 + (level * 10)
        self.max_health = self.health
        
        # Resize image based on enemy size
        self.original_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.image = self.original_image
        
        # Set up rect
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Set mask for better collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # Store player reference
        self.player = player
        
        # Add knockback effect variables
        self.hurt_timer = 0
        self.knockback_dx = 0
        self.knockback_dy = 0
        
    def update(self):
        # Handle hurt timer and knockback effect
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            # Apply knockback movement
            self.rect.x += self.knockback_dx
            self.rect.y += self.knockback_dy
            
            # Flash red when hurt
            if self.hurt_timer % 6 < 3:
                self.image.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                self.image = self.original_image.copy()
                if self.knockback_dx < 0:
                    self.image = pygame.transform.flip(self.image, True, False)
            return 
        
            
        # Get target from player if available
        if self.player:
            target = self.player.rect.center
            
            # Calculate direction vector
            dx = target[0] - self.rect.centerx
            dy = target[1] - self.rect.centery
            
            # Normalize the direction
            distance = max(1, math.sqrt(dx * dx + dy * dy))
            dx = dx / distance
            dy = dy / distance
            
            # Move in the direction of the player
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            
            # Flip the image based on movement direction
            if dx < 0:
                self.image = pygame.transform.flip(self.original_image, True, False)
            else:
                self.image = self.original_image
        
        # Update mask for better collision
        self.mask = pygame.mask.from_surface(self.image)
        
        # Keep enemy within play area with a margin
        margin = 50
        if self.rect.left < margin:
            self.rect.left = margin
        if self.rect.right > WIDTH - margin:
            self.rect.right = WIDTH - margin
        if self.rect.top < margin:
            self.rect.top = margin
        if self.rect.bottom > HEIGHT - margin:
            self.rect.bottom = HEIGHT - margin
            
    def take_damage(self, amount):
        # Apply damage to enemy
        self.health -= amount
        
        # Set hurt timer and visual effect
        self.hurt_timer = 15
        
        # Calculate knockback direction (away from player)
        if self.player:
            dx = self.rect.centerx - self.player.rect.centerx
            dy = self.rect.centery - self.player.rect.centery
            
            # Normalize and set knockback strength
            distance = max(1, math.sqrt(dx * dx + dy * dy))
            self.knockback_dx = (dx / distance) * 5
            self.knockback_dy = (dy / distance) * 5
        
        # Check if enemy is dead
        if self.health <= 0:
            self.kill()
            
    # Method to check if enemy is too far off screen
    def check_offscreen(self):
        if (self.rect.right < -100 or self.rect.left > WIDTH + 100 or 
            self.rect.bottom < -100 or self.rect.top > HEIGHT + 100):
            self.kill()
            return True
        return False
