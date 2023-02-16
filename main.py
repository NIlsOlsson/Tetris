import pygame

from graphics import Graphics
from model import GameBoard, Model

pygame.init()

screen = pygame.display.set_mode((500, 600), pygame.RESIZABLE)

clock = pygame.time.Clock()


pygame.display.set_caption("Tetris")

gameRate = 10
rateCounter = 0

d, l, r = 0, 0, 0

graphics = Graphics(20, 10, screen)
model = Model()

graphics.repaint(model.get_board(), model.get_score())
pygame.display.flip()

paused = True
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if paused:
                if event.key == pygame.K_SPACE:
                    paused = False
            else:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                else:
                    model.key_pressed(event.key)
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


    if not paused:
        if rateCounter == gameRate:
            rateCounter = 0
            model.tick()
        else:
            rateCounter += 1

    graphics.repaint(model.get_board(), model.get_score())
    pygame.display.flip()

pygame.quit()
