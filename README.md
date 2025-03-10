# RPG game - Phase3 Personal Project

This RPG is a 2D top-down adventure game where you control a character in a dangerous world filled with enemies. Collect coins to increase your score and health, while avoiding or defeating increasingly difficult enemies. The game features progressive difficulty with enemies growing stronger as you level up.

### Sneek Peak of how the game looks like
Frame 1| Frame 2| Frame 3| End Screen|
|![alt text](<Screenshot (30).png>)|![alt text](<Screenshot (31).png>)|![alt text](<Screenshot (32).png>)|![alt text](<Screenshot (29).png>)|
### My File Structure:

* main.py: Entry point to start the game
* game.py: Main game class that handles game loop and logic
* player.py: Player class with movement, animation, and health mechanics
* enemy.py: Enemy class that scales with difficulty
* coin.py: Collectible items 
* settings.py: Game constants and configuration

## Game Mechanics

### Player
- Move in four directions using WASD or arrow keys
- Health bar displays current health status
- Collect coins to increase score
- Every 10 coins collected:
  - Gain 20 health points
  - Level up, increasing game difficulty

### Enemies
- Enemies attack the player from all sides
- They increase with increase in level making it harder for the player

### Coins
- Player aims to collect 10 coins to get to next level.
- The more the coins they collect help in rejuvenating their health back after enemy attacks

### Game Progression
- Game difficulty increases with each level




## Controls
- **Movement**: WASD or Arrow keys

## How to Play
1. Run the game using Python: `python main.py`
2. Move your character to collect coins
3. Avoid enemies or they will damage your health
4. Survive as long as possible and achieve a high score

## How to Win
The game is an endless survival challenge. Your goal is to achieve the highest score and level possible before losing all health.

## How to Defeat Enemies
This is a survival game - your primary strategy should be to avoid enemies rather than defeat them directly. As you collect coins and progress through levels, enemies become more challenging, requiring better evasive maneuvers.

## Requirements
- Python 3.6+
- Pygame library

## Installation
1. Clone the repository
2. Install the required packages: `pip install pygame`
3. Run the game: `python main.py`

## Tips & Strategies
- Keep moving to avoid enemies
- Prioritize coin collection to level up and gain health
- Use the edges of the screen strategically - enemies spawn from outside
- Watch for the invincibility period after taking damage (player flashes)
- Plan escape routes, especially as enemies get faster at higher levels

## Credit and References
* Created as a beginner-friendly game project using Python and Pygame.
* I was able to achieve this through useful detailed information in following pages: 
            1. https://www.pygame.org/docs/
            2. https://github.com/pygame/pygame
            3. https://www.geeksforgeeks.org/pygame-tutorial/
