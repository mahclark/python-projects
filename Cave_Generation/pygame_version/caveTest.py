import pygame
import os
import time
from math import sqrt, atan2, sin, cos, degrees
from random import randint

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)

pygame.init()

#Screen
xSize, ySize = 1200, 800
screen = pygame.display.set_mode((xSize, ySize + 20))
base = pygame.Surface((xSize, ySize))
world = pygame.Surface((xSize, ySize))
ui = pygame.Surface((xSize, 20))
pygame.display.set_caption("Cave")

pixelSize = 10

caveArray = []

caveX = int(xSize/pixelSize)
caveY = int(ySize/pixelSize)

for y in range(caveY):
	row = []
	for x in range(caveX):
		rand = randint(0,120)
		value = (rand > 55) + (rand > 80)
		if x == 0 or y == 0 or x == caveX - 1 or y == caveY - 1: value = 0
		row.append(value)
	caveArray.append(row)

mx, my = pygame.mouse.get_pos()
mouseHold = False

def get(x, y):
	if x < 0 or x >= len(caveArray[0]) or y < 0 or y >= len(caveArray): return 0
	return caveArray[y][x]

def getNeighbours(x, y):
	count = get(x - 1, y - 1) == 1
	count += get(x	  , y - 1) == 1
	count += get(x + 1, y - 1) == 1
	count += get(x - 1, y	 ) == 1
	count += get(x + 1, y	 ) == 1
	count += get(x - 1, y + 1) == 1
	count += get(x    , y + 1) == 1
	count += get(x + 1, y + 1) == 1
	return count

def getWater(x, y):
	count = get(x - 1, y - 1) == 2
	count += get(x	  , y - 1) == 2
	count += get(x + 1, y - 1) == 2
	count += get(x - 1, y	 ) == 2
	count += get(x + 1, y	 ) == 2
	count += get(x - 1, y + 1) == 2
	count += get(x    , y + 1) == 2
	count += get(x + 1, y + 1) == 2
	return count

def smooth():

	for y in range(len(caveArray)):
		for x in range(len(caveArray[0])):
			value = caveArray[y][x]
			color = [230*value, 230*value, 230*value] if value < 2 else [20,120,250]
			pygame.draw.rect(base, color, (x*pixelSize, y*pixelSize, pixelSize, pixelSize))

			neighbours = getNeighbours(x,y) + getWater(x,y)

			if getWater(x,y) > 4:
				caveArray[y][x] = 2
			elif value != 2 or getWater(x,y) < 4:
				if neighbours > 4:# and (value != 2) or (value == 2 and getWater(x,y) < 2):
					caveArray[y][x] = 1
				elif neighbours < 4 or (value == 2 and getWater(x,y) < 2):
					caveArray[y][x] = 0

			if caveArray[y][x] != value:
				screen.blit(base,(0,0))
				pygame.display.flip()

for i in range(50):
	smooth()
	screen.fill([0,0,0])
	base.set_alpha(255*(30 - max(0, i - 20))/30)
	screen.blit(base, (0,0))
	pygame.display.flip()

man = [0,0]
lights = []
lightCount = 10

bear = [0,0]

torchRadius = 18

def place():
	being = [0,0]
	while get(being[0], being[1]) == 0:
		being = [randint(1,caveX - 2), randint(1,caveY - 2)]
	return being

man = place()
bear = place()

wetness = 0

