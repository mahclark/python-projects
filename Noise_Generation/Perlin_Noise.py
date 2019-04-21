import pygame
import time
import os
from math import sqrt
import random
from random import randint

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 1000, 1000
screen = pygame.display.set_mode((xSize*2, ySize))
pygame.display.set_caption("Pygame Template")

def fade(x): return 6*x**5 - 15*x**4 + 10*x**3

def makeNoise(cellSize):
    vectorChoice = [
        ( 1, 1),
        ( 1,-1),
        (-1,-1),
        (-1, 1)
        ]
    vectors = []

    for yCorner in range(int(ySize/cellSize)):
        vectors.append([])
        for xCorner in range(int(xSize/cellSize)):
            randX = random.random()
            randY = random.random()
            mod = sqrt(randX**2 + randY**2)
            vectors[yCorner].append(vectorChoice[randint(0, len(vectorChoice) - 1)])
                                    #(randX/mod, randY/mod))
        vectors[yCorner].append(vectors[yCorner][0])
    vectors.append(vectors[0])

    values = []
    for y in range(ySize): values.append([])

    for yCell in range(int(ySize/cellSize)):
        for xCell in range(int(xSize/cellSize)):

            randVec0 = vectors[yCell][xCell]
            randVec1 = vectors[yCell][xCell + 1]
            randVec2 = vectors[yCell + 1][xCell + 1]
            randVec3 = vectors[yCell + 1][xCell]

            for yPixel in range(cellSize):
                for xPixel in range(cellSize):

                    distVec0 = (xPixel/cellSize, yPixel/cellSize)
                    distVec1 = (xPixel/cellSize - 1, yPixel/cellSize)
                    distVec2 = (xPixel/cellSize - 1, yPixel/cellSize - 1)
                    distVec3 = (xPixel/cellSize, yPixel/cellSize - 1)

                    dot0 = randVec0[0]*distVec0[0] + randVec0[1]*distVec0[1]
                    dot1 = randVec1[0]*distVec1[0] + randVec1[1]*distVec1[1]
                    dot2 = randVec2[0]*distVec2[0] + randVec2[1]*distVec2[1]
                    dot3 = randVec3[0]*distVec3[0] + randVec3[1]*distVec3[1]

                    topInterpolated = dot0 + fade(xPixel/cellSize)*(dot1 - dot0)
                    botInterpolated = dot3 + fade(xPixel/cellSize)*(dot2 - dot3)

                    finalValue = topInterpolated + fade(yPixel/cellSize)*(botInterpolated - topInterpolated)
                    values[yCell*cellSize + yPixel].append(finalValue)

    return values

v0 = makeNoise(200)
v1 = makeNoise(50)
v2 = makeNoise(25)

weights = (1,0.3,0.1)

for y in range(ySize):
    for x in range(xSize):
        col = (weights[0]*v0[y][x] + weights[1]*v1[y][x] + weights[2]*v2[y][x] + sum(weights))*127.5/sum(weights)
        screen.set_at((x, y), [col, col, col])
        
pygame.display.flip()

for y in range(ySize):
    for x in range(xSize):
        value = (weights[0]*v0[y][x] + weights[1]*v1[y][x] + weights[2]*v2[y][x] + sum(weights))/2/sum(weights)
        if value < 0.5: color = [29*(0.5 + value),109*(0.5 + value),210*(0.5 + value)]
        elif value < 0.65: color = [60*(1 - value/2),204*(1 - value/2),62*(1 - value/2)]
        elif value < 0.75: color = [91*(1 - value/2),46*(1 - value/2),39*(1 - value/2)]
        else: color = [255,255,255]
        
        screen.set_at((xSize + x, y), color)
        
pygame.display.flip()

#----------------------Main Loop----------------------#
mouseHold = False
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


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
