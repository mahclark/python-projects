import pygame
import time
import os
from math import sqrt, tan, radians, sin, pi
from random import randint

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 1200, 600
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pygame Template")

class Point2:
    x = 0
    y = 0

def terminator2(angle, radius, col, centre):
    pygame.draw.circle(screen,col,(centre.x, centre.y),radius)
    
    for y in range(2*radius):
        rowRadius = sqrt(radius**2 - (radius - y)**2)
##        lightLength = rowRadius + rowRadius*sin(angle - pi/2)
        darkLength = rowRadius - rowRadius*sin(angle - pi/2)
        if angle > pi:
##            lightStart = centre.x + rowRadius - lightLength
            darkStart = centre.x - rowRadius
        else:
##            lightStart = centre.x - rowRadius
            darkStart = centre.x + rowRadius*sin(angle - pi/2)
        pygame.draw.line(screen, [col[0]/10,col[1]/10,col[2]/10], (darkStart, centre.y - radius + y), (darkStart + darkLength, centre.y - radius + y))

        
    if angle < 0.1 or angle > 2*pi - 0.1:
        zeroAngle = angle
        if angle > pi: zeroAngle = angle - 2*pi
        f = 1 - abs(zeroAngle)/0.1
        pygame.draw.circle(screen,[col[0]*f,col[1]*f,col[2]*f],(centre.x, centre.y),radius)
        pygame.draw.circle(screen,[col[0]/10,col[1]/10,col[2]/10],(centre.x, centre.y),radius - 1)

#----------------------Main Loop----------------------#

ox, oy = 300,300
rad = 70
point = Point2()
point.x = 300
point.y = 300

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 0.51
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([0,0,0])

    angle = frameCount*pi/360
    while angle >= 2*pi: angle -= 2*pi
    
    terminator2(angle, 80, [92,135,45], point)

    print(angle*180/pi)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
