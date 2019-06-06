import pygame
import time
import math
from math import sqrt, radians, sin, cos
import random
from random import randint as ri

pygame.init()

xSize, ySize = 600, 900
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Learn to Fly")

def get_end(length,angle,px0,py0):
    py = length*cos(radians(angle)) + py0
    px = length*sin(radians(angle)) + px0
    
    return int(px),int(py)

def get_ang(flap, time):
    time -= int(time/flap[1])*flap[1]
    gap = flap[1]/flap[0]
    sec = int(time/gap)
    
    y = (flap[sec+3]-flap[sec+2])*(time-sec*gap)/gap + flap[sec+2]
    return y

def create_flap(flap, breed):
    if breed:
        flap1,flap2 = flap[0],flap[1]

        timed = ri(-10,10)
        
        r1 = [abs(int(ri(-6,6)/5)+flap1[0]-1)+1, abs(timed+int(ri(-6,6)/5)+flap1[1]-20)+20]
        r2 = [abs(int(ri(-6,6)/5)+flap2[0]-1)+1, abs(timed+int(ri(-6,6)/5)+flap2[1]-20)+20]
        
        for i in range(r1[0]):
            r1.append(abs(ri(-10,10)+flap1[i+2]))
        r1.append(r1[2])
        
        for i in range(r2[0]):
            r2.append(abs(ri(-10,10)+flap2[i+2]))
        r2.append(r2[2])
        
    else:
        r1 = [ri(2,10), ri(30,180)] #[number, time period]
        r2 = [ri(2,10), ri(30,180)]

        for i in range(r1[0]):
            r1.append(ri(0,180))
        r1.append(r1[2])
        
        for i in range(r2[0]):
            r2.append(ri(0,180))
        r2.append(r2[2])
        
    return r1,r2
    
#Variables

length = 100
ox, oy = 300,ySize-200
px1, py1 = ox, oy
px2, py2 = 500,200
px3, py3 = 0,0

max_y = ySize
max_flap = [[],[]]
b_flap = [24, 98, 295, 14, 205, 173, 202, 80, 14, 121, 68, 162, 96, 322, 266, 276, 274, 271, 270, 279, 282, 284, 252, 273, 259, 283, 295], [11, 148, 155, 87, 92, 79, 37, 96, 210, 176, 174, 166, 178, 155]
#[4, 48, 175, 4, 186, 185, 175], [8, 47, 172, 188, 179, 10, 11, 185, 177, 174, 172]#create_flap(max_flap, False)
#[4, 48, 175, 4, 186, 185, 175], [8, 47, 172, 188, 179, 10, 11, 185, 177, 174, 172]
r1,r2 = create_flap(b_flap, True)

t1 = get_ang(r1, 0)
t2 = get_ang(r2, 0)
px3,py3 = get_end(length,t1,px1,py1)
px2,py2 = get_end(length,180-t2+t1,px3,py3)
ppx,ppy = px2,py2

gen = 1
org = 0

#----------------------Main Loop----------------------#
clock = pygame.time.Clock()
frameCount = 0
mouseHold = False
done = False
t = 1.333
t2 = -170
while not done:
    frameCount += 1
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([255,255,255])

    t1 = -get_ang(r1, frameCount)
    t2 = get_ang(r2, frameCount)
    
    px3,py3 = get_end(length,t1,px1,py1)
    px2,py2 = get_end(length,180-t2+t1,px3,py3)

    if frameCount > 2:
        diff = (py2 - ppy)*(px2 - px1)/200
        
        if py1 < ySize and py2 < ySize and py3 < ySize:
            py1 += diff + 1
        else:
            py1 += diff - max(py1,py2,py3) + ySize
        
    if py1 < max_y:
        max_y = py1
        max_flap[0], max_flap[1] = r1, r2
    
    ppx,ppy = px2,py2

    if frameCount >= 300:
        org += 1

        if gen == 1 or org >= 8:
            r1,r2 = create_flap(b_flap, False)
        else:
            r1,r2 = create_flap(b_flap, True)
        px1, py1 = ox, oy
        print(gen,org,"max:",ySize-max_y, max_flap)
        frameCount = 0

        if org >= 9:
            gen += 1
            org = 0
            b_flap = max_flap
    
    #Draw
    pygame.draw.line(screen, [0,0,0], (px1,int(py1)), (px3,py3),1)
    pygame.draw.line(screen, [0,0,0], (px3,py3), (px2,py2),1)
    pygame.draw.circle(screen, [0,0,255], (px3,py3), 4)
    pygame.draw.circle(screen, [255,0,0], (px1,int(py1)), 4)
    pygame.draw.circle(screen, [255,0,0], (px2,py2), 4)

    pygame.draw.line(screen, [0,0,0], (2*ox-px1,int(py1)), (2*ox-px3,py3),1)
    pygame.draw.line(screen, [0,0,0], (2*ox-px3,py3), (2*ox-px2,py2),1)
    pygame.draw.circle(screen, [0,0,255], (2*ox-px3,py3), 4)
    pygame.draw.circle(screen, [255,0,0], (2*ox-px1,int(py1)), 4)
    pygame.draw.circle(screen, [255,0,0], (2*ox-px2,py2), 4)
    
    pygame.draw.circle(screen, [0,255,0], (ox,int(max_y)), 4)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
