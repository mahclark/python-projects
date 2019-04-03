import pygame
import time
import math
from math import sqrt, atan2, degrees, radians, pi, sin, cos
import random
from random import randint as ri

pygame.init()

xSize, ySize = 600, 400
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pygame Template")

def get_end(length,angle,px0,py0):
    py = length*cos(radians(angle)) + py0
    px = length*sin(radians(angle)) + px0
    
    return int(px),int(py)

def get_joint(length,px1,py1,px2,py2,rev):
    dy, dx = py2 - py1, px2 - px1

    if dx == 0:
        dx = 0.00001
    if dy == 0:
        dy = 0.00001
        
    g_par = dy/dx
    g_per = -dx/dy
    
    pxm, pym = (int((px1 + px2)/2),int((py1 + py2)/2))

    mid_d = sqrt(pow(dy,2) + pow(dx,2))/2
    
    if length >= mid_d:
        pd = sqrt(pow(length,2) - pow(mid_d,2))

        px = sqrt(pow(pd,2)/(pow(g_per,2)+1))
        py = sqrt(pow(pd,2)*pow(g_per,2)/(pow(g_per,2)+1))

        if rev:
            py = -py
            px = -px
        
        if px2 > px1:
            py3 = int(pym + py)
        else:
            py3 = int(pym - py)
        if py2 < py1:
            px3 = int(pxm + px)
        else:
            px3 = int(pxm - px)
            
        return px3,py3,False
    else:
        return pxm,pym,True

#----------------------Main Loop----------------------#

length = 100

px1, py1 = 300,200
px2, py2 = 500,200
px3, py3 = 0,0
pxm, pym = 0,0 #midpoint

g_par = 0 #parallel gradient
g_per = 0 #perpendicular gradient

dx, dy = 0,0 #difference in x,y
pd = 0 #difference between midpoint & point3
px, py = 0,0 #x,y difference between midpoint & point3
mid_d = 0 #distance to midpoint

r1 = 5#ri(1,5)
r2 = 10#ri(1,5)
r3 = 90#ri(1,90)
r4 = 45#ri(1,90)
r5 = ri(r3,180-r3)
r6 = ri(r4,180-r4)

px3,py3 = get_end(length,r3*sin(r1*0)+r5,px1,py1)
px2,py2 = get_end(length,r4*sin(r2*0)+r6,px3,py3)
ppx,ppy = px2,py2

too_far = False
rev = True

clock = pygame.time.Clock()
frameCount = 0
mouseHold = False
done = False
t = 1.333
while not done:
    frameCount += 0.01
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([255,255,255])

    t -= 0.05

    t1 = r3*sin(r1*frameCount)+r5
    t2 = r4*sin(r2*frameCount+3.14/2)+r6
    
    px3,py3 = get_end(length,t1,px1,py1)
    px2,py2 = get_end(length,180-t2+t1,px3,py3)

    if frameCount > 2:
        diff = (py2 - ppy)*(px2 - px1)/1000
        py1 -= diff
        print(diff)
        
    ppx,ppy = px2,py2
    
    #print(px1,py1)
    
##    if mouseHold == True:
##        px2, py2 = mx, my
##    else:
##        #px2 = 230 - int(130*pow(1-t,2)) + 130
##        #py2 = 380 + int(100*pow(t,2)*math.log(t)/math.log(2.718281828))
##        if t >= 0.575:
##            px2 = 160 + int(150*t)
##            py2 = 380
##        elif t >= 0:
##            px2 = 170 + int(150*1.7*pow(t,2))
##            py2 = 380 - int(120*(pow(t,3)-t + 0.38488))
##        elif t >= -1.1547:
##            px2 = 170 + int(150*pow(t,2))
##            py2 = 380 - int(120*(pow(t,3)-t + 0.38488))
##        else:
##            t = 1.333
##        #print(t)
##
##    px3,py3,too_far = get_joint(length,px1,py1,px2,py2,rev)
    
    #Draw
    #if not too_far:
    pygame.draw.line(screen, [0,0,0], (px1,int(py1)), (px3,py3),1)
    pygame.draw.line(screen, [0,0,0], (px3,py3), (px2,py2),1)
    pygame.draw.circle(screen, [0,0,255], (px3,py3), 4)
    pygame.draw.circle(screen, [255,0,0], (px1,int(py1)), 4)
    pygame.draw.circle(screen, [255,0,0], (px2,py2), 4)
    
           

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
