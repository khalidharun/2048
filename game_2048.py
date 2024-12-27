import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Optional

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048")
        self.grid_cells: List[List[tk.Label]] = []
        self.matrix: List[List[int]] = []
        self.score = 0
        self.game_over = False
        self.won = False
        self.init_grid()
        self.init_matrix()
        self.bind_keys()

    def init_grid(self):
        background = tk.Frame(
            self.window,
            bg='#92877d',
            width=400,
            height=400
        )
        background.grid()

        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = tk.Label(
                    background,
                    bg='#9e948a',
                    font=('Arial', 40, 'bold'),
                    width=4,
                    height=2
                )
                cell.grid(row=i, column=j, padx=5, pady=5)
                grid_row.append(cell)
            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid_cells()

    def add_new_tile(self) -> None:
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid_cells(self):
        for i in range(4):
            for j in range(4):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg='#9e948a')
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=self.get_cell_color(new_number),
                        fg=self.get_text_color(new_number)
                    )
        self.window.update_idletasks()

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
        self.reverse()
        self.move_left()
        self.reverse()

    def move_up(self) -> None:
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self) -> None:
        self.transpose()
        self.move_right()
        self.transpose()

    def bind_keys(self) -> None:
        self.window.bind('<Left>', lambda event: self.move_left())
        self.window.bind('<Right>', lambda event: self.move_right())
        self.window.bind('<Up>', lambda event: self.move_up())
        self.window.bind('<Down>', lambda event: self.move_down())

    @staticmethod
    def get_cell_color(number: int) -> str:
        cell_colors = {
            0: '#9e948a',
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
        return cell_colors.get(number, '#ff0000')

    @staticmethod
    def get_text_color(number: int) -> str:
        return '#776e65' if number <= 4 else '#f9f6f2'

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
