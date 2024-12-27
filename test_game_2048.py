import unittest
from game_2048 import Game2048
import tkinter as tk

class TestGame2048(unittest.TestCase):
    def setUp(self):
        self.game = Game2048()
        
    def tearDown(self):
        self.game.window.destroy()

    def test_initial_conditions(self):
        """Test the game's initial state"""
        # Check grid size
        self.assertEqual(len(self.game.matrix), 4)
        self.assertEqual(len(self.game.matrix[0]), 4)
        
        # Count initial tiles
        non_zero_tiles = sum(1 for row in self.game.matrix for cell in row if cell != 0)
        self.assertEqual(non_zero_tiles, 2)
        
        # Check that initial tiles are either 2 or 4
        valid_values = {2, 4}
        initial_values = {cell for row in self.game.matrix for cell in row if cell != 0}
        self.assertTrue(initial_values.issubset(valid_values))

    def test_movement_mechanics(self):
        """Test basic movement mechanics"""
        # Set up a known board state
        self.game.matrix = [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        # Test moving up (should combine the 2s)
        self.game.move_up()
        self.assertEqual(self.game.matrix[0][0], 4)
        
    def test_merge_rules(self):
        """Test tile merging rules"""
        # Test that only same numbers merge
        self.game.matrix = [
            [2, 4, 2, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move_left()
        self.assertEqual(self.game.matrix[0][:2], [2, 4])
        
        # Test that merging happens only once per move
        self.game.matrix = [
            [2, 2, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move_left()
        self.assertEqual(self.game.matrix[0][:2], [4, 4])

    def test_win_condition(self):
        """Test win condition (reaching 2048)"""
        self.game.matrix = [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move_left()
        self.assertEqual(self.game.matrix[0][0], 2048)
        self.assertTrue(self.game.check_win())

    def test_game_over_condition(self):
        """Test game over condition"""
        # Fill board with unmergeable numbers
        self.game.matrix = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.assertTrue(self.game.is_game_over())

    def test_valid_moves(self):
        """Test valid move detection"""
        # Test a board where moves are possible
        self.game.matrix = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertTrue(self.game.has_valid_moves())

    def test_score_tracking(self):
        """Test score calculation"""
        self.game.matrix = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        initial_score = self.game.score
        self.game.move_left()
        self.assertEqual(self.game.score, initial_score + 4)

if __name__ == '__main__':
    unittest.main()
