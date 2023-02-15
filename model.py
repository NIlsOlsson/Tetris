import random
from copy import deepcopy

import numpy as np
import pygame


class Model:

    def __init__(self):
        self.game_board = GameBoard()
        self.current_block = Block(-1, 5)
        self.place_block()

    new_block_delay = 2
    counter = 0

    def tick(self):
        if not self.try_move("down"):
            if self.counter == self.new_block_delay:
                self.new_block()
                self.counter = 0
            else:
                self.counter += 1

    def new_block(self):
        filled_rows = [i for i, row in enumerate(self.game_board.board) if np.all(row != 0)]
        self.game_board.empty_rows(filled_rows)
        self.current_block = Block(-1, 5)

    def key_pressed(self, key):
        if key == pygame.K_LEFT:
            self.try_move("left")
        elif key == pygame.K_RIGHT:
            self.try_move("right")
        elif key == pygame.K_DOWN:
            self.try_move("down")
        elif key == pygame.K_UP:
            self.try_move("rotate")
        elif key == pygame.K_SPACE:
            self.fall()

    def try_move(self, direction):
        self.clear_block()
        test_block = deepcopy(self.current_block)
        test_block.move(direction)
        if not self.check_collision(test_block):
            self.current_block.move(direction)
            self.place_block()
            return True
        self.place_block()
        return False

    def fall(self):
        if self.try_move("down"):
            self.fall()

    def check_collision(self, block):
        for (row, col) in block.get_filled_cells():
            if row >= self.game_board.rows or col >= self.game_board.cols or col < 0:
                return True
            if self.within_board(row, col) and self.game_board.board[row][col] != 0:
                return True
        return False

    def clear_block(self):
        for (row, col) in self.current_block.get_filled_cells():
            if self.within_board(row, col):
                self.game_board.board[row][col] = 0

    def place_block(self):
        for (row, col) in self.current_block.get_filled_cells():
            if self.within_board(row, col):
                self.game_board.board[row][col] = self.current_block.get_color()

    def within_board(self, row, col):
        return 0 <= row < self.game_board.rows and self.game_board.cols > col >= 0

    def get_board(self):
        return self.game_board.board

    def get_score(self):
        return self.game_board.score


class Block:
    row = 0
    col = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.shape = random.choice(shapes)()

    def get_filled_cells(self):
        return [(i + self.row, j + self.col) for (i, j) in self.shape.normalized_cells]

    def get_color(self):
        return self.shape.color

    def move(self, direction):
        if direction == "down":
            self.row += 1
        elif direction == "left":
            self.col -= 1
        elif direction == "right":
            self.col += 1
        elif direction == "rotate":
            self.shape.rotate()
        else:
            raise Exception("Invalid command")


class Shape:
    normalized_cells = []
    color = 1

    def rotate(self):
        self.normalized_cells = [(i, -j) for (j, i) in self.normalized_cells]


class RightLShape(Shape):
    color = 3

    def __init__(self):
        self.normalized_cells = [(-2, 0), (-1, 0), (0, 0), (0, 1)]


class LeftLShape(Shape):
    color = 4

    def __init__(self):
        self.normalized_cells = [(-2, 1), (-1, 1), (0, 1), (0, 0)]


class SquareShape(Shape):
    color = 5

    def __init__(self):
        self.normalized_cells = [(-1, 0), (-1, 1), (0, 0), (0, 1)]


class LineShape(Shape):
    color = 1

    def __init__(self):
        self.normalized_cells = [(-3, 0), (-2, 0), (-1, 0), (0, 0)]


class RightZShape(Shape):
    color = 6

    def __init__(self):
        self.normalized_cells = [(-2, 0), (-1, 0), (-1, 1), (0, 1)]


class LeftZShape(Shape):
    color = 2

    def __init__(self):
        self.normalized_cells = [(-2, 1), (-1, 1), (-1, 0), (0, 0)]

class MountainShape(Shape):
    color = 7

    def __init__(self):
        self.normalized_cells = [(0, 0), (0, 1), (-1, 1), (0, 2)]


shapes = [RightLShape, LeftLShape, LineShape, SquareShape, RightZShape, LeftZShape, MountainShape]


class GameBoard:
    rows = 20
    cols = 10
    board = np.zeros((rows, cols))
    score = 0

    def empty_rows(self, rows):
        if not len(rows) == 0:
            self.score += len(rows)
            self.board = np.delete(self.board, rows, axis=0)
            self.board = np.concatenate((np.zeros((len(rows), self.cols)), self.board), axis=0)