footprints = []

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

	wetness = max(0, wetness - 0.004)

	newFootprints = []
	for (footprint, alpha, angle, pos) in footprints:

		footprint = pygame.Surface((pixelSize, pixelSize), pygame.SRCALPHA, 32)

		left = pygame.Surface((3, 2))
		right = pygame.Surface((3, 2))

		left.fill([50, 40, 30])
		right.fill([50, 40, 30])

		alpha -= 255*0.007
		left.set_alpha(alpha)
		right.set_alpha(alpha)

		footprint.blit(left, (pixelSize*0.75, pixelSize*0.3))
		footprint.blit(right, (pixelSize*0.25, pixelSize*0.7))

		footprint = pygame.transform.rotate(footprint, -degrees(angle))

		if alpha > 0:
			newFootprints.append((footprint, alpha, angle, pos))

	footprints = newFootprints

	if frameCount % max(1, int((5 + 2*(get(man[0], man[1]) == 2))*clock.get_fps()/60)) == 0:
		prevMan = man.copy()
		if keys[pygame.K_w]:
			man[1] -= 1
		if keys[pygame.K_a]:
			man[0] -= 1
		if keys[pygame.K_s]:
			man[1] += 1
		if keys[pygame.K_d]:
			man[0] += 1

		angle = atan2(man[1] - prevMan[1], man[0] - prevMan[0])

		if get(man[0], man[1]) == 2:
			wetness = 1

		if get(prevMan[0], prevMan[1]) == 1 and wetness > 0 and get(man[0], man[1]) != 2:
			footprint = pygame.Surface((pixelSize, pixelSize), pygame.SRCALPHA, 32)
			footprint.fill([0,0,0,0])

			lFoot = pygame.Surface((3, 2))
			rFoot = pygame.Surface((3, 2))

			lFoot.fill([50, 40, 30])
			rFoot.fill([50, 40, 30])

			lFoot.set_alpha(255*wetness)
			rFoot.set_alpha(255*wetness)

			footprint.blit(lFoot, (pixelSize*0.75, pixelSize*0.3))
			footprint.blit(rFoot, (pixelSize*0.25, pixelSize*0.7))

			footprint = pygame.transform.rotate(footprint, -degrees(angle))

			if prevMan != man:
				footprints.append((footprint, 255*wetness, angle, prevMan))

		if get(man[0], man[1]) == 0:
			if keys[pygame.K_RETURN] and randint(0,10) == 0:
				caveArray[man[1]][man[0]] = 1
			man = prevMan

		if man != prevMan:
			protoLight = None

	world.set_alpha(min(255, frameCount/0.1))
	world.fill([0,0,0])
	ui.fill([0,0,0])

	intensities = {}
	for (n, light) in enumerate([man] + lights):

		if n == 0:
			lightRadius = 15 if lightOn else 50
		else:
			lightRadius = torchRadius

		flicker = 1
		if randint(0,10) == 0: flicker = randint(70,100)/100

		blocks = {}
		for y in range(light[1] - lightRadius, light[1] + lightRadius):
			forStep = 1 if y == light[1] - lightRadius or y == light[1] + lightRadius - 1 else 2*lightRadius - 1
			for x in range(light[0] - lightRadius, light[0] + lightRadius, forStep):
				dist = sqrt((y - light[1])**2 + (x - light[0])**2)
				d = int(dist)

				blocked = False
				xStep = (x - light[0])/d
				yStep = (y - light[1])/d
				for i in range(d):
					posx, posy = int(light[0] + xStep*i), int(light[1] + yStep*i)
					if get(posx, posy) == 0 or [posx, posy] in (bear):
						blocked = True
					blocks[(posx, posy)] = blocked



		for y in range(light[1] - lightRadius, light[1] + lightRadius):
			for x in range(light[0] - lightRadius, light[0] + lightRadius):
				if [x,y] != light:
					dist = sqrt((y - light[1])**2 + (x - light[0])**2)

					fade = 0.8#2.5
					intensity = 1/(1 + pow(2, fade*(abs(dist) + 5/fade - lightRadius)))
					intensity *= flicker

					blocked = blocks.get((x,y), True)

					existing = intensities.get((x, y), 0)

					if get(x, y) == 0:
						intensity *= .2
						if existing + intensity > 0.3:
							intensity = 0.3 - existing

					elif blocked:
						intensity *= .5
						maxIntensity = 0.4
						intensity = max(0, min(maxIntensity - existing, intensity))

					newIntensity = min(1, existing + intensity)

					if newIntensity > 0:
						intensities[(x, y)] = newIntensity

	for pos in intensities:
		if pos[1] < caveY:
			intensity = intensities.get(pos)
			color = [230*intensity, 200*intensity, 170*intensity]
			if get(pos[0], pos[1]) == 2: color = [80*intensity, 96*intensity, 200*intensity]
			pygame.draw.rect(world, color, (pos[0]*pixelSize, pos[1]*pixelSize, pixelSize, pixelSize))

	for (n,pos) in enumerate(lights):
		if pos == man and pos != protoLight:
			del lights[n]
			lightCount += 1
			break

	for (footprint, alpha, angle, pos) in footprints:
		world.blit(footprint, (pos[0]*pixelSize, pos[1]*pixelSize))
		
	for pos in lights:
		pygame.draw.rect(world, [255, 250, 150], (pos[0]*pixelSize, pos[1]*pixelSize, pixelSize, pixelSize))

	pygame.draw.rect(world, [20, 50, 100], (man[0]*pixelSize + 2, man[1]*pixelSize + 2, pixelSize - 4, pixelSize - 4))

	pygame.draw.rect(world, [89, 69, 46], ((bear[0] - 1)*pixelSize + 5, bear[1]*pixelSize, pixelSize - 5, pixelSize))
	pygame.draw.rect(world, [89, 69, 46], (bear[0]*pixelSize, bear[1]*pixelSize, pixelSize, pixelSize))
	pygame.draw.rect(world, [89, 69, 46], ((bear[0] + 1)*pixelSize + 2, bear[1]*pixelSize + 2, pixelSize - 4, pixelSize - 4))

	pygame.draw.line(ui, [255,255,255], (10, 0), (xSize - 10, 0))

	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("Lights: {0}".format(lightCount), 1, (255,255,255))
	ui.blit(label, (10, 3))

	label = myfont.render("{0}".format(int(clock.get_fps())), 1, (255,255,255))
	ui.blit(label, (xSize - 20, 3))

	label = myfont.render("Alpha: {0}".format(world.get_alpha()), 1, (255,255,255))
	ui.blit(label, (200, 3))

	screen.blit(world, (0,0))
	screen.blit(ui, (0,ySize))

	clock.tick(60)
	pygame.display.flip()

pygame.quit()