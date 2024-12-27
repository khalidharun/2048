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
    """Test all movement directions with various scenarios"""
    
    def reset_board(matrix):
        game.matrix = [row[:] for row in matrix]
        game.score = 0
    
    # Test Case 1: Basic left movement and merging
    test_board = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    reset_board(test_board)
    game.move_left()
    assert game.matrix[0][0] == 4, "Failed to merge tiles moving left"
    assert game.score == 4, "Score not updated correctly after merge"

    # Test Case 2: Multiple merges in one move
    test_board = [
        [2, 2, 2, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    reset_board(test_board)
    game.move_left()
    assert game.matrix[0][:2] == [4, 4], "Failed to properly merge multiple pairs"
    assert game.score == 8, "Score not updated correctly after multiple merges"

    # Test Case 3: No valid moves
    test_board = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2]
    ]
    reset_board(test_board)
    original = [row[:] for row in test_board]
    game.move_left()
    assert game.matrix == original, "Board changed when no valid moves possible"

def test_directional_movement(game):
    """Test all directional movements thoroughly"""
    
    def assert_movement_correct(actual, expected, message):
        # Check that all expected merges and moves happened
        for i in range(4):
            for j in range(4):
                if expected[i][j] != 0:  # Only check non-zero positions
                    assert actual[i][j] == expected[i][j], f"{message}\nExpected {expected[i][j]} at position ({i},{j}), got {actual[i][j]}"
    
    # Test LEFT movement
    game.matrix = [
        [0, 2, 2, 4],
        [0, 2, 0, 2],
        [2, 0, 2, 0],
        [4, 0, 0, 4]
    ]
    expected_left = [
        [4, 4, 0, 0],
        [4, 0, 0, 0],
        [4, 0, 0, 0],
        [8, 0, 0, 0]
    ]
    game.move_left()
    assert_movement_correct(game.matrix, expected_left, "Left movement failed")

    # Test RIGHT movement
    game.matrix = [
        [4, 2, 2, 0],
        [2, 0, 2, 0],
        [0, 2, 0, 2],
        [4, 0, 0, 4]
    ]
    expected_right = [
        [0, 0, 4, 4],
        [0, 0, 0, 4],
        [0, 0, 0, 4],
        [0, 0, 0, 8]
    ]
    game.move_right()
    assert_movement_correct(game.matrix, expected_right, "Right movement failed")

    # Test UP movement
    game.matrix = [
        [0, 2, 4, 2],
        [0, 2, 4, 2],
        [2, 0, 0, 4],
        [2, 4, 0, 4]
    ]
    expected_up = [
        [4, 8, 8, 2],
        [0, 0, 0, 8],
        [0, 0, 0, 2],
        [0, 0, 0, 0]
    ]
    game.move_up()
    assert_movement_correct(game.matrix, expected_up, "Up movement failed")

    # Test DOWN movement
    game.matrix = [
        [2, 4, 0, 4],
        [2, 0, 0, 4],
        [0, 2, 4, 2],
        [0, 2, 4, 2]
    ]
    expected_down = [
        [0, 0, 0, 0],
        [0, 0, 0, 2],
        [0, 0, 0, 8],
        [4, 8, 8, 2]
    ]
    game.move_down()
    assert_movement_correct(game.matrix, expected_down, "Down movement failed")

    # Test complex scenarios
    # Test merging prevention after one merge
    game.matrix = [
        [2, 2, 2, 2],
        [4, 4, 4, 4],
        [8, 8, 8, 8],
        [16, 16, 16, 16]
    ]
    expected_right = [
        [0, 0, 4, 4],
        [0, 0, 8, 8],
        [0, 0, 16, 16],
        [0, 0, 32, 32]
    ]
    game.move_right()
    assert_movement_correct(game.matrix, expected_right, "Complex right movement failed")

    # Test no movement when already aligned
    game.matrix = [
        [0, 0, 2, 4],
        [0, 0, 4, 8],
        [0, 0, 8, 16],
        [0, 0, 16, 32]
    ]
    expected_no_change = [row[:] for row in game.matrix]
    game.move_right()
    assert_movement_correct(game.matrix, expected_no_change, "Unnecessary movement occurred")

def test_movement_edge_cases(game):
    """Test edge cases in movement mechanics"""
    
    # Test merging prevention after one merge
    game.matrix = [
        [2, 2, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    game.move_left()
    assert game.matrix[0][:2] == [4, 2], "Multiple merges occurred in single move"

    # Test preservation of unmergeable sequences
    game.matrix = [
        [2, 4, 2, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    original_first_row = game.matrix[0][:]
    game.move_left()
    assert game.matrix[0][:4] == original_first_row, "Unmergeable sequence was modified"

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

def test_stack_method(game):
    """Test the stack method"""
    game.matrix = [
        [0, 2, 0, 4],
        [0, 0, 0, 2],
        [0, 0, 2, 0],
        [2, 0, 0, 0]
    ]
    game.stack()
    expected = [
        [2, 4, 0, 0],
        [2, 0, 0, 0],
        [2, 0, 0, 0],
        [2, 0, 0, 0]
    ]
    assert game.matrix == expected, "Stack method failed to move numbers correctly"

def test_combine_method(game):
    """Test the combine method"""
    game.matrix = [
        [2, 2, 4, 4],
        [2, 2, 2, 2],
        [4, 4, 0, 0],
        [2, 0, 0, 0]
    ]
    initial_score = game.score
    game.combine()
    expected = [
        [4, 0, 8, 0],
        [4, 0, 4, 0],
        [8, 0, 0, 0],
        [2, 0, 0, 0]
    ]
    assert game.matrix == expected, "Combine method failed to merge numbers correctly"
    assert game.score == initial_score + 28, "Score not updated correctly after combines"

def test_reverse_method(game):
    """Test the reverse method"""
    game.matrix = [
        [2, 0, 0, 4],
        [0, 2, 4, 0],
        [0, 0, 2, 0],
        [4, 2, 0, 2]
    ]
    expected = [
        [4, 0, 0, 2],
        [0, 4, 2, 0],
        [0, 2, 0, 0],
        [2, 0, 2, 4]
    ]
    game.reverse()
    assert game.matrix == expected, "Reverse method failed to reverse rows correctly"

def test_transpose_method(game):
    """Test the transpose method"""
    game.matrix = [
        [2, 0, 0, 4],
        [0, 2, 4, 0],
        [0, 0, 2, 0],
        [4, 2, 0, 2]
    ]
    expected = [
        [2, 0, 0, 4],
        [0, 2, 0, 2],
        [0, 4, 2, 0],
        [4, 0, 0, 2]
    ]
    game.transpose()
    assert game.matrix == expected, "Transpose method failed to transpose matrix correctly"
