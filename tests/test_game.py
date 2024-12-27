import pytest
from src.game import Game2048

@pytest.fixture
def game():
    return Game2048()

def test_initial_conditions(game):
    """Test the game's initial state"""
    # Check grid size
    assert len(game.matrix) == 4
    assert len(game.matrix[0]) == 4

    # Count initial tiles
    non_zero_tiles = sum(1 for row in game.matrix for cell in row if cell != 0)
    assert non_zero_tiles == 2

    # Check that initial tiles are either 2 or 4
    valid_values = {2, 4}
    initial_values = {cell for row in game.matrix for cell in row if cell != 0}
    assert initial_values.issubset(valid_values)

def test_movement_mechanics(game):
    """Test all movement directions with various scenarios"""
    # Test Case 1: Basic left movement and merging
    game.matrix = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    game.handle_input('LEFT')
    assert game.matrix[0][0] == 4
    assert game.score == 4

    # Test Case 2: Multiple merges in one move
    game.matrix = [
        [2, 2, 2, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    game.handle_input('LEFT')
    assert game.matrix[0][:2] == [4, 4]
    assert game.score == 12  # Previous 4 + new 8

def test_win_condition(game):
    """Test win condition (reaching 2048)"""
    game.matrix = [
        [1024, 1024, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    game.handle_input('LEFT')
    assert game.matrix[0][0] == 2048
    assert game.check_win()

def test_game_over_condition(game):
    """Test game over condition"""
    game.matrix = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2]
    ]
    assert game.is_game_over()

def test_valid_moves(game):
    """Test valid move detection"""
    game.matrix = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    assert game.has_valid_moves()

def test_score_tracking(game):
    """Test score calculation"""
    game.matrix = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    initial_score = game.score
    game.handle_input('LEFT')
    assert game.score == initial_score + 4
