import pygame
import time
import colorsys

x, y, width, height = (16, 47, 832, 1486)

cell = 50
xSize, ySize = cell*7, cell*7

cols = [(114, 39, 107, 255), (228, 183, 122, 255), (126, 88, 92, 255), (140, 163, 180, 255), (125, 88, 95, 255), (222, 119, 138, 255), (118, 136, 150, 255), (127, 145, 157, 255), (120, 45, 114, 255), (245, 226, 202, 255), (69, 61, 60, 255), (142, 164, 181, 255), (59, 56, 53, 255), (215, 165, 116, 255), (120, 83, 90, 255), (214, 116, 133, 255), (235, 186, 126, 255), (244, 227, 203, 255), (236, 185, 126, 255), (121, 45, 113, 255), (64, 61, 60, 255), (211, 113, 132, 255), (123, 84, 93, 255), (121, 42, 111, 255), (219, 118, 140, 255), (63, 62, 59, 255), (138, 161, 175, 255), (214, 112, 136, 255), (242, 225, 201, 255), (64, 61, 58, 255), (143, 166, 180, 255), (127, 45, 121, 255), (248, 231, 205, 255), (241, 189, 133, 255), (131, 90, 98, 255), (63, 63, 63, 255), (139, 163, 177, 255), (222, 118, 139, 255), (129, 90, 97, 255), (127, 46, 119, 255), (131, 90, 98, 255), (254, 233, 208, 255), (221, 174, 120, 255), (241, 228, 200, 255), (65, 62, 61, 255), (241, 189, 133, 255), (224, 127, 141, 255), (249, 229, 198, 255), (113, 57, 91, 255)]

if __name__ == "__main__":
    screen = pygame.display.set_mode((xSize, ySize))
    pygame.display.set_caption("Pygame Template")

    clock = pygame.time.Clock()
    frameCount = 0
    done = False
    mouseHold = False
    while not done:
        frameCount += 1
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseHold = True
                # points.append((int(1000*mx/width)/1000, int(1000*my/height)/1000))

            if event.type == pygame.MOUSEBUTTONUP:
                mouseHold = False
                
        screen.fill([255,255,255])

        for y in range(7):
        	for x in range(7):
        		pygame.draw.rect(screen, cols[y*7 + x], (x*cell, y*cell, cell, cell))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()