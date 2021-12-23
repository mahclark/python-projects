import pygame
import time
import colorsys
from screen_capture import get_lonely_screen_id, get_phone_rect, save_img

hwnd = get_lonely_screen_id()
rect = get_phone_rect(hwnd)
save_img(hwnd)

x, y, width, height = rect

xSize, ySize = width, height
img = pygame.image.load("test.png")

points = [(0.425, 0.469), (0.451, 0.467), (0.538, 0.498), (0.625, 0.527), (0.711, 0.539), (0.799, 0.549), (0.943, 0.594), (0.316, 0.485), (0.405, 0.51), (0.49, 0.537), (0.58, 0.568), (0.664, 0.577), (0.75, 0.589), (0.836, 0.605), (0.268, 0.53), (0.355, 0.553), (0.442, 0.579), (0.531, 0.607), (0.615, 0.619), (0.704, 0.634), (0.789, 0.651), (0.221, 0.577), (0.307, 0.598), (0.394, 0.621), (0.48, 0.649), (0.567, 0.664), (0.655, 0.679), (0.742, 0.697), (0.174, 0.604), (0.262, 0.629), (0.344, 0.651), (0.435, 0.679), (0.522, 0.693), (0.609, 0.708), (0.693, 0.725), (0.122, 0.629), (0.211, 0.654), (0.298, 0.683), (0.385, 0.712), (0.471, 0.724), (0.557, 0.734), (0.645, 0.751), (0.131, 0.69), (0.163, 0.685), (0.25, 0.716), (0.337, 0.746), (0.423, 0.757), (0.51, 0.767), (0.59, 0.792)]

screen = pygame.display.set_mode((xSize, ySize))
screen.blit(img, (-x,-y))
screen_points = [(int(pp[0]*width), int(pp[1]*height)) for pp in points]
rgb_cols = [screen.get_at(pp) for pp in screen_points]

hsv_cols = [colorsys.rgb_to_hsv(r, g, b) for r, g, b, _ in rgb_cols]

if __name__ == "__main__":
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
                print((int(1000*mx/width)/1000, int(1000*my/height)/1000))

            if event.type == pygame.MOUSEBUTTONUP:
                mouseHold = False
                
        screen.fill([255,255,255])

        screen.blit(img, (-x,-y))
        for pp in screen_points:
        	screen.set_at(pp, (255,0,0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()