import pygame
import time


if __name__ == "__main__":
    xSize, ySize = 600, 450
    screen = pygame.display.set_mode((xSize, ySize))
    pygame.display.set_caption("Pygame Template")

    clock = pygame.time.Clock()
    frameCount = 0
    done = False
    mouseHold = False
    while not done:
        frameCount += 1
        mx, my = pygame.mouse.get_pos()
        events = pygame.event.get()
        if len(events) > 0:
        	print(events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseHold = True
                print(event.button)

            if event.type == pygame.MOUSEBUTTONUP:
                mouseHold = False
                
        screen.fill([255,255,255])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
