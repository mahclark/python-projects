import pygame
import time
import os
from math import sqrt, tan, radians
from random import randint

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 1200, 600
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pygame Template")

def terminator(ox, oy, rad, angle, col):
    pygame.draw.circle(screen,[col[0]/10,col[1]/10,col[2]/10],(ox,oy),rad)
    angle -= int(angle/360)*360
    for y in range(oy - rad, oy + rad):
        if angle <= 90:
            inter = (rad*rad - (y - oy)*(y - oy))/(tan(radians(angle) + 0.000001) + 1)
            x = ox + sqrt(abs(inter))*inter/abs(inter + 0.00001)
        elif angle >= 270:
            inter = (rad*rad - (y - oy)*(y - oy))/(tan(radians(-angle) + 0.000001) + 1)
            x = ox - sqrt(abs(inter))*inter/abs(inter + 0.00001)
        elif angle < 180:
            inter = (rad*rad - (y - oy)*(y - oy))/(tan(radians(-angle) + 0.000001) + 1)
            x = ox - sqrt(abs(inter))*inter/abs(inter + 0.00001)
        else:
            inter = (rad*rad - (y - oy)*(y - oy))/(tan(radians(angle) + 0.000001) + 1)
            x = ox + sqrt(abs(inter))*inter/abs(inter + 0.00001)
            
        try:
            if angle < 180:
                xs = x
                xe = ox + sqrt(rad*rad - pow(y - oy,2))
                pygame.draw.line(screen,col,(xs,y),(xe,y))
            else:
                xs = ox - sqrt(rad*rad - pow(y - oy,2))
                xe = x
                pygame.draw.line(screen,col,(xs,y),(xe,y))
        except: pass

#----------------------Main Loop----------------------#

ox, oy = 300,300
rad = 70

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 0.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([0,0,0])

    #pygame.draw.circle(screen,[92,135,45],(ox,oy),rad)

    print(frameCount - int(frameCount/360)*360)

    terminator(300,300,70,frameCount, [92,135,45])

##    for y in range(230,371):
##        for x in range(230,371):
##            if screen.get_at((x,y)) == (92,135,45):
##                light = False
##                dx = x - 300
##                r = sqrt(70*70 - pow(y - 300,2))
##                try:
##                    dy = sqrt(r*r - dx*dx)
##                    if frameCount - int(frameCount/360)*360 < 90 or frameCount - int(frameCount/360)*360 >= 270:
##                        if dy <= 10 + tan(radians(frameCount) + 0.000001)*dx:
##                            light = True
##                    else:
##                        if dy >= 10 + tan(radians(frameCount) + 0.000001)*dx:
##                            light = True
##                except: pass
##                if not light:
##                    screen.set_at((x,y),[9.2,13.5,4.5])

    if frameCount % 60 == 0: print("fps:",clock.get_fps())
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
