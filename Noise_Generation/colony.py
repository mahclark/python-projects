import pygame
import pygame.freetype
import time
import os
from math import sqrt, inf
import random
from random import randint
import perlin_noise
import a_star

dir_path = os.path.dirname(os.path.realpath(__file__))

xSize, ySize = 1200, 800

rendersShadows = False #High render times!

pygame.init()
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Colony")

class Bridge():
    def __init__(self, origin, aim):
        self.origin = origin
        self.aim = aim
        self.points = [origin]
        self.direction = (self.aim[0] - self.origin[0], self.aim[1] - self.origin[1])
        self.direction = (self.direction[0]/sqrt(self.direction[0]**2 + self.direction[1]**2), self.direction[1]/(sqrt(self.direction[0]**2 + self.direction[1]**2)))
        self.current = (origin[0] + self.direction[0], origin[1] + self.direction[1])
    complete = False

class Airplane():
	landed = True

	def __init__(self, position):
		self.position = position
		self.pixel = position
		self.hidden_color1 = screen.get_at(position)
		self.hidden_color2 = screen.get_at(position)
		self.tail = position
		self.height = 0

	def takeoff(self, destination):
		self.landed = False
		self.destination = destination
		self.curveSide = 2*randint(0,1) - 1
		self.adjust()

	def adjust(self):
		self.direction = (self.destination[0] - self.position[0], self.destination[1] - self.position[1])
		self.dist = sqrt(self.direction[0]**2 + self.direction[1]**2)
		if self.dist > 2: self.direction = (self.direction[0] + self.curveSide*self.direction[1]/1.5, self.direction[1] - self.curveSide*self.direction[0]/1.5)
		self.direction = (self.direction[0]/self.dist, self.direction[1]/self.dist)

airplane = Airplane((1,2))
airplane.takeoff((5,20))

def multiplyVec(vector, x):
    newVector = []
    for component in vector:
        newVector.append(component*x)
    return tuple(newVector)

def multiplyVecs(vector1, vector2):
    newVector = []
    for c1, c2 in zip(vector1, vector2):
        newVector.append(c1*c2)
    return tuple(newVector)

L = (-1/sqrt(3), -1/sqrt(3), 1/sqrt(3)) #Direction to light

def shader(meshColor, normal, shaded):
    Ia = (0.8,0.8,1) #Ambient light color
    Kd = 0.99 #Diffuse coefficient
    I = (1,1,0.5) #Directional light color

    ambient = multiplyVecs(multiplyVec(meshColor, 1/255), Ia) #max = max(Ia)
    diffuse = multiplyVec(multiplyVecs(multiplyVec(meshColor, Kd/255), I), (1 - shaded)*max(0, normal[0]*L[0] + normal[1]*L[1] + normal[2]*L[2])) #max = Kd*Max(I)

    return multiplyVec((ambient[0] + diffuse[0], ambient[1] + diffuse[1], ambient[2] + diffuse[2]), 255/(max(Ia) + Kd*max(I)))

def makePath(pos, destination=None):
    global path
    global pathRemaining

    if destination == None:
        minimum = (None, inf)
        for hub in hubs:
            distance = sqrt((hub[0] - mx)**2 + (hub[1] - my)**2)
            if distance < minimum[1]:
                minimum = (hub, distance)
        destination = minimum[0]

    (newPath, bridgePos) = a_star.findPath(pos, destination, (xSize, ySize), normals, heights, (0.5, 0.65), path)

    if newPath != None:
        path += newPath.copy()
        pathRemaining += newPath.copy()
        
    if bridgePos != None:
        bridge = Bridge(bridgePos, destination)
        bridges.append(bridge)

def offScreen(pos):
	if pos[0] < 0 or pos[0] >= xSize or pos[1] < 0 or pos[1] >= ySize:
		return True
	return False

(v0, n0) = perlin_noise.makeNoise((200,200), (xSize, ySize))
(v1, n1) = perlin_noise.makeNoise((50,50), (xSize, ySize))
(v2, n2) = perlin_noise.makeNoise((25,25), (xSize, ySize))
(v3, n3) = perlin_noise.makeNoise((10,10), (xSize, ySize))

print("rendering landscape...")

valueLevels = [v0,v1,v2,v3]
normalLevels = [n0,n1,n2,n3]

levelWeights = (1, 0.3, 0.2, 0.1)

waterLevel = 0.5
grassLevel = 0.65
rockLevel = 20.0

