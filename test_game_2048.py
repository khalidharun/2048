import pytest
from game_2048 import Game2048
import tkinter as tk

@pytest.fixture
def game():
    game_instance = Game2048()
    yield game_instance
    game_instance.window.destroy()

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
    """Test basic movement mechanics"""
    # Set up a known board state
    game.matrix = [
        [2, 0, 0, 0],
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    
    # Test moving up (should combine the 2s)
    game.move_up()
    assert game.matrix[0][0] == 4

def test_merge_rules(game):
    """Test tile merging rules"""
    # Test that only same numbers merge
    game.matrix = [
        [2, 4, 2, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    game.move_left()
    assert game.matrix[0][:2] == [2, 4]
    
    # Test that merging happens only once per move
    game.matrix = [
        [2, 2, 2, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    game.move_left()
    assert game.matrix[0][:2] == [4, 4]

def test_win_condition(game):
    """Test win condition (reaching 2048)"""
    game.matrix = [
        [1024, 1024, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    game.move_left()
    assert game.matrix[0][0] == 2048
    assert game.check_win()

def test_game_over_condition(game):
    """Test game over condition"""
    # Fill board with unmergeable numbers
    game.matrix = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2]
    ]
    assert game.is_game_over()

def test_valid_moves(game):
    """Test valid move detection"""
    # Test a board where moves are possible
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
    game.move_left()
    assert game.score == initial_score + 4
