import pygame
from pygame.locals import *
from .game import Game2048
from .renderer import GameRenderer

def main():
    game = Game2048()
    renderer = GameRenderer()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                key_map = {
                    K_LEFT: 'LEFT',
                    K_RIGHT: 'RIGHT',
                    K_UP: 'UP',
                    K_DOWN: 'DOWN'
                }
                
                if event.key in key_map:
                    if game.handle_input(key_map[event.key]):
                        # Check achievements/win condition after valid move
                        if any(16 in row for row in game.matrix) and not game.has_shown_16:
                            game.has_shown_16 = True
                            print("Achievement! You've reached 16!")
                        
                        if game.check_win():
                            print("Congratulations! You've won!")
                        
                        if game.is_game_over():
                            print(f"Game Over! Final Score: {game.score}")
                            running = False
        
        renderer.draw_game(game)
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
