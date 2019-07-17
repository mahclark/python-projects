import pygame
import time

xSize, ySize = 600, 450
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pygame Template")

mx, my = pygame.mouse.get_pos()
mouseHold = False

#----------------------Main Loop----------------------#

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([255,255,255])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
