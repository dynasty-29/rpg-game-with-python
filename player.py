import pygame
from settings import *

class Player():
    def __init__(self, x, y):
        super().__init__()
        
        
        # Player stats
        self.speed = 5
        self.max_health = 100
        self.health = self.max_health
        self.invincible = False
        self.invincible_timer = 0
        self.facing_right = True
        
    def update(self):
        pass
        
    def take_damage(self):
        pass
            
    def heal(self):
       pass