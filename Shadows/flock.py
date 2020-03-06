import pygame
import time
from random import randint, random
import operator
from math import sin, cos, pi, sqrt, atan2

xSize, ySize = 1200, 600
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("flock")

adultAge = 700
margin = 20
bish_col = [20,200,90]

followTheLeader = False
grandmasFootsteps = False
ringOfFire = False

def toVec(angle):
	return Vec2(sin(angle), cos(angle))

class Vec2():

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def ints(self):
		return (int(self.x), int(self.y))

	def inBounds(self):
		if self.x < margin or self. y < margin or self.x >= xSize - margin or self.y >= ySize - margin:
			return False
		return True

	def collides(self, rect):
		return rect.collidepoint(self.x, self.y)

	def length(self):
		return sqrt(self.x**2 + self.y**2)

	def toAngle(self):
		return (atan2(self.y, -self.x) - pi/2)%(2*pi)

	def abs(self):
		return sqrt(self.x**2 + self.y**2)

	def mult(self, n):
		return Vec2(self.x*n, self.y*n)

	def addVec(self, vec):
		return Vec2(self.x + vec.x, self.y + vec.y)

	def sendOffScreen(self):
		return self.mult(Vec2(xSize,ySize).abs()/self.abs())

	def avg(self, vec):
		return self.addVec(vec).mult(0.5)

	def toPair(self):
		return (self.x, self.y)

	def toIntPair(self):
		return (int(self.x), int(self.y))

	def toAngle(self):
		return (atan2(self.y, -self.x) - pi/2)%(2*pi)

	def average(vecs):
		return Vec2(sum([vec.x for vec in vecs])/len(vecs), sum([vec.y for vec in vecs])/len(vecs))

predatorDists = []

class Bish():

	sightRad = 50
	speed = 3
	dirc = 0
	desi = 0
	nearby = []
	age = adultAge - 200
	predator = False
	vel = Vec2(0,0)

	def __init__(self, pos=Vec2(xSize/2,ySize/2)):
		self.pos = pos

	def move(self, obstacles):
		self.vel.x = self.speed*sin(self.dirc)
		self.vel.y = self.speed*cos(self.dirc)

		if self.predator or not obstacles.collides(self.pos.addVec(self.vel)):
			self.pos.x += self.vel.x
			self.pos.y += self.vel.y

	def _rotBy(self, dt):
		self.dirc += dt
		self.dirc = self.dirc%(2*pi)

	def _rotDesiBy(self, dt):
		desi += dt
		desi = desi%(2*pi)

	def _rotToDesi(self, factor=10):
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

		self._rotBy(diff/factor)

	def rotate(self, mousePos, mouseHold, predator, obstacles, flock):

		#Deisre to isolate
		angle1 = self.dirc
		weight1 = 0		

		minD, minB = self.sightRad, None
		for bish, dist in self.nearby:
			if dist < minD:
				minD, minB = dist, bish

		if minB != None:
			dx = sum([(bish.pos.x - self.pos.x)/(dist + 0.01) for bish, _ in self.nearby])
			dy = sum([(bish.pos.y - self.pos.y)/(dist + 0.01) for bish, _ in self.nearby])
			angle1 = Vec2(-dx, -dy).toAngle()

			weight1 = 3*self.sightRad/(minD**0.9 + 0.001)

		#Desire to align
		angle2 = Vec2(
			sum([toVec(bish.dirc).x for bish, _ in self.nearby]),
			sum([toVec(bish.dirc).y for bish, _ in self.nearby])
			).toAngle()

		weight2 = 5
		if len(self.nearby) == 0:
			weight2 = 0

		#Desire to move to centre
		dx = sum([bish.pos.x - self.pos.x for bish, _ in self.nearby])
		dy = sum([bish.pos.y - self.pos.y for bish, _ in self.nearby])
		angle3 = Vec2(dx, dy).toAngle()

		if len(self.nearby) == 0:
			weight3 = 0
		else:
			dist = sqrt((dx/len(self.nearby))**2 + (dy/len(self.nearby))**2)
			weight3 = dist*sqrt(len(self.nearby))/10

		#Run away
		angle4 = self.dirc
		weight4 = 0
		d = Vec2(self.pos.x - mousePos.x, self.pos.y - mousePos.y)
		if mouseHold and (d.length() >= self.sightRad*2 or not ringOfFire):
			d.x = -d.x
			d.y = -d.y

		if d.length() < self.sightRad*2 or mouseHold:
			angle4 = d.toAngle()
			weight4 = 200
			self.speed = 6 if not mouseHold else 3 + 5*(1.02**(40 - d.length()))
		else:
			self.speed = 0 if grandmasFootsteps else 3

		if self.predator: self.speed = len(flock.bishes)/25

		#Follow the leader
		angle5 = self.dirc
		weight5 = 3 if not self.predator else 0
		d = Vec2(predator.pos.x - self.pos.x, predator.pos.y - self.pos.y).mult(-1)
		dist = d.abs()
		if not self.predator:
			predatorDists.append(dist)
		if dist != 0:
			weight5 *= 200/dist
		angle5 = d.toAngle()

		if self.predator:
			weight5 = 20
			m = min(predatorDists)
			pos = flock.bishes[predatorDists.index(m)].pos
			angle5 = Vec2(pos.x - self.pos.x, pos.y - self.pos.y).toAngle()
			if m < 20:
				flock.eliminate(predatorDists.index(m))
				self.move(obstacles)
				self.move(obstacles)

		#Weight the desires
		params = [(angle1, weight1), (angle2, weight2), (angle3, weight3), (angle4, weight4), (angle5, weight5)]
		desired = Vec2(
			sum([toVec(angle).x*weight for angle, weight in params]),
			sum([toVec(angle).y*weight for angle, weight in params])
			).toAngle()

		#self.speed = 2 + sum([weight for _, weight in params])/40

		#Check for walls/obstacles
		attempts = 50
		for attempt in range(0,attempts):
			dAngle = pi*attempt/attempts

			final = desired + dAngle*(2*(attempt%2) - 1)
			checkPos = Vec2(
				self.pos.x + self.sightRad*sin(final),
				self.pos.y + self.sightRad*cos(final))

			if checkPos.inBounds() and not obstacles.collides(checkPos):
				self.desi = final

				if attempt != 0: self._rotToDesi(5)
				break

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

		self.nearby.sort(key=operator.itemgetter(1))

	def mate(self, flock):
		if len(self.nearby) > 0:# and self.age >= adultAge:
			if random() < 0.0003:
				flock.add(self.pos)
				print(len(flock.bishes))

