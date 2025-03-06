import pygame
import sys
import random
from player import Player
from enemy import Enemy
from coin import Coin
from settings import *

# Aim t have all game mechanics here 
class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dynasty's RPG")
        self.clock = pygame.time.Clock()
        
        # Load background
        self.background = pygame.image.load('assets/background3.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        # whats a game without background music
        # will be using pygame mixer to have background music and also sounds
        pygame.mixer.music.load('assets/background.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
        # game sound effects
        self.coin_sound = pygame.mixer.Sound('assets/coin.mp3')
        self.hit_sound = pygame.mixer.Sound('assets/hit.mp3')
        self.level_up_sound = pygame.mixer.Sound('assets/level_up.mp3')
        
        # Game variables
        self.score = 0
        self.level = 1
        self.game_over = False
        self.enemy_spawn_timer = 0
        self.coin_spawn_timer = 0
        
        # Create sprite groups that will store all resplicated sprites for spreadig functionality
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        # player
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.all_sprites.add(self.player)
        
        # Awesomeness of using artistic fonts
        self.font = pygame.font.Font("assets/Butcherman-Regular.ttf", 36)

    # making the player run for it by ejecting players from all sides
    def spawn_enemy(self):
        # randomly setting sides at intervals
        #  setting top as 1, bottom as 3, right as 2, and left as 4
        side = random.randint(1, 4)
        
        # condition for sides selection
        #  also setting values for x and y axises
        #  top
        if side == 1:  
            x = random.randint(0, WIDTH)
            y = -10
        # right 
        elif side == 2:  
            x = WIDTH + 10
            y = random.randint(0, HEIGHT)
        # bottom 
        elif side == 3: 
            x = random.randint(0, WIDTH)
            y = HEIGHT + 10
        # left 
        else:  
            x = -10
            y = random.randint(0, HEIGHT)
        
        # now lets create new enemies at each position set above 
        enemy = Enemy(x, y, self.level)
        
        #  onces created we add them to the game
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    # adding the fun of collection coins by spawning them randomly but making sure its not spawn close to enemy
    def spawn_coin(self):
        # Making sure coins don't spawn too close to enemies
        safe_spawn = False
        while not safe_spawn:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            
            # Check distance from enemies
            safe_spawn = True
            for enemy in self.enemies:
                distance = ((x - enemy.rect.centerx) ** 2 + (y - enemy.rect.centery) ** 2) ** 0.5
                if distance < 100:  # Minimum safe distance
                    safe_spawn = False
                    break
        
        # setting the coin object and where it will be spawaned at
        coin = Coin(x, y)
        #  adding this to coin sprite group
        self.all_sprites.add(coin)
        self.coins.add(coin)

    def handle_events(self):
        # my event handler 
        # making it posible to restart the game once its done or even quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_r:
                    self.__init__() 
    def handle_update(self):
        # to continously update the game logic
        if not self.game_over:
            # 1. always update all sprites
            self.all_sprites.update()
            
            # 2. Check for player collision with enemies
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
            for hit in hits:
                self.player.take_damage(hit.damage)
                # 3. Ensure the hit sound effect we added is effect when the collision happens
                self.hit_sound.play()
                
                # 4. Check if player is dead by checking lifes left
                if self.player.health <= 0:
                    self.game_over = True
            
            # 5. Check for player collection of coins whenever they come incontact with them
            coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
            for coin in coin_hits:
                self.score += 1
                #  as usual play the sound effect we set for this collection
                self.coin_sound.play()
                
                # 6. we need to boost player health for every 10 coins they collect
                if self.score % 10 == 0:
                    self.player.heal(20)
                    # 7. also leveling up
                    self.level += 1
                    #  leveling up sound effect
                    self.level_up_sound.play()
            
            # Spawn new enemies based on timer and level
            self.enemy_spawn_timer += 1
            #  more enemies spawning as leveling up happens
            if self.enemy_spawn_timer >= 180 - (self.level * 10):  
                self.enemy_spawn_timer = 0
                self.spawn_enemy()
            
            # Spawn new coins for every 2 seconds
            self.coin_spawn_timer += 1
            if self.coin_spawn_timer >= 120:  
                self.coin_spawn_timer = 0
                self.spawn_coin()

    def handle_draw(self):
        # Giving our game a background
        self.screen.blit(self.background, (0, 0))
        
        # Making the sprites visible on set screen
        self.all_sprites.draw(self.screen)
        
        # showing scores, level and life infomation on the screen 
        self.draw_ui()
        
        # Showing game overscreen onces player is defeated
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()

    def draw_ui(self):
        # How the scores will appear
        score_text = self.font.render(f"Score: {self.score}", True, MAGENTA)
        self.screen.blit(score_text, (20, 20))
        
        # How level display will appear
        level_text = self.font.render(f"Level: {self.level}", True, MAGENTA)
        self.screen.blit(level_text, (20, 60))
        
        # health bar
        health_pct = self.player.health / self.player.max_health
        bar_width = 200
        fill_width = int(bar_width * health_pct)
        
        # where to place them on the screen
        outline_rect = pygame.Rect(WIDTH - bar_width - 20, 20, bar_width, 20)
        fill_rect = pygame.Rect(WIDTH - bar_width - 20, 20, fill_width, 20)
        
        # aesthetic of the health bar
        pygame.draw.rect(self.screen, RED, fill_rect)
        pygame.draw.rect(self.screen, BLUE, outline_rect, 2)
        
        # health text am calling it life
        health_text = self.font.render(f"LIFE: {self.player.health}/{self.player.max_health}", True, MAGENTA)
        self.screen.blit(health_text, (WIDTH - bar_width - 20, 45))

    def draw_game_over(self):
        # making the game-over screen appear as an overlay using SRCALPHA
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Bring all my UI text together
        game_over_text = self.font.render("OOOPs!! GAME OVER MATE", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, CYAN)
        level_text = self.font.render(f"Final Level: {self.level}", True, WHITE)
        restart_text = self.font.render("Press R to Restart", True, GREEN)
        
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))
        self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

    def run(self):
        # handling all above function 
        while True:
            self.handle_events()
            self.handle_update()
            self.handle_draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()