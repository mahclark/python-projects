import pygame
import time

xSize, ySize = 600, 450
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("fluid")

gridX = 60
gridY = 45
dye = {}
xVel = {}
yVel = {}

diffusion = 0.2
velTransfer = 1

dye[(20,44)] = 1
dye[(43,22)] = 1

xPixel = xSize/gridX
yPixel = ySize/gridY

fan = {}
fanDir = {}
wall = {}
for y in range(gridY):
	for x in range(gridX):
		wall[(x,y)] = False

# for y in range(10,30):
# 	for x in range(10,30):
# 		dye[(x,y)] = 1 

def getWall(x,y):
	return x < 0 or y < 0 or x >= gridX or y >= gridY or wall[(x,y)]

def get(dict, x, y, default=None):
	if x < 0 or y < 0 or x >= gridX or y >= gridY or getWall(x,y):
		return default
	else:
		return dict.get((x,y), 0)

def transfer(v1, v2, velocity):
	if velocity < 0:
		amt = min(-v2*velocity, 1 - v1)
		amt = -min(amt, v2)
	else:
		amt = min(v1*velocity, 1 - v2)
		amt = min(amt, v1)
	return (v1 - amt, v2 + amt)

#----------------------Main Loop----------------------
mouseHold = False
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
	mx, my = pygame.mouse.get_pos()
	mpx, mpy = int(mx/xPixel), int(my/yPixel)
	keys = pygame.key.get_pressed()
	frameCount += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseHold = True

		if event.type == pygame.MOUSEBUTTONUP:
			mouseHold = False
			
	screen.fill([255,255,255])

	(leftDown, middleDown, rightDown) = pygame.mouse.get_pressed()

	if keys[pygame.K_LSHIFT] and (leftDown or rightDown):
		wall[(mpx,mpy)] = leftDown

	elif keys[pygame.K_w] and (leftDown or rightDown):
		fan[(mpx,mpy)] = (leftDown, (0,-1))
	elif keys[pygame.K_a] and (leftDown or rightDown):
		fan[(mpx,mpy)] = (leftDown, (-1,0))
	elif keys[pygame.K_s] and (leftDown or rightDown):
		fan[(mpx,mpy)] = (leftDown, (0,1))
	elif keys[pygame.K_d] and (leftDown or rightDown):
		fan[(mpx,mpy)] = (leftDown, (1,0))

	elif leftDown or rightDown:
		for y in range(my-2,my+2):
			for x in range(mx-2,mx+2):
				dye[(int(x/xPixel),int(y/yPixel))] = leftDown

	newX = {}
	for y in range(gridY):
		for x in range(gridX):
			if not getWall(x,y):
				value = get(xVel, x, y)
				average = value
				average += get(xVel, x - 1,y,-value)
				average += get(xVel, x + 1,y,-value)
				average += get(xVel, x,y - 1,-value)
				average += get(xVel, x,y + 1,-value)
				average /= 5

				if getWall(x+1,y):
					if not getWall(x,y-1):
						yVel[(x,y-1)] = min(1,max(0, get(yVel,x,y-1) - velTransfer*value/5))
					if not getWall(x,y+1):
						yVel[(x,y+1)] = min(1,max(0, get(yVel,x,y+1) + velTransfer*value/5))

				if getWall(x-1,y):
					if not getWall(x,y-1):
						yVel[(x,y-1)] = min(1,max(0, get(yVel,x,y-1) + velTransfer*value/5))
						pygame.draw.rect(screen, [255,0,0], (x*xPixel, (y-1)*yPixel, xPixel, yPixel))
					if not getWall(x,y+1):
						yVel[(x,y+1)] = min(1,max(0, get(yVel,x,y+1) - velTransfer*value/5))
						pygame.draw.rect(screen, [255,0,0], (x*xPixel, (y+1)*yPixel, xPixel, yPixel))

				newX[(x,y)] = velTransfer*average + (1 - velTransfer)*value
				if get(fan, x, y):
					_, direction = get(fan, x, y)
					newX[(x,y)] = direction[0]

	xVel = newX

	newY = {}
	for y in range(gridY):
		for x in range(gridX):
			if not getWall(x,y):
				value = get(yVel, x,y)
				average = value
				average += get(yVel, x - 1,y,-value)
				average += get(yVel, x + 1,y,-value)
				average += get(yVel, x,y - 1,-value)
				average += get(yVel, x,y + 1,-value)
				average /= 5

				if getWall(x,y+1):
					if not getWall(x-1,y):
						xVel[(x-1,y)] = min(1,max(0, get(xVel,x-1,y) - velTransfer*value/5))
					if not getWall(x+1,y):
						xVel[(x+1,y)] = min(1,max(0, get(xVel,x+1,y) + velTransfer*value/5))

				if getWall(x,y-1):
					if not getWall(x-1,y):
						xVel[(x-1,y)] = min(1,max(0, get(xVel,x-1,y) + velTransfer*value/5))
					if not getWall(x+1,y):
						xVel[(x+1,y)] = min(1,max(0, get(xVel,x+1,y) - velTransfer*value/5))

				newY[(x,y)] = velTransfer*average + (1 - velTransfer)*value

				# if get(fan, x, y, (False))[0]:
				# 	_, direction = get(fan, x, y)
				# 	newY[(x,y)] = direction[1]
	yVel = newY

	newDye = {}
	for y in range(gridY):
		for x in range(gridX):
			if not getWall(x,y):
				value = get(dye, x,y)
				average = value
				average += get(dye, x - 1,y,value)
				average += get(dye, x + 1,y,value)
				average += get(dye, x,y - 1,value)
				average += get(dye, x,y + 1,value)
				average /= 5

				newDye[(x,y)] = diffusion*average + (1 - diffusion)*value
	dye = newDye

	# newDye = {}
	for y in range(gridY):
		for x in range(gridX):
			if not getWall(x,y):

				avgV = (get(xVel, x, y) + get(xVel, x+1, y, get(xVel, x, y)))/2
				t = transfer(get(dye, x, y), get(dye, x+1, y, get(dye, x, y)), avgV)
				dye[(x,y)] = t[0]
				dye[(x+1,y)] = t[1]

				avgV = (get(yVel, x, y) + get(yVel, x, y+1, get(yVel, x, y)))/2
				t = transfer(get(dye, x, y), get(dye, x, y+1, get(dye, x, y)), avgV)
				dye[(x,y)] = t[0]
				dye[(x,y+1)] = t[1]

	for y in range(gridY):
		for x in range(gridX):
			value = dye.get((x,y), 0)
			if getWall(x,y):
				pygame.draw.rect(screen, [20,100,250], (x*xPixel, y*yPixel, xPixel, yPixel))
			# elif get(fan, x, y, (False))[0]:
			# 	pygame.draw.rect(screen, [20,200,100], (x*xPixel, y*yPixel, xPixel, yPixel))				
			elif value > 0:
				pygame.draw.rect(screen, [255*(1-value),255*(1-value),255*(1-value)], (x*xPixel, y*yPixel, xPixel, yPixel))

	value = max(0,min(1,get(yVel,0,20)))
	
	pygame.draw.rect(screen, [255*value,0,255*(1-value)], (0*xPixel, 20*yPixel, xPixel, yPixel))

	pygame.display.flip()
	clock.tick(60)

pygame.quit()