potentialHubs = []
heights = {}
normals = {}
shadow = {}

maxHeight = 0

for y in range(ySize):
    for x in range(xSize):

        value = (sum([levelWeights[i]*valueLevels[i][y][x] for i in [0,1,2]]) + sum(levelWeights))/2/sum(levelWeights)

        if value >= grassLevel:
            value = grassLevel + (value - grassLevel)*(value + 1)**10

        heights[(x,y)] = value
        if value > maxHeight: maxHeight = value
        
for y in range(ySize):
    for x in range(xSize):

        value = heights[(x,y)]

        weightedNormals = []
        for normalLevel, weight in zip(normalLevels, levelWeights):
            weightedNormals.append(multiplyVec(normalLevel[y][x], weight))

        normalSum = (sum([n[0] for n in weightedNormals]), sum([n[1] for n in weightedNormals]), sum([n[2] for n in weightedNormals]))

        modulus = sqrt(normalSum[0]**2 + normalSum[1]**2 + normalSum[2]**2)
        normal = multiplyVec(normalSum, 1/modulus)
        normals[(x,y)] = normal
        
        if value < waterLevel:
            meshColor = (84*(0.5 + value), 128*(0.5 + value), 197*(0.5 + value))#(29,109,210)
            normal = (0,0,1)

        elif value < grassLevel:
            i = randint(120,140)
            meshColor = (0.7*i, i, 0.6*i)#[60*(1.25 - value), 204*(1.25 - value), 62*(1.25 - value)]

            if value < 0.505:
                potentialHubs.append((x,y))

        elif value < rockLevel:
            i = randint(70,90)
            meshColor = (1.5*i, 1.3*i, 1.2*i)#[182*(1.25 - value), 92*(1.25 - value), 78*(1.25 - value)]

        else:
            meshColor = (235,235,235)#[255*(value), 255*(value), 255*(value)]

        shaded = False
        if rendersShadows:
            currentPos = (x,y,max(value, waterLevel))
            shadowInaccuracy = 3
            while True:
                currentPos = (currentPos[0] + shadowInaccuracy*L[0], currentPos[1] + shadowInaccuracy*L[1], currentPos[2] + shadowInaccuracy*L[2]/4)
                if round(currentPos[0]) < 0 or round(currentPos[1]) < 0 or round(currentPos[0]) >= xSize or round(currentPos[1]) >=ySize or currentPos[2] > maxHeight:
                    break
                if heights[(round(currentPos[0]), round(currentPos[1]))] > currentPos[2]:
                    shaded = True
                    break

        shadow[(x,y)] = shaded

        color = shader(meshColor, normal, shaded)
        
        screen.set_at((x, y), color)
    if 100*y/ySize % 10 == 0:
        print(str(int(100*y/ySize)) + "%")

cityNumber = 1
cities = []
hubs = []
bridges = [] #[(origin, current build pos, destination hub)]
airports = []
airplanes = []
for cityNum in range(cityNumber):
    city = []
    hub = potentialHubs[randint(0,len(potentialHubs) - 1)]
    hubs.append(hub)
    city.append(hub)
    cities.append(city)
    airports.append(hub)

path = []
pathRemaining = []

print("rendering complete")
print()

pygame.display.flip()
background = screen.copy()

