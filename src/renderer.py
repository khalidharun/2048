import pygame
from pygame import Surface, Rect
from .constants import *
from .game import Game2048

class GameRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))
        pygame.display.set_caption("2048")
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.title_font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE, bold=True)
        self.message_font = pygame.font.SysFont(FONT_NAME, int(FONT_SIZE * 1.5))  # Slightly smaller messages
        self.close_button_size = 20
        self.close_button_padding = 5
        
    def draw_game(self, game: Game2048):
        self.screen.fill(pygame.Color(COLORS['background']))
        
        # Draw title
        title_text = self.title_font.render("2048", True, pygame.Color(TEXT_COLORS['default']))
        title_rect = title_text.get_rect(centerx=WINDOW_SIZE // 2, top=10)
        self.screen.blit(title_text, title_rect)
        
        # Draw game grid
        for i in range(4):
            for j in range(4):
                value = game.matrix[i][j]
                cell_rect = Rect(
                    j * CELL_SIZE + PADDING,
                    i * CELL_SIZE + PADDING + GAME_AREA_TOP,  # Offset by title area
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
        self.screen.blit(score_text, (10, WINDOW_HEIGHT - 40))
        
        # Draw message if exists
        if game.current_message:
            # Message area with semi-transparent background
            message_area = pygame.Surface((WINDOW_SIZE, MESSAGE_AREA_HEIGHT))
            message_area.fill((0, 0, 0))
            message_area.set_alpha(180)
            message_y = GAME_AREA_TOP + (WINDOW_SIZE - MESSAGE_AREA_HEIGHT) // 2
            self.screen.blit(message_area, (0, message_y))
            
            # Draw close button
            close_x = WINDOW_SIZE - self.close_button_size - self.close_button_padding
            close_y = message_y + self.close_button_padding
            game.close_button_rect = self.draw_close_button(close_x, close_y)
            
            # Message text
            message_text = self.message_font.render(game.current_message, True, pygame.Color(TEXT_COLORS['default']))
            message_rect = message_text.get_rect(center=(WINDOW_SIZE // 2, message_y + MESSAGE_AREA_HEIGHT // 2))
            self.screen.blit(message_text, message_rect)
        
        pygame.display.flip()
        
    def draw_close_button(self, x, y):
        """Draw an X close button"""
        button_rect = Rect(x, y, self.close_button_size, self.close_button_size)
        pygame.draw.rect(self.screen, pygame.Color('darkgray'), button_rect)
        
        # Draw X
        x_color = pygame.Color('white')
        start_x, start_y = x + 5, y + 5
        size = self.close_button_size - 10
        pygame.draw.line(self.screen, x_color, (start_x, start_y), (start_x + size, start_y + size), 2)
        pygame.draw.line(self.screen, x_color, (start_x + size, start_y), (start_x, start_y + size), 2)
        
        return button_rect
