import numpy as np
import pygame


class Graphics:
    border_width = 1

    window_height = 0
    window_width = 0
    cell_size = 0

    def __init__(self, rows, cols, screen):
        self.image = None
        self.rows = rows
        self.cols = cols
        self.screen = screen

        self.load_images()

    def load_images(self):
        self.image = {"blue block": pygame.image.load('images/blue_tetris_block.png'),
                      "green block": pygame.image.load('images/green_tetris_block.png'),
                      "purple block": pygame.image.load('images/purple_tetris_block.png'),
                      "red block": pygame.image.load('images/red_tetris_block.png'),
                      "yellow block": pygame.image.load('images/yellow_tetris_block.png'),
                      "orange block": pygame.image.load('images/orange_tetris_block.png'),
                      "pink block": pygame.image.load('images/pink_tetris_block.png')}

    def repaint(self, board):
        if board.shape != (self.rows, self.cols):
            raise ValueError("Board shape does not match graphics board shape")
        self.update_scale(self.screen.get_height(), self.screen.get_width())
        self.screen.fill((250, 250, 250))
        side_margin, top_margin = self.get_margins()
        self.paint_background(side_margin, top_margin)
        self.paint_filled_cells(board, side_margin + self.cell_size * self.border_width,
                                top_margin + self.cell_size * self.border_width)

    def update_scale(self, height, width):
        if self.window_height == height and self.window_width == width:
            return
        self.window_height = height
        self.window_width = width
        self.cell_size = round(self.get_cell_size())
        self.scale_images()

    def scale_images(self):
        self.load_images()
        for key in self.image:
            self.image[key] = pygame.transform.smoothscale(self.image[key], (self.cell_size, self.cell_size))

    def get_cell_size(self):
        height_width_ratio = (self.rows + self.border_width * 2) / (self.cols + self.border_width * 2)
        actual_height = np.min([self.window_height, self.window_width * height_width_ratio])
        return actual_height / (self.rows + self.border_width * 2)

    def get_margins(self):  # returns (side, top)
        return ((self.window_width - self.cell_size * (self.cols + self.border_width * 2)) / 2,
                (self.window_height - self.cell_size * (self.rows + self.border_width * 2)) / 2)

    def paint_background(self, side_margin, top_margin):
        border_pixels = self.cell_size * self.border_width
        for i in range(0, 11):
            w = border_pixels / 4 + border_pixels * i / 10
            color_value = 80 + 12 * (11 - (i / 2 - 5 / 2) ** 2)
            color = (color_value, color_value, color_value)
            pygame.draw.rect(self.screen, color,
                             (side_margin + w, top_margin + w, self.cell_size * (self.cols + self.border_width * 2) - 2 * w,
                              self.cell_size * (self.rows + self.border_width * 2) - 2 * w))
        pygame.draw.rect(self.screen, (240, 240, 240),
                         (side_margin + border_pixels, top_margin + border_pixels, self.cell_size * self.cols,
                          self.cell_size * self.rows))
        self.paint_lines(side_margin, top_margin)

    def paint_lines(self, side_margin, top_margin):
        line_color_value = 230
        line_color = (line_color_value, line_color_value, line_color_value)
        border_pixels = self.cell_size * self.border_width
        line_width = self.cell_size / 10
        x = side_margin + border_pixels - line_width / 2
        for i in range(1, self.cols):
            pygame.draw.rect(self.screen, line_color,
                             (x + i * self.cell_size, top_margin + border_pixels, line_width, self.cell_size * self.rows))
        y = top_margin + border_pixels - line_width / 2
        for i in range(1, self.rows):
            pygame.draw.rect(self.screen, line_color, (
                side_margin + border_pixels, y + i * self.cell_size, self.cell_size * self.cols, line_width))

    def paint_filled_cells(self, board, start_x, start_y):
        x, y = start_x, start_y
        for row in board:
            for col in row:
                if not col == 0:
                    self.fill_cell(x, y, col)
                x += self.cell_size
            x = start_x
            y += self.cell_size

    def fill_cell(self, x, y, color):
        if color == 1:
            self.screen.blit(self.image["blue block"], (x, y))
        elif color == 2:
            self.screen.blit(self.image["green block"], (x, y))
        elif color == 3:
            self.screen.blit(self.image["purple block"], (x, y))
        elif color == 4:
            self.screen.blit(self.image["red block"], (x, y))
        elif color == 5:
            self.screen.blit(self.image["yellow block"], (x, y))
        elif color == 6:
            self.screen.blit(self.image["orange block"], (x, y))
        elif color == 7:
            self.screen.blit(self.image["pink block"], (x, y))

