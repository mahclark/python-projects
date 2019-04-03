import pygame
import os
import time
import math
import random
from random import randint
import sys
from ctypes import windll

def roll_text(string):
    text = ''
    for i in range(len(string)):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_ESCAPE]:
                print("pressed")
        print(string[i], end='', flush=True)
        time.sleep(0.04)

os.system('mode con: cols=70 lines=50')

dir_path = os.path.dirname(os.path.realpath(__file__))

if 'idlelib.run' in sys.modules:
    print("Run in CMD for optimised experience.")
    print("")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

setWindowPos = windll.user32.SetWindowPos
setWindowPos(pygame.display.get_wm_info()['window'], -1, 400, 300, 0, 0, 0x0001)

#Screen
infoObject = pygame.display.Info()
scrW, scrH = infoObject.current_w, infoObject.current_h
xShift = scrW/2 - 300
yShift = scrH/2 - 225
xSize, ySize = scrW, scrH#600, 450
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Mission_")

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
