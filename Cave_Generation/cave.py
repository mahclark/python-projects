import pygame
import os
import time
from math import sqrt
from random import randint

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)

pygame.init()

#Screen
xSize, ySize = 1200, 800
screen = pygame.display.set_mode((xSize, ySize + 20))
base = pygame.Surface((xSize, ySize))
pygame.display.set_caption("Cave")

pixelSize = 10

caveArray = []

caveX = int(xSize/pixelSize)
caveY = int(ySize/pixelSize)

for y in range(caveY):
    row = []
    for x in range(caveX):
        value = round(randint(0,100) > 48)
        if x == 0 or y == 0 or x == caveX - 1 or y == caveY - 1: value = 0
        row.append(value)
    caveArray.append(row)

mx, my = pygame.mouse.get_pos()
mouseHold = False

def get(x, y):
    if x < 0 or x >= len(caveArray[0]) or y < 0 or y >= len(caveArray): return 0
    return caveArray[y][x]

def getNeighbours(x, y):
    count = get(x - 1, y - 1) + get(x    , y - 1) + get(x + 1, y - 1) + get(x - 1, y    ) + get(x + 1, y    ) + get(x - 1, y + 1) + get(x    , y + 1) + get(x + 1, y + 1)
    return count

def smooth():

    for y in range(len(caveArray)):
        for x in range(len(caveArray[0])):
            value = caveArray[y][x]
            pygame.draw.rect(base, [230*value, 230*value, 230*value], (x*pixelSize, y*pixelSize, pixelSize, pixelSize))

            if getNeighbours(x, y) > 4:
                caveArray[y][x] = 1
            elif getNeighbours(x, y) < 4:
                caveArray[y][x] = 0

for _ in range(10):
    smooth()

man = [0,0]
lights = []
lightCount = 10

bear = [0,0]

torchRadius = 10

def place():
    being = [0,0]
    while get(being[0], being[1]) == 0:
        being = [randint(1,caveX - 2), randint(1,caveY - 2)]
    return being

man = place()
bear = place()

#----------------------Main Loop----------------------#

lightOn = True

protoLight = None

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False

        if event.type == pygame.KEYUP:
            if keys[pygame.K_l]:
                lightOn = not lightOn

            if keys[pygame.K_SPACE]:
                if man not in lights and lightCount > 0:
                    protoLight = man.copy()
                    lights.append(protoLight)
                    lightCount -= 1

    if frameCount % (1 + 3*lightOn) == 0:
        prevMan = man.copy()
        if keys[pygame.K_w]:
            man[1] -= 1
        if keys[pygame.K_a]:
            man[0] -= 1
        if keys[pygame.K_s]:
            man[1] += 1
        if keys[pygame.K_d]:
            man[0] += 1

        if get(man[0], man[1]) == 0:

            if keys[pygame.K_RETURN] and randint(0,10) == 0:
                caveArray[man[1]][man[0]] = 1
            man = prevMan

        if man != prevMan:
            protoLight = None

            
    screen.fill([0,0,0])

    # screen.blit(base, (0,0))

    intensities = {}

    for (n, light) in enumerate([man] + lights):

        if n == 0:
            lightRadius = 9 if lightOn else 30
        else:
            lightRadius = torchRadius

        flicker = 1
        if randint(0,10) == 0: flicker = randint(70,100)/100

        for y in range(light[1] - lightRadius, light[1] + lightRadius):
            for x in range(light[0] - lightRadius, light[0] + lightRadius):
                if [x,y] != light:
                    dist = sqrt((y - light[1])**2 + (x - light[0])**2)

                    fade = 2.5
                    intensity = 1/(1 + pow(2, fade*(abs(dist) + 5/fade - lightRadius)))
                    intensity *= flicker

                    blocked = False
                    xStep = (x - light[0])/int(dist)
                    yStep = (y - light[1])/int(dist)
                    for i in range(int(dist)):
                        posx, posy = int(light[0] + xStep*i), int(light[1] + yStep*i)
                        if get(posx, posy) == 0 or [posx, posy] in (bear):
                            blocked = True
                            break

                    existing = intensities.get((x, y), 0)

                    if get(x, y) == 0:
                        intensity *= .2
                        if existing + intensity > 0.3:
                            intensity = 0.3 - existing

                    elif blocked:
                        intensity *= .5

                    newIntensity = min(1, existing + intensity)

                    if newIntensity > 0:
                        intensities[(x, y)] = newIntensity
                    # pygame.draw.rect(screen, [230*intensity, 200*intensity, 170*intensity], (x*pixelSize, y*pixelSize, pixelSize, pixelSize))

    for pos in intensities:
        intensity = intensities.get(pos)
        pygame.draw.rect(screen, [230*intensity, 200*intensity, 170*intensity], (pos[0]*pixelSize, pos[1]*pixelSize, pixelSize, pixelSize))

    for (n,pos) in enumerate(lights):
        if pos == man and pos != protoLight:
            del lights[n]
            lightCount += 1
            break

    for pos in lights:
        pygame.draw.rect(screen, [255, 250, 150], (pos[0]*pixelSize, pos[1]*pixelSize, pixelSize, pixelSize))

    pygame.draw.rect(screen, [20, 50, 100], (man[0]*pixelSize + 2, man[1]*pixelSize + 2, pixelSize - 4, pixelSize - 4))

    pygame.draw.rect(screen, [89, 69, 46], ((bear[0] - 1)*pixelSize + 5, bear[1]*pixelSize, pixelSize - 5, pixelSize))
    pygame.draw.rect(screen, [89, 69, 46], (bear[0]*pixelSize, bear[1]*pixelSize, pixelSize, pixelSize))
    pygame.draw.rect(screen, [89, 69, 46], ((bear[0] + 1)*pixelSize + 2, bear[1]*pixelSize + 2, pixelSize - 4, pixelSize - 4))

    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Lights: {0}".format(lightCount), 1, (255,255,255))
    screen.blit(label, (10, ySize))

    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("{0}".format(int(clock.get_fps())), 1, (255,255,255))
    screen.blit(label, (xSize - 20, ySize))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
