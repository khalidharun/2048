import random
from typing import List, Optional

class Game2048:
    def __init__(self):
        self.matrix: List[List[int]] = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.has_shown_16 = False
        self.init_game()

    def init_game(self):
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self) -> None:
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4


    def stack(self) -> None:
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self) -> None:
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.score += self.matrix[i][j]
                    self.matrix[i][j + 1] = 0
                    if self.matrix[i][j] == 2048 and not self.won:
                        self.won = True
                        messagebox.showinfo("Congratulations!", "You've won! You can continue playing to achieve a higher score.")

    def reverse(self) -> None:
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    def transpose(self) -> None:
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def move_left(self) -> None:
        old_matrix = [row[:] for row in self.matrix]
        self.stack()
        self.combine()
        self.stack()
        if self.matrix != old_matrix:
            self.add_new_tile()
        self.update_grid_cells()
        if not self.has_valid_moves() and not self.game_over:
            self.game_over = True
            messagebox.showinfo("Game Over!", f"No more moves available.\nFinal Score: {self.score}")

    def move_right(self) -> None:
        old_matrix = [row[:] for row in self.matrix]
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        if self.matrix != old_matrix:
            self.add_new_tile()
        self.update_grid_cells()
        if not self.has_valid_moves() and not self.game_over:
            self.game_over = True
            messagebox.showinfo("Game Over!", f"No more moves available.\nFinal Score: {self.score}")

    def move_up(self) -> None:
        old_matrix = [row[:] for row in self.matrix]
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        if self.matrix != old_matrix:
            self.add_new_tile()
        self.update_grid_cells()
        if not self.has_valid_moves() and not self.game_over:
            self.game_over = True
            messagebox.showinfo("Game Over!", f"No more moves available.\nFinal Score: {self.score}")

    def move_down(self) -> None:
        old_matrix = [row[:] for row in self.matrix]
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        if self.matrix != old_matrix:
            self.add_new_tile()
        self.update_grid_cells()
        if not self.has_valid_moves() and not self.game_over:
            self.game_over = True
            messagebox.showinfo("Game Over!", f"No more moves available.\nFinal Score: {self.score}")

    def handle_input(self, event_key: str) -> bool:
        """Returns True if the move was valid and changed the board"""
        old_matrix = [row[:] for row in self.matrix]
        
        if event_key == 'LEFT':
            self.move_left()
        elif event_key == 'RIGHT':
            self.move_right()
        elif event_key == 'UP':
            self.move_up()
        elif event_key == 'DOWN':
            self.move_down()
            
        return self.matrix != old_matrix

    def has_valid_moves(self) -> bool:
        """Check if any valid moves remain"""
        # Check for empty cells
        if any(0 in row for row in self.matrix):
            return True
            
        # Check for possible merges
        for i in range(4):
            for j in range(4):
                current = self.matrix[i][j]
                # Check right neighbor
                if j < 3 and current == self.matrix[i][j + 1]:
                    return True
                # Check bottom neighbor
                if i < 3 and current == self.matrix[i + 1][j]:
                    return True
        return False

    def is_game_over(self) -> bool:
        """Check if the game is over"""
        return not self.has_valid_moves()

    def check_win(self) -> bool:
        """Check if the player has won"""
        return self.won

if __name__ == '__main__':
    game = Game2048()
    game.window.mainloop()
