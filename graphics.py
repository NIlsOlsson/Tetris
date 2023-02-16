import numpy as np
import pygame


class Graphics:
    border_width = 1

    window_height = 0
    window_width = 0
    cell_size = 0

    def __init__(self, rows, cols, screen):
        self.images = None
        self.rows = rows
        self.cols = cols
        self.screen = screen

        self.load_images()

    def load_images(self):
        self.images = {"blue block": pygame.image.load('images/blue_tetris_block.png'),
                       "green block": pygame.image.load('images/green_tetris_block.png'),
                       "purple block": pygame.image.load('images/purple_tetris_block.png'),
                       "red block": pygame.image.load('images/red_tetris_block.png'),
                       "yellow block": pygame.image.load('images/yellow_tetris_block.png'),
                       "orange block": pygame.image.load('images/orange_tetris_block.png'),
                       "pink block": pygame.image.load('images/pink_tetris_block.png')}

    def repaint(self, board, score):
        if board.shape != (self.rows, self.cols):
            raise ValueError("Board shape does not match graphics board shape")
        self.update_scale(self.screen.get_height(), self.screen.get_width())
        self.screen.fill((250, 250, 250))
        side_margin, top_margin = self.get_margins()
        self.paint_background(side_margin, top_margin)
        self.paint_filled_cells(board, side_margin + self.cell_size * self.border_width,
                                top_margin + self.cell_size * self.border_width)
        self.paint_score(score, top_margin)

    def update_scale(self, height, width):
        if self.window_height == height and self.window_width == width:
            return
        self.window_height = height
        self.window_width = width
        self.cell_size = round(self.get_cell_size())
        self.scale_images()

    def scale_images(self):
        self.load_images()
        for key in self.images:
            self.images[key] = pygame.transform.smoothscale(self.images[key], (self.cell_size, self.cell_size))

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
                             (side_margin + w, top_margin + w,
                              self.cell_size * (self.cols + self.border_width * 2) - 2 * w,
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
                             (x + i * self.cell_size, top_margin + border_pixels, line_width,
                              self.cell_size * self.rows))
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
            self.screen.blit(self.images["blue block"], (x, y))
        elif color == 2:
            self.screen.blit(self.images["green block"], (x, y))
        elif color == 3:
            self.screen.blit(self.images["purple block"], (x, y))
        elif color == 4:
            self.screen.blit(self.images["red block"], (x, y))
        elif color == 5:
            self.screen.blit(self.images["yellow block"], (x, y))
        elif color == 6:
            self.screen.blit(self.images["orange block"], (x, y))
        elif color == 7:
            self.screen.blit(self.images["pink block"], (x, y))

    def paint_score(self, score, top_margin):
        x = self.window_width / 2 - 2 * self.cell_size
        y = top_margin + self.cell_size * self.border_width / 2
        width = 4 * self.cell_size
        height = 3 / 2 * self.cell_size
        self.paint_score_border(x, y, width, height, self.cell_size / 4)
        font = pygame.font.SysFont("comicsans", self.cell_size)
        text = font.render(str(score), True, (0, 0, 0))
        text_width, text_height = font.size(str(score))
        text_x = x + (width - text_width) / 2
        text_y = y + (height - text_height) / 2
        self.screen.blit(text, (text_x, text_y))

    def paint_score_border(self, x, y, width, height, border_width):
        for i in range(0, 11):
            w = border_width / 4 + border_width * i / 10
            color_value = 80 + 12 * (11 - (i / 2 - 5 / 2) ** 2)
            color = (color_value, color_value, color_value)
            pygame.draw.rect(self.screen, color,
                             (x + w, y + w, width - 2 * w,
                              height - 2 * w))
        pygame.draw.rect(self.screen, (235, 235, 235),
                         (x + border_width, y + border_width, width - 2 * border_width,
                          height - 2 * border_width))
