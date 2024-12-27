import pygame
from pygame import Surface, Rect
from .constants import *
from .game import Game2048

class GameRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("2048")
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.message_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE * 2)  # Larger font for messages
        
    def draw_game(self, game: Game2048):
        self.screen.fill(pygame.Color(COLORS['background']))
        
        for i in range(4):
            for j in range(4):
                value = game.matrix[i][j]
                cell_rect = Rect(
                    j * CELL_SIZE + PADDING,
                    i * CELL_SIZE + PADDING,
                    CELL_SIZE - 2 * PADDING,
                    CELL_SIZE - 2 * PADDING
                )
                
                # Draw cell background
                color = COLORS.get(value, COLORS['empty_cell'])
                pygame.draw.rect(self.screen, pygame.Color(color), cell_rect)
                
                # Draw value
                if value != 0:
                    text_color = TEXT_COLORS.get(value, TEXT_COLORS['default'])
                    text = self.font.render(str(value), True, pygame.Color(text_color))
                    text_rect = text.get_rect(center=cell_rect.center)
                    self.screen.blit(text, text_rect)
        
        # Draw score
        score_text = self.font.render(f"Score: {game.score}", True, pygame.Color(TEXT_COLORS['default']))
        self.screen.blit(score_text, (10, WINDOW_SIZE - 40))
        
        # Draw message if exists
        if game.current_message:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            # Message text
            message_text = self.message_font.render(game.current_message, True, pygame.Color(TEXT_COLORS['default']))
            message_rect = message_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            self.screen.blit(message_text, message_rect)
        
        pygame.display.flip()
