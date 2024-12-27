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
        current_time = pygame.time.get_ticks()
        
        # Clear message after 2 seconds
        if game.current_message and current_time - game.message_timer > 2000:
            game.current_message = None
        
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
                            game.current_message = "Achievement! You've reached 16!"
                            game.message_timer = current_time
                        
                        if game.check_win():
                            game.current_message = "Congratulations! You've won!"
                            game.message_timer = current_time
                        
                        if game.is_game_over():
                            game.current_message = f"Game Over! Final Score: {game.score}"
                            game.message_timer = current_time
        
        renderer.draw_game(game)
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
