import pygame
import time
import math
import random
from random import randint

pygame.init()

white = [255,255,255]
black = [0,0,0]

length = 50
subLen = 10
subArray = []

xSize, ySize = 500, 500
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Sonwflake Generator")

screen.fill(black)

branchNum = randint(3,8)
print(branchNum)

for i in range(branchNum):
    y = length*math.cos(math.radians(i*360/branchNum))
    x = length*math.sin(math.radians(i*360/branchNum))
    pygame.draw.line(screen, white, (250, 250), (250 + x, 250 + y), 4)

subNum = randint(0,10)
print(subNum)

for i in range(subNum):
        subArray.append([(i+0.5)*length/subNum, randint(-70,70)]) # [height, angle]

for n in range(branchNum):
    for i in range(subNum):
        ys = subArray[i][0]*math.cos(math.radians(n*360/branchNum))
        xs = subArray[i][0]*math.sin(math.radians(n*360/branchNum))
        
        ye = subLen*math.cos(math.radians(90 - n*360/branchNum))
        xe = subLen*math.sin(math.radians(90 - n*360/branchNum))
        
        pygame.draw.line(screen, white, (250 + xs, 250 + ys), (250 + xs + xe, 250 + ys - ye), 2)
        pygame.draw.line(screen, white, (250 + xs, 250 + ys), (250 + xs - xe, 250 + ys + ye), 2)

#for i in range(branchNum):
    

pygame.display.flip()


