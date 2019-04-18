import pygame
import time
import os
from math import sqrt, sin, cos, atan2, exp

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 600, 600
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pygame Template")

#----------------------Main Loop----------------------#
#Distance - pixels
#Time - seconds

fps = 60
g = 2
airResistance = 0.5

points = []
dynamicPoints = []
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
        points.append(self)
    color = [255, 0, 0]

class DynamicPoint:
    def __init__(self, x, y, color=[0,0,255]):
        self.x = x
        self.y = y
        self.color = color
        points.append(self)
        dynamicPoints.append(self)
    xVel = 0
    yVel = 0
    xAcc = 0
    yAcc = 0
    xForce = 0
    yForce = 0
    mass = 10

class Link:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.length = dist(p1, p2)
        links.append(self)
    color = [0,0,0]
    tension = 0 #inwards
    stiffness = 700

center = FixedPoint(300, 300)
p1 = DynamicPoint(250, 300)
p2 = DynamicPoint(200, 299)
link1 = Link(center, p1)
link2 = Link(p1, p2)

p3 = DynamicPoint(250, 300, [0,255,0])
p4 = DynamicPoint(200, 301, [0,255,0])
link3 = Link(center, p3)
link4 = Link(p3, p4)


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
            
    screen.fill([255,255,255])
    
    for point in dynamicPoints:
        point.xForce = 0#30*sin(frameCount/300) - point.xVel*airResistance
        point.yForce = point.mass*g# - point.yVel*airResistance

    for link in links:
        distDiff = dist(link.p1, link.p2) - link.length
        link.tension = distDiff*link.stiffness
        bearing1 = atan2(link.p2.x - link.p1.x, link.p2.y - link.p1.y)
        bearing2 = atan2(link.p1.x - link.p2.x, link.p1.y - link.p2.y)
        apply(link.tension, bearing1, link.p1)
        apply(link.tension, bearing2, link.p2)
    
    for point in dynamicPoints:
        point.xAcc = point.xForce/point.mass
        point.yAcc = point.yForce/point.mass
        point.xVel += point.xAcc
        point.yVel += point.yAcc
        point.x += point.xVel/fps
        point.y += point.yVel/fps

    for link in links:
        pygame.draw.line(screen, link.color, (int(link.p1.x), int(link.p1.y)), (int(link.p2.x), int(link.p2.y)), 1)

    for point in points:
        pygame.draw.circle(screen, point.color, (int(point.x), int(point.y)), 4)
        

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
