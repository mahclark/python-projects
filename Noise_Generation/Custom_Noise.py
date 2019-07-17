import pygame
import os
import time
import math
import random
from random import randint
import sys
from ctypes import windll

dir_path = os.path.dirname(os.path.realpath(__file__))

def get_count(xc, yc, size):
    counta = len(dotsx)
    countf = 0
    posl = -1
    posu = -1
    n = 0
    while posl == -1:
        try:
            posl = dotsx.index(xc - size + n)
        except:
            n += 1
        
    n = 0
    while posu == -1:
        try:
            posu = dotsx.index(xc + size - n)
        except:
            n += 1
    
    for i in range(posl, posu):
        dx = abs(dotsx[i] - xc)
        dy = abs(dotsy[i][0] - yc)

        if dx < size:
            if dy < size:
                if dx + dy <= size:
                    countf += dotsy[i][1]
                elif math.pow(dx,2) + math.pow(dy,2) <= math.pow(size,2):
                    countf += dotsy[i][1]
    return countf
    

pygame.init()

#Settings
size = 60   #controls biome size (increases agianst amplitude)
pixel = 2   #controls resolution
k = 1.0     #relative altitude to normal (0.7 < x < 1.5)
grass = 30  #color level
rock = 43   # ''    ''
ice = 44    # ''    ''
snow = 50   # ''    ''

infoObject = pygame.display.Info()
scrW, scrH = infoObject.current_w, infoObject.current_h
xSize, ySize = 400, 400
screen = pygame.display.set_mode((int(xSize*2), ySize))
pygame.display.set_caption("Noise Creation")

dotsx = []
dotsy = []

total = 0
high = 0
low = 100
prevc = 0

for x in range(int(k*10*(xSize+2*size)*(ySize+2*size)/math.pow(size,2))):
    dotsx.append(randint(0,xSize+2*size)-1*size)
    dotsy.append([randint(0,ySize+2*size)-1*size, randint(0,200)/100])

dotsx.sort()

screen.fill([29,109,210])

prevc = get_count(0,0,size)
for x in range(int(xSize/pixel)):
    x *= pixel
    for y in range(int(ySize/pixel)):
        y *= pixel
        count = get_count(x, y, size)
        total += count

        if count > high:
            high = count
            hix = x
            hiy = y
        if count < low:
            low = count
            mix = x
            miy = y

        if count > grass:
            pygame.draw.rect(screen, [60,204,62], (x,y,pixel,pixel))
        if count > rock:
            pygame.draw.rect(screen, [91,46,39], (x,y,pixel,pixel))
        if count > ice:
            pygame.draw.rect(screen, [112,73,68], (x,y,pixel,pixel))
        if count > snow:
            pygame.draw.rect(screen, [255,255,255], (x,y,pixel,pixel))
        prevc = count
            
        pygame.display.flip()
pygame.draw.rect(screen, [255,0,0], (hix,hiy,pixel,pixel))
pygame.draw.rect(screen, [0,0,255], (mix,miy,pixel,pixel))

#Max / Min
##pygame.draw.line(screen, [0,0,255], (0, int(miy+pixel/2)), (xSize, int(miy+pixel/2)))
##pygame.draw.line(screen, [0,0,255], (int(mix+pixel/2), 0), (int(mix+pixel/2), ySize))
##pygame.draw.line(screen, [255,0,0], (0, int(hiy+pixel/2)), (xSize, int(hiy+pixel/2)))
##pygame.draw.line(screen, [255,0,0], (int(hix+pixel/2), 0), (int(hix+pixel/2), ySize))
##
###Terrain level
##pygame.draw.line(screen, [0,170,255], (xSize, ySize-ySize*(grass-low)/(high-low)), (2*xSize, ySize-ySize*(grass-low)/(high-low)))
##pygame.draw.line(screen, [91,46,39], (xSize, ySize-ySize*(rock-low)/(high-low)), (2*xSize, ySize-ySize*(rock-low)/(high-low)))
##pygame.draw.line(screen, [255,255,255], (xSize, ySize-ySize*(snow-low)/(high-low)), (2*xSize, ySize-ySize*(snow-low)/(high-low)))
##
##prev = get_count(0, miy, size)
##for x in range(1,int(xSize/pixel)):
##    x *= pixel
##    count = get_count(x, miy, size)
##    pygame.draw.line(screen, [0,0,0], (x-pixel+xSize,ySize-ySize*(prev-low)/(high-low)), (x+xSize,ySize-ySize*(count-low)/(high-low)))
##    prev = count
##    pygame.display.flip()
##
##prev = get_count(0, hiy, size)
##for x in range(1,int(xSize/pixel)):
##    x *= pixel
##    count = get_count(x, hiy, size)
##    pygame.draw.line(screen, [255,255,255], (x-pixel+xSize,ySize-ySize*(prev-low)/(high-low)), (x+xSize,ySize-ySize*(count-low)/(high-low)))
##    prev = count
##    pygame.display.flip()

for x in range(int(xSize/pixel)):
    x *= pixel
    for y in range(int(ySize/pixel)):
        y *= pixel
        count = get_count(x, y, size)
        total += count 
            
        pygame.draw.rect(screen, [255*(count-low)/(high-low),255*(count-low)/(high-low),255*(count-low)/(high-low)], (x+xSize,y,pixel,pixel))
            
        pygame.display.flip()
        
for i in range(len(dotsx)):
    pygame.draw.circle(screen, [255,0,0], (dotsx[i]+xSize, dotsy[i][0]), 2)
#pygame.display.flip()
pygame.draw.rect(screen, [255,0,0], (hix+xSize,hiy,pixel,pixel))
pygame.draw.rect(screen, [0,0,255], (mix+xSize,miy,pixel,pixel))

print("done")
print(total/((xSize/pixel)*(ySize/pixel)))
