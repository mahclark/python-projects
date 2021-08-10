import pygame
import time
from math import sqrt
from random import randint

class Vec2():

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def abs(self):
		return sqrt(self.x**2 + self.y**2)

	def mult(self, n):
		return Vec2(self.x*n, self.y*n)

	def addVec(self, vec):
		return Vec2(self.x + vec.x, self.y + vec.y)

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

class FixedPoint():

	join = None

	def __init__(self, pos, index1, index2):
		self.pos = pos
		self.minIndex = min(index1, index2)
		self.maxIndex = max(index1, index2)

	def draw(self, surf):
		if self.join != None:
			pygame.draw.line(surf, [0,0,0], self.pos.toIntPair(), self.join.pos.toIntPair())
		else:
			surf.set_at(self.pos.toIntPair(), [0,0,0])

class Voronoi():

	lineOffset = 0
	fixed = []
	unjoined = []
	#ants = []
	done = False
	maxIndexes = {}

	def __init__(self, points, surf):
		self.points = [Vec2(x, y) for x, y in points]
		self.surf = surf
		self.xSize, self.ySize = surf.get_size()
		self.ants = [Vec2(0,0) for _ in range(self.ySize)]

	def _setMinDist(self, pos):
		xs = []
		for point in self.points:
			if point.x < self.lineOffset:
				xs.append((point.x**2 - self.lineOffset**2 + (pos.y - point.y)**2)/(2*point.x - 2*self.lineOffset))
			else:
				xs.append(-1)

		pos.x = max(xs)

		maxIndex = xs.index(pos.x)

		if pos.y in self.maxIndexes and maxIndex != self.maxIndexes[pos.y]:
			self.fixed.append(self.ants[pos.y])

		self.maxIndexes[pos.y] = maxIndex


	def advance(self):
		if self.done:
			return

		self.lineOffset += 1
		self.done = True
		for y in range(self.ySize):
			pos = Vec2(0, y)
			self._setMinDist(pos)

			self.ants[pos.y] = pos

			if pos.x < self.xSize:
				self.done = False

	def draw(self):
		for point in self.points:
			pygame.draw.rect(self.surf, [255,0,0], point.toIntPair() + (2,2,))

		for fixed in self.fixed:
			#fixed.draw(self.surf)
			#print(fixed)
			self.surf.set_at(fixed.toIntPair(), [0,0,0])

		for i in range(len(self.ants) - 1):
			pygame.draw.line(self.surf, [0,0,255], self.ants[i].toIntPair(), self.ants[i + 1].toIntPair())

		pygame.draw.line(self.surf, [0,0,0], (self.lineOffset, 0), (self.lineOffset, self.ySize))

	def flip(x):
		return [(v, u) for (u, v) in x]
	def flipVec(x):
		return [Vec2(v.y, v.x) for v in x]

if __name__ == "__main__":
	xSize, ySize = 500, 500
	screen = pygame.display.set_mode((xSize, ySize))
	pygame.display.set_caption("Voronoi")

	#voronoi = Voronoi([(20, 100), (20, 300)], screen)
	#points = [(300,300),(300,100),(500,200),(500,400),(100,400),(100,200)]
	points = [(randint(0, xSize - 1), randint(0, ySize - 1)) for _ in range(1000)]
	voronoi = Voronoi(Voronoi.flip(points), screen)

	# while not voronoi.done:
	# 	voronoi.advance()
	# fixed = voronoi.fixed
	# voronoi = Voronoi(points, screen)
	# voronoi.fixed = Voronoi.flipVec(fixed)


	clock = pygame.time.Clock()
	frameCount = 0
	done = False
	mouseHold = False
	while not done:
		frameCount += 1
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseHold = True

			if event.type == pygame.MOUSEBUTTONUP:
				mouseHold = False
				
		screen.fill([255,255,255])

		voronoi.advance()
		voronoi.draw()

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
