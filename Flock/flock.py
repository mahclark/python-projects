import pygame
import time
from random import randint, random
from math import sin, cos, pi, sqrt, atan2

xSize, ySize = 600, 450
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("flock")

def toAngle(vec):
	return (atan2(vec.y, -vec.x) - pi/2)%(2*pi)

def toVec(angle):
	return Vec2(sin(angle), cos(angle))

class Vec2():

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def ints(self):
		return (int(self.x), int(self.y))

	def inBounds(self):
		if self.x < 0 or self. y < 0 or self.x >= xSize or self.y >+ ySize:
			return False
		return True

class Bish():

	sightRad = 50
	speed = 2
	dirc = 0
	desi = 0
	nearby = []

	def __init__(self, pos=Vec2(xSize/2,ySize/2)):
		self.pos = pos

	def move(self):
		xVel = self.speed*sin(self.dirc)
		yVel = self.speed*cos(self.dirc)

		self.pos.x += xVel
		self.pos.y += yVel

	def _rotBy(self, dt):
		self.dirc += dt
		self.dirc = self.dirc%(2*pi)

	def _rotDesiBy(self, dt):
		desi += dt
		desi = desi%(2*pi)

	def _rotToDesi(self):
		diff0 = self.desi - self.dirc + 2*pi
		diff1 = self.desi - self.dirc
		diff2 = self.desi - self.dirc - 2*pi

		minAbs = min([abs(diff0), abs(diff1), abs(diff2)])

		if minAbs == abs(diff0):
			diff = diff0
		elif minAbs == abs(diff1):
			diff = diff1
		else:
			diff = diff2

		self._rotBy(diff/10)

	def rotate(self):

		#Check for walls
		angle0 = self.dirc
		weight0 = 1
		attempts = 10
		for attempt in range(0,attempts):
			dAngle = pi*attempt/attempts

			angle0 = self.dirc + dAngle*(2*(attempt%2) - 1)
			checkPos = Vec2(
				self.pos.x + self.sightRad*sin(angle0),
				self.pos.y + self.sightRad*cos(angle0))

			if checkPos.inBounds():
				if attempt != 0: weight0 = 50
				break

		#Deisre to isolate
		angle1 = self.dirc
		weight1 = 0
		minD, minB = self.sightRad, None
		for bish, dist in self.nearby:
			if dist < minD:
				minD, minB = dist, bish

		if minB != None:
			dx = minB.pos.x - self.pos.x
			dy = minB.pos.y - self.pos.y
			angle1 = toAngle(Vec2(-dx, -dy))
			weight1 = 3*self.sightRad/(minD + 0.01)

		#Desire to align
		angle2 = toAngle(Vec2(
			sum([toVec(bish.dirc).x for bish, _ in self.nearby]),
			sum([toVec(bish.dirc).y for bish, _ in self.nearby])
			))

		weight2 = 5
		if len(self.nearby) == 0:
			weight2 = 0

		#Desire to move to centre
		dx = sum([bish.pos.x - self.pos.x for bish, _ in self.nearby])
		dy = sum([bish.pos.y - self.pos.y for bish, _ in self.nearby])
		angle3 = toAngle(Vec2(dx, dy))

		if len(self.nearby) == 0:
			weight3 = 0
		else:
			dist = sqrt((dx/len(self.nearby))**2 + (dy/len(self.nearby))**2)
			weight3 = dist*sqrt(len(self.nearby))/10

		#Weight the desires
		params = [(angle0, weight0), (angle1, weight1), (angle2, weight2), (angle3, weight3)]
		self.desi = toAngle(Vec2(
			sum([toVec(angle).x*weight for angle, weight in params]),
			sum([toVec(angle).y*weight for angle, weight in params])
			))

		#self.speed = 2 + sum([weight for _, weight in params])/40

		self._rotToDesi()

	def seek(self, bishes):
		self.nearby = []
		for bish in bishes:
			dx = bish.pos.x - self.pos.x
			dy = bish.pos.y - self.pos.y
			if abs(dx) < self.sightRad and abs(dy) < self.sightRad:
				dist = sqrt(dx**2 + dy**2)
				if dist < self.sightRad and dist > 0:
					self.nearby.append((bish, dist))

	def mate(self, flock):
		if len(self.nearby) > 0:
			if random() < 0.001:
				flock.add(self.pos)


class Flock():

	bishes = []

	def __init__(self, n=1):
		for i in range(n):
			self.bishes.append(Bish(Vec2(xSize*random(), ySize*random())))
			self.bishes[-1].dirc = random()*2*pi
			self.bishes[-1].desi = random()*2*pi

	def add(self, pos):
		bish = Bish(Vec2(pos.x, pos.y))
		#bish.pos.x += 40*random() - 20
		#bish.pos.y += 40*random() - 20
		bish.dirc = random()*2*pi
		bish.desi = random()*2*pi
		#bish.seek(self.bishes)
		#bish.rotate()

		self.bishes.append(bish)

	def move(self):
		for bish in self.bishes:
			bish.mate(self)
			bish.move()
			bish.seek(self.bishes)
			bish.rotate()

			bish.desi = pi + pi/2

	def draw(self):
		scene = pygame.Surface((xSize, ySize), pygame.SRCALPHA, 32)

		for bish in self.bishes:
			pygame.draw.polygon(scene, [0,0,255], (
				(bish.pos.x + 16*sin(bish.dirc),		bish.pos.y + 16*cos(bish.dirc)),
				(bish.pos.x + 5*sin(bish.dirc - pi/2),	bish.pos.y + 5*cos(bish.dirc - pi/2)),
				(bish.pos.x + 5*sin(bish.dirc + pi/2),	bish.pos.y + 5*cos(bish.dirc + pi/2))
				))

		screen.blit(scene, (0,0))

flock = Flock(3)

# a = 0
# print(a)
# v = toVec(a)
# print(v.x, v.y)
# print(toAngle(v))

#----------------------Main Loop----------------------
mouseHold = False
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
	mx, my = pygame.mouse.get_pos()
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

	flock.move()
	flock.draw()

	if frameCount > 5000:
		print("TIMEOUT")
		done = True

	pygame.display.flip()
	clock.tick(60)

pygame.quit()