# Aim to have collectables inthe game
import pygame
import math
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Load a single coin image
        self.image = pygame.image.load('assets/coin.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        
        # Set up rect
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # For floating animation
        self.float_offset = 0
        self.original_y = y
        
        # Set mask for better collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        # Floating animation (making the coin bob up and down)
        self.float_offset += 0.05
        self.rect.y = self.original_y + int(math.sin(self.float_offset) * 5)
        
        # Optional: Rotate the coin slightly
        # This would require saving the original image and rotating a copy
        
        # Update mask for better collision
        self.mask = pygame.mask.from_surface(self.image)