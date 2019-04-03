import pygame
import time
import os
from math import sqrt, cos, tan, radians
from functions import read

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 600, 600
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pygame Template")

def make_planet(ox,oy,r,texture):
    for y in range(oy - r, oy + r):
        ncol = int((y - oy + r)/(r/len(texture))/2)
        
        r2 = sqrt(r**2 - (y - oy)**2)
        c = 2*3.141*r2
        n = len(texture[ncol])
        for i in range(n):
            pygame.draw.line(screen, texture[ncol][i], (ox - c/2 + c*i/n,y), (ox - c/2 + c*(i+1)/n,y))

        n/=2
        for i in range(int(n)):
            icol = i
            while icol >= 2*n:
                icol = int(i - 2*n)
            if r2 == 0: r2 = 0.000001
            x = r2*cos(i*c/(2*n)/r2) - r2*cos(i*c/(2*n)/r2 + c/(2*n)/r2)
            x1 = r2 - r2*cos(i*c/(2*n)/r2)
            #pygame.draw.line(screen, texture[ncol][icol], (ox - r2 + x1, y), (ox - r2 + x1 + x, y))

def terminator(ox, oy, rad, angle):
    #pygame.draw.circle(screen,[col[0]/10,col[1]/10,col[2]/10],(ox,oy),rad)
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
                xe = ox + sqrt(rad*rad - pow(y - oy,2)) + 2
                horizontal_line = pygame.Surface((abs(xe - xs), 1), pygame.SRCALPHA)
                horizontal_line.fill((0, 0, 0, 240))
                screen.blit(horizontal_line, (xs,y))
                
                #pygame.draw.line(screen,col,(xs,y),(xe,y))
            else:
                xs = ox - sqrt(rad*rad - pow(y - oy,2))
                xe = x
                horizontal_line = pygame.Surface((abs(xe - xs), 1), pygame.SRCALPHA)
                horizontal_line.fill((0, 0, 0, 240))
                screen.blit(horizontal_line, (xs,y))
                
                #pygame.draw.line(screen,col,(xs,y),(xe,y))
        except: pass

#----------------------Main Loop----------------------#
q = [50,50,50]
w = [110,110,110]
q = [75,116,41]
w = [37,78,124]

text = read("\Textures\Text_Earth.txt").split("\n")

texture = {}

for i in range(len(text)):
    texture[i] = []
    for j in text[i]:
        if j == "q": texture[i].append(q)
        elif j == "w": texture[i].append(w)

r = 50
ox, oy = 300, 300

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
            
    screen.fill([0,0,0])

    if frameCount % 5 == 0:
        for i in range(len(texture)):
            texture[i].append(texture[i][0])
            texture[i].pop(0)
            

    make_planet(ox,oy,r,texture)

    #terminator(ox, oy, r, 45)#frameCount)

    
    if frameCount % 20 == 0: print(clock.get_fps())

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
