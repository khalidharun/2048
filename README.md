# 2048 Game

A Python implementation of the popular 2048 puzzle game using Tkinter for the graphical interface.

## Description

2048 is a single-player sliding tile puzzle game. The game's objective is to slide numbered tiles on a grid to combine them and create a tile with the number 2048.

## Game Mechanics

### Starting Conditions
- The game begins with a 4x4 grid
- Two tiles are randomly placed on the grid
- Each starting tile has a value of either 2 (90% probability) or 4 (10% probability)

### Gameplay Rules
1. **Movement**: Players can slide tiles in four directions (up, down, left, right) using arrow keys
2. **Merging Tiles**:
   - When two tiles with the same number collide during a move, they merge into one tile
   - The value of the merged tile is the sum of the two original tiles
   - Each tile can only merge once per move
3. **New Tile Spawning**:
   - After each move, a new tile appears in an empty cell
   - New tiles have a value of either 2 (90% probability) or 4 (10% probability)
4. **Scoring**:
   - Score increases by the value of each merged tile
   - Example: Merging two 8 tiles adds 16 points to the score

### Win/Loss Conditions
- **Win**: Create a tile with the value 2048
- **Loss**: No valid moves remain (grid is full and no adjacent tiles can merge)

### Valid Moves
A move is considered valid if at least one of these conditions is met:
- Tiles can slide to empty spaces in the chosen direction
- Tiles with the same value can merge in the chosen direction

## Installation

```bash
# Clone the repository
git clone [repository-url]

# Install required dependencies
pip install pytest
```

## Running the Game

```bash
python game_2048.py
```

## Running Tests

```bash
pytest test_game_2048.py -v
```

## Controls
- ↑: Move tiles up
- ↓: Move tiles down
- ←: Move tiles left
- →: Move tiles right

## Implementation Details
The game is implemented using:
- Python 3
- Tkinter for GUI
- Pytest for testing

## Testing
The test suite covers:
- Initial game conditions
- Movement mechanics
- Merge rules
- Win condition
- Game over condition
- Valid move detection
- Score tracking
