import pygame
import time
import os
from random import randint
from math import sqrt, atan2, sin as sine, cos as cosine, radians, degrees

def sin(deg): return sine(radians(deg))
def cos(deg): return cosine(radians(deg))

def pythag(a,b):
    return sqrt(a*a + b*b)

def correct(a,d,r,x,y):
    a += 90
    d -= r
    rx = x - d*cos(a)
    ry = y - d*sin(a)
    return rx, ry

def apply_force(magnitude,angle,hf,vf):
    hf += magnitude*sin(angle)
    vf += -magnitude*cos(angle)
    return hf, vf
    

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 600, 600
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pendulum Physics")

#----------------------Main Loop----------------------#

m = 1 #mass
g = 10#1.6 #gravitational field strength
hv = 0 #initial horizontal velocity
vv = 0 #initial vertical velocity
ppm = 5 #pixels per metre
fps = 60
r = 100 #radius
px1, py1 = 300,300 #fulcrum (red)
x = -r*sqrt(3)/2 #x coordinate of starting position of mass relative to fulcrum (x<=|r|)
px2, py2 = x + px1, sqrt(pow(r,2) - x*x) + py1 #starting position of mass
res = 1/500 #air resistance (1>=res>=0)

mouseHold = True
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    screen.fill([255,255,255])

    #Gravity Flip
    if int(frameCount/600) % 2 == 0:
        g = 20
    else:
        g = -20

##    #Water
##    if py2 >= ySize/2 + r*9/10 + 10*sin(px2+100*frameCount):#ySize/2 + r*9/10:
##        res = 0.9
##        hv -= 2
##    else:
##        res = 1/500
##    for i in range(xSize):
##        pygame.draw.rect(screen,[55,155,255],(i,ySize/2 + r*9/10 + 10*sin(i+10*frameCount),1,ySize/2))
    

    th = degrees(atan2((py2 - py1),(px2 - px1))) - 90 #theta, in degrees
    
    d = pythag(py1 - py2,px1 - px2) #true radius
    px2, py2 = correct(th,d,r,px2,py2) #adjusting radius

    v = pythag(hv,vv) #overall velocity
    v -= v*res #adding air resistance
    f = m*v*v/r + m*g*cos(th) #tension in string
    
    hf = 0 #horizontal force
    vf = 0 #vertical force
    hf, vf = apply_force(f,th,hf,vf)
    hf, vf = apply_force(m*g,180,hf,vf)
    hf, vf = apply_force(res*v*v,degrees(atan2(vv,hv)) - 90,hf,vf)

    ha = hf/m #horizontal acceleration
    va = vf/m

    hv += ha*ppm/fps #horizontal velocity (with speed corrections)
    vv += va*ppm/fps

##    if hv >= 0:
##        print(frameCount)

    px2 += hv*ppm/fps
    py2 += vv*ppm/fps
    
    #Draw
    string = pygame.draw.line(screen, [0,0,0], (px1,py1), (px2,py2),1)
    fulcrum = pygame.draw.circle(screen, [255,0,0], (px1,py1), 4)
    mass = pygame.draw.circle(screen, [0,0,255], (int(px2),int(py2)), 4)
    pygame.draw.circle(screen, [0,0,255], (int(px2),100), 4)    
##    pygame.draw.line(screen, [0,0,0], (px2 + hf,py2), (px2,py2),1)
##    pygame.draw.line(screen, [0,0,0], (px2,py2 + vf), (px2,py2),1)
    #Scale
    mark0 = pygame.draw.line(screen, [0,0,0], (5,5), (25,5),1)
    mark1 = pygame.draw.line(screen, [0,0,0], (5,5+ppm), (25,5+ppm),1)
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
