import pygame
import random
import math
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        super().__init__()
        
        # Load a single enemy image
        self.original_image = pygame.image.load('assets/enemy.jpg').convert_alpha()
        
        # Enemy stats based on level
        self.level = level
        self.size = 40 + (level * 5)  
        self.speed = 1 + (level * 0.2)  
        self.damage = 5 + (level * 2)  
        
        # Resize image based on enemy size
        self.original_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.image = self.original_image
        
        # Set up rect
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Set mask for better collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # Target for enemy to move towards (player position)
        self.target = None
        
    def update(self):
        # Find the player (assumed to be first sprite in all_sprites)
        if hasattr(self.groups()[0], 'sprites') and self.groups()[0].sprites():
            for sprite in self.groups()[0].sprites():
                if hasattr(sprite, 'speed') and hasattr(sprite, 'health'):
                    # This is likely the player
                    self.target = sprite.rect.center
                    break
        
        # Move towards the player
        if self.target:
            # Calculate direction vector
            dx = self.target[0] - self.rect.centerx
            dy = self.target[1] - self.rect.centery
            
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
        
        # Remove enemy if it goes too far off screen
        if (self.rect.right < -100 or self.rect.left > WIDTH + 100 or 
            self.rect.bottom < -100 or self.rect.top > HEIGHT + 100):
            self.kill()



