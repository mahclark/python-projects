import pygame
import time
from math import radians, sin, cos, tan, atan, sqrt, pi
import numpy as np

pygame.init()

xSize, ySize = 1600, 800
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("3D Graphics")

xFov = pi/4
yFov = 2*atan(tan(xFov/2)*ySize/xSize)

ry = 0 #rotation about y axis
rx = pi/4#rotation about x axis

class c: x, y, z = 0,50,0 #camera coordinates

class ScreenCoordinate():
    def __init__(self, x=0, y=0, dist = 0, behind=False):
    	self.x = x
    	self.y = y
    	self.behind = behind;
    	self.dist = dist
a = ScreenCoordinate(1,4)

def get_2d_vectorized(coordinates): #Algorithm to convert 3D coordinates into 2D screen coordinates
	world = coordinates - [c.x, c.y, c.z]

	rotateY = lambda coordinate: np.array([	coordinate[0]*cos(ry) - coordinate[2]*sin(ry),
											coordinate[1],
											coordinate[0]*sin(ry) + coordinate[2]*cos(ry)
											])
	rotateX = lambda coordinate: np.array([	coordinate[0],
											coordinate[1]*cos(rx) - coordinate[2]*sin(rx),
											coordinate[1]*sin(rx) + coordinate[2]*cos(rx)
											])

	# rotate = lambda coordinate: np.array([	coordinate[0]*cos(ry) - coordinate[2]*sin(ry),
	# 										coordinate[1]*cos(rx) - (coordinate[0]*sin(ry) + coordinate[2]*cos(ry))*sin(rx),
	# 										coordinate[1]*sin(rx) + (coordinate[0]*sin(ry) + coordinate[2]*cos(ry))*cos(rx)
	# 										])

	# cameraCoordinates = np.apply_along_axis(rotate, 1, world)
	cameraCoordinates = np.apply_along_axis(rotateX, 1, np.apply_along_axis(rotateY, 1, world))

	makeScreen = lambda coordinate : ScreenCoordinate(behind=True) if coordinate[2] >= 0 else ScreenCoordinate(
														xSize*(0.5 + coordinate[0]/(coordinate[2]*tan(xFov))),
														ySize*(0.5 + coordinate[1]/(coordinate[2]*tan(yFov))),
														sqrt(coordinate[0]**2 + coordinate[1]**2 + coordinate[2]**2)
														)

	screenCoordinates = np.apply_along_axis(makeScreen, 1, cameraCoordinates)

	return screenCoordinates

#----------------------Main Loop----------------------#

clock = pygame.time.Clock()
fc = 0
done = False
while not done:
    fc += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if keys[pygame.K_ESCAPE]:
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
    else:
        delta_x, delta_y = pygame.mouse.get_rel()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        rx += delta_y*pi/180/30
        ry += delta_x*pi/180/30
        if rx > pi/2: ry = pi/2
        if rx < -pi/2: ry = -pi/2
    if keys[pygame.K_w]:
        c.x += -sin(ry)
        c.z -= cos(ry)
    if keys[pygame.K_a]:
        c.x += cos(ry)
        c.z += -sin(ry)
    if keys[pygame.K_s]:
        c.x -= -sin(ry)
        c.z += cos(ry)
    if keys[pygame.K_d]:
        c.x -= cos(ry)
        c.z -= -sin(ry)
    if keys[pygame.K_SPACE]:
        c.y += 1
    if keys[pygame.K_LCTRL]:
        c.y -= 1
    if keys[pygame.K_LALT] and keys[pygame.K_q]:
    	done = True

    screen.fill([255,255,255])

    landscape = [] #generating flat landscape
    for x in range(-50,50,2):
        for z in range(-50,50,2):
            landscape.append((x, 4*cos(5*(x + z - fc)*pi/180), z))

    landscape = np.array(landscape)

    screenCoordinates = get_2d_vectorized(landscape)

    for i in range(len(screenCoordinates) - 1): #creating landscape

    	if not screenCoordinates[i].behind and not screenCoordinates[i+1].behind:
    		pygame.draw.line(screen, [0,0,0], (int(screenCoordinates[i].x), int(screenCoordinates[i].y)), (int(screenCoordinates[i+1].x), int(screenCoordinates[i+1].y)))
    		# pygame.draw.circle(screen, [0,0,0], (int(screenCoordinates[i].x), int(screenCoordinates[i].y)), round(4*100/screenCoordinates[i].dist))

    fps = int(10*clock.get_fps())/10
    fpsLabel = pygame.font.SysFont("monospace", 15).render(str(fps), 1, (0,0,0))
    screen.blit(fpsLabel, (0,0)) #displays fps

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