#----------------------Main Loop----------------------#
mouseHold = False
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 1
    mx,my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False

            if heights[(mx,my)] >= waterLevel and heights[(mx,my)] < grassLevel:
	            makePath((mx,my))

	            cities.append([(mx,my)])
	            hubs.append((mx,my))
	            airports.append((mx,my))

	            airplane = Airplane((mx,my))
	            airplanes.append(airplane)

    for city in cities:
        cityPoint = city[randint(0, len(city) - 1)]
        direction = randint(0,3) #clockiwise from left = 0
        expansionPoint = (cityPoint[0] + (direction%2==0)*(direction - 1), cityPoint[1] + (direction%2==1)*(direction - 2))
        if a_star.checkValid(expansionPoint, (xSize, ySize), heights, (0.5, 0.65)) and randint(0, int(1000*abs(heights[cityPoint] - heights[expansionPoint]))) == 0:
            
            if expansionPoint not in city:
                city.append(expansionPoint)
                if path == None or expansionPoint not in path:
                    cityPalette = [
                    (180, 180, 190),
                    (185, 185, 185),
                    ]
                    screen.set_at(expansionPoint, shader(cityPalette[randint(0, len(cityPalette) - 1)], normals[expansionPoint], shadow[expansionPoint]))

    if pathRemaining != [] and frameCount%3 == 0 and sum([len(city) for city in cities]) > 200:
        screen.set_at(pathRemaining[0], shader([80,80,80], normals[pathRemaining[0]], shadow[pathRemaining[0]]))
        if len(pathRemaining) > 1: screen.set_at(pathRemaining[-1], shader([80,80,80], normals[pathRemaining[-1]], shadow[pathRemaining[-1]]))
        del pathRemaining[0]
        if len(pathRemaining) > 0: del pathRemaining[-1]

    for (n, bridge) in enumerate(bridges):
        if not bridge.complete and pathRemaining == []:
            newPos = (bridge.current[0] + bridge.direction[0], bridge.current[1] + bridge.direction[1])
            newPixel = (round(newPos[0]), round(newPos[1]))

            # sides = [
            #     (newPixel[0] - 1, newPixel[1] - 1),
            #     (newPixel[0]    , newPixel[1] - 1),
            #     (newPixel[0] + 1, newPixel[1] - 1),
            #     (newPixel[0] - 1, newPixel[1]    ),
            #     (newPixel[0] + 1, newPixel[1]    ),
            #     (newPixel[0] - 1, newPixel[1] + 1),
            #     (newPixel[0]    , newPixel[1] + 1),
            #     (newPixel[0] + 1, newPixel[1] + 1),
            #     ]

            screen.set_at(newPixel, shader([150,150,150], (0,0,1), shadow[newPixel]))

            # for side in sides:
            #     if side not in bridge.points and not offScreen(side):
            #         screen.set_at(side, shader([150,150,150], (0,0,1), shadow[side]))

            bridge.current = newPos
            bridge.points.append(newPixel)

            if heights[newPixel] >= waterLevel:
                bridge.complete = True
                print("aim path from " + str(newPixel) + " to " + str(bridge.aim))
                makePath(newPixel, bridge.aim)

    if randint(1,60) == 1 and airplanes != []:
    	plane = airplanes[randint(0, len(airplanes) - 1)]
    	if plane.landed:
    		destination = plane.position
    		while destination == plane.position:
    			destination = hubs[randint(0, len(hubs) - 1)]

    		plane.takeoff(destination)
    
    for plane in airplanes:
    	if not plane.landed and sum([len(city) for city in cities]) > 400:
    		plane.adjust()

    		newPos = (plane.position[0] + plane.direction[0], plane.position[1] + plane.direction[1])
    		newPixel = (round(newPos[0]), round(newPos[1]))

    		pixelNoMove = False
    		if plane.pixel == newPixel: pixelNoMove = True

    		if not offScreen(plane.tail) and not pixelNoMove:
    			screen.set_at(plane.tail, plane.hidden_color2)

    		plane.position = newPos

    		if not pixelNoMove:
    			plane.tail = plane.pixel
    			plane.pixel = newPixel

    		if not offScreen(plane.pixel) and not pixelNoMove:
    			plane.hidden_color2 = plane.hidden_color1
    			plane.hidden_color1 = screen.get_at(plane.pixel)
    			screen.set_at(plane.pixel, shader([255,255,255], (0,0,1), False))

    		# currentPos = (plane.pixel[0], plane.pixel[1], plane.height)
    		# shadowInaccuracy = 3
    		# while True:
    		# 	currentPos = (currentPos[0] - shadowInaccuracy*L[0], currentPos[1] - shadowInaccuracy*L[1], currentPos[2] - shadowInaccuracy*L[2]/4)
    		# 	if round(currentPos[0]) < 0 or round(currentPos[1]) < 0 or round(currentPos[0]) >= xSize or round(currentPos[1]) >=ySize or currentPos[2] > maxHeight:
    		# 		break
    		# 	if heights[(round(currentPos[0]), round(currentPos[1]))] > currentPos[2]:
    		# 		shadow[(round(currentPos[0]), round(currentPos[1]))] = True
    		# 		break

    		if plane.pixel == plane.destination:
    			plane.landed = True
    			if not offScreen(plane.pixel): screen.set_at(plane.pixel, plane.hidden_color1)
    			if not offScreen(plane.tail): screen.set_at(plane.tail, plane.hidden_color2)


    pygame.display.flip()

    clock.tick(60)
    currentFps = clock.get_fps()

pygame.quit()
