import pygame
import time
import os
from math import sqrt, sin, cos, atan2, exp, degrees, pi

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 600, 600
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pendulum")

#----------------------Main Loop----------------------#
#Distance - pixels
#Time - seconds

fps = 60
g = 6
airResistance = 0.5

points = []
dynamicPoints = []
fixedPoints = []
links = []

def dist(p1, p2):
    return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def apply(force, bearing, point):
    if point not in dynamicPoints: return
    point.xForce += force*sin(bearing)
    point.yForce += force*cos(bearing)

class FixedPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        fixedPoints.append(self)
    color = [255, 0, 0]
    mass = 10

class DynamicPoint:
    def __init__(self, x, y, color=[0,0,255]):
        self.x = x
        self.y = y
        self.color = color
        dynamicPoints.append(self)
    xVel = 0
    yVel = 0
    xAcc = 0
    yAcc = 0
    xForce = 0
    yForce = 0
    mass = 10

class Link:
    def __init__(self, p1, p2, isString=False):
        self.p1 = p1
        self.p2 = p2
        self.length = dist(p1, p2)
        self.isString = isString
        links.append(self)
    color = [0,0,0]
    tension = 0 #inwards
    stiffness = 700

center = FixedPoint(300, 300)

for i in range(0,5,4):
    p1 = DynamicPoint(250, 300, [0, i*25, 255 - i*25])
    p2 = DynamicPoint(245 + i, 250, [0, i*25, 255 - i*25])
    link1 = Link(center, p1)
    lin2 = Link(p1, p2)

##p1 = DynamicPoint(250, 300)
##p2 = DynamicPoint(255, 250)
##link1 = Link(center, p1)
##link2 = Link(p1, p2)
##
##p3 = DynamicPoint(250, 300, [0,255,0])
##p4 = DynamicPoint(245, 250, [0,255,0])
##link3 = Link(center, p3)
##link4 = Link(p3, p4)
##Link(p4,p1)
##
##center = DynamicPoint(100, 100)
##p1 = DynamicPoint(50, 50)
##p2 = DynamicPoint(150, 0)
##p1.mass = 100
##link1 = Link(center, p1, True)
##link2 = Link(p1, p2)
##link3 = Link(center, p2, True)


mouseHold = False
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    mx, my = pygame.mouse.get_pos()
    frameCount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

            mp = DynamicPoint(mx,my)
            Link(center, mp)

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([255,255,255])

    if frameCount % 1000 == 0: g = -g
    
    for point in dynamicPoints:
        point.xForce = 0
        point.yForce = point.mass*g

    for link in links:
        distDiff = dist(link.p1, link.p2) - link.length
        link.tension = max(distDiff*link.stiffness, distDiff*link.stiffness*(not link.isString))
        bearing1 = atan2(link.p2.x - link.p1.x, link.p2.y - link.p1.y)
        bearing2 = atan2(link.p1.x - link.p2.x, link.p1.y - link.p2.y)

        p1VelWeight = 1
        p2VelWeight = 1
##        if (link.p1 in dynamicPoints) and (link.p1.xVel != 0 or link.p1.yVel != 0) and distDiff != 0:
##            p1VelWeight = 1 + 0.3*(link.p1.yVel*cos(bearing2) + link.p1.xVel*sin(bearing2))/sqrt(link.p1.xVel**2 + link.p1.yVel**2)*distDiff/abs(distDiff)    
        if (link.p2 in dynamicPoints) and (link.p2.xVel != 0 or link.p2.yVel != 0) and distDiff != 0:        
            p2VelWeight = 1 + 0.3*(link.p2.yVel*cos(bearing1) + link.p2.xVel*sin(bearing1))/sqrt(link.p2.xVel**2 + link.p2.yVel**2)*distDiff/abs(distDiff)
        
        apply(min(link.tension*p1VelWeight, 2000), bearing1, link.p1)
        apply(min(link.tension*p2VelWeight, 2000), bearing2, link.p2)

        if distDiff > link.length: links.remove(link)

    for point in dynamicPoints:
        if point.y >= ySize - 5:
            point.yVel = -abs(0.8*point.yVel)
        if point.y <= 5:
            point.yVel = abs(0.8*point.yVel)
        if point.x >= xSize - 5:
            point.xVel = -abs(0.8*point.xVel)
        if point.x <= 5:
            point.xVel = abs(0.8*point.xVel)
        
    for point in dynamicPoints:
        point.xAcc = point.xForce/point.mass
        point.yAcc = point.yForce/point.mass
        point.xVel += point.xAcc
        point.yVel += point.yAcc
        point.x += point.xVel/fps
        point.y += point.yVel/fps
        
        point.x = min(ySize - 5, point.x)
        point.x = max(5, point.x)
        point.y = min(ySize - 5, point.y)
        point.y = max(5, point.y)

    for link in links:
        distDiff = dist(link.p1, link.p2) - link.length
        pygame.draw.line(screen, link.color, (int(link.p1.x), int(link.p1.y)), (int(link.p2.x), int(link.p2.y)), 1 + 2*(link.isString))

    for point in dynamicPoints + fixedPoints:
        pygame.draw.circle(screen, point.color, (int(point.x), int(point.y)), int(5*pow(point.mass/10,1/3)))

    pygame.draw.line(screen, [0,0,0], (550, 300), (550, 300 + g*20), 2)
    pygame.draw.line(screen, [0,0,0], (520, 300 + g*15), (550, 300 + g*20), 2)
    pygame.draw.line(screen, [0,0,0], (580, 300 + g*15), (550, 300 + g*20), 2)

    pygame.display.flip()
    clock.tick(fps/2)

pygame.quit()
