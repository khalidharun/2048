# Window settings
WINDOW_SIZE = 600
WINDOW_HEIGHT = 700  # Increased height to accommodate title
TITLE_HEIGHT = 80  # Increased to accommodate score
SCORE_FONT_SIZE = 24  # New smaller font size for score
GAME_AREA_TOP = TITLE_HEIGHT + 20
TITLE_FONT_SIZE = 48
MESSAGE_AREA_HEIGHT = 60  # Reduced height for message area
MESSAGE_FONT_SIZE = 28  # Smaller font size for messages
GRID_SIZE = 4
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
PADDING = 10

# Colors (using similar colors to original)
COLORS = {
    'background': '#92877d',
    'empty_cell': '#9e948a',
    2: '#eee4da',
    4: '#ede0c8',
    8: '#f2b179',
    16: '#f59563',
    32: '#f67c5f',
    64: '#f65e3b',
    128: '#edcf72',
    256: '#edcc61',
    512: '#edc850',
    1024: '#edc53f',
    2048: '#edc22e'
}

TEXT_COLORS = {
    2: '#776e65',
    4: '#776e65',
    'default': '#f9f6f2'
}

# Font settings
FONT_SIZE = CELL_SIZE // 3
FONT_NAME = 'Arial'