class Particle():

	def __init__(self, center, vel):
		self.center = center
		self.pos = Vec2(center.x, center.y)
		angle = random()*2*pi
		self.vel = Vec2(cos(angle)*5*random(), sin(angle)*5*random()).addVec(vel.mult(2))
		if randint(0,20) == 0:
			self.vel = self.vel.mult(2)
		if randint(0,1) == 0:
			self.col = [240,20,90]
		else:
			self.col = [15,150,60]

	def move(self, obstacles):
		self.pos = self.pos.addVec(self.vel)
		self.vel = self.vel.mult(0.8)
		if obstacles.collides(self.pos):
			self.vel = Vec2(0,0)

	def draw(self, surf):
		pygame.draw.rect(surf, self.col, self.pos.ints() + (2,2))

class Flock():

	bishes = []
	particles = []

	def __init__(self, n, obstacles):
		for i in range(n):
			pos = Vec2(xSize*random(), ySize*random())
			while obstacles.collides(pos):
				pos = Vec2(xSize*random(), ySize*random())

			self.bishes.append(Bish(pos))
			self.bishes[-1].dirc = random()*2*pi
			self.bishes[-1].desi = random()*2*pi
		self.bishes[-1].predator = True
		self.bishes[-1].age += 100

	def add(self, pos):
		bish = Bish(Vec2(pos.x, pos.y))
		bish.dirc = random()*2*pi
		bish.desi = random()*2*pi

		self.bishes = [bish] + self.bishes

	def move(self, shouldSeek, mousePos, mouseHold, obstacles):
		for particle in self.particles:
			particle.move(obstacles)

		predatorDists.clear()
		for bish in self.bishes:
			bish.mate(self)
			bish.move(obstacles)
			if shouldSeek: bish.seek(self.bishes)
			bish.rotate(mousePos, mouseHold, self.bishes[-1], obstacles, self)

		return self.bishes[-1].pos

	def draw(self):
		scene = pygame.Surface((xSize, ySize), pygame.SRCALPHA, 32)

		for particle in self.particles:
			particle.draw(scene)

		for bish in self.bishes:
			col = bish_col if bish != self.bishes[-1] else [240, 200, 10]
			pygame.draw.polygon(scene, col, (
				(bish.pos.x + 16*sin(bish.dirc)*(bish.age + 200)/adultAge,			bish.pos.y + 16*cos(bish.dirc)*(bish.age + 200)/adultAge),
				(bish.pos.x + 5*sin(bish.dirc - pi/2)*(bish.age + 200)/adultAge,	bish.pos.y + 5*cos(bish.dirc - pi/2)*(bish.age + 200)/adultAge),
				(bish.pos.x + 5*sin(bish.dirc + pi/2)*(bish.age + 200)/adultAge,	bish.pos.y + 5*cos(bish.dirc + pi/2)*(bish.age + 200)/adultAge)
				))

			#pygame.draw.line(scene, [255,0,0], bish.pos.ints(), Vec2(bish.pos.x + bish.sightRad*toVec(bish.desi).x, bish.pos.y + bish.sightRad*toVec(bish.desi).y).ints())

		#obstacles.draw(scene)

		return scene
		#screen.blit(scene, (0,0))

	def eliminate(self, n):
		for _ in range(200):
			self.particles.append(Particle(self.bishes[n].pos, self.bishes[n].vel))
			if len(self.particles) > 2000:
				del self.particles[randint(0, len(self.particles) - 1)]
		del self.bishes[n]

class Obstacles():

	rects = []

	def __init__(self): pass

	def add(self, x, y, width, height):
		self.rects.append(pygame.Rect(x, y, width, height))

	def draw(self, surf):
		for rect in self.rects:
			pygame.draw.rect(surf, [0,0,0], rect)

	def collides(self, pos):
		for rect in self.rects:
			newRect = pygame.Rect(rect.x - margin, rect.y - margin, rect.width + margin*2, rect.height + margin*2)
			if pos.collides(newRect):
				return True
		return False


if __name__ == "__main__":

	obstacles = Obstacles();
	flock = Flock(200)

	#obstacles.add(400,300,100,300)

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
				
		#if frameCount%120 == 0:
		screen.fill([20,20,20])

		flock.move(True, Vec2(mx, my), mouseHold)
		flock.draw()

		if frameCount > 5000:
			print("TIMEOUT")
			done = True

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()