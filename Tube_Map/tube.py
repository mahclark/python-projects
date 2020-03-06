import pygame
import time
from random import choice, randint
from name import generateStation

pygame.init()
displayFont = pygame.font.SysFont("monospace", 15)
xGrid, yGrid = 15,10

class Vec2():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def addVec(self, vec):
		return Vec2(self.x + vec.x, self.y + vec.y)

	def toScreen(self, size):
		return Vec2(size[0]*(self.x + 1)/(xGrid + 2), size[1]*(self.y + 1)/(yGrid + 2))

	def ints(self):
		return (int(self.x), int(self.y))

class Station():

	def __init__(self, posOrX, y=None):
		self.pos = posOrX if y == None else Vec2(posOrX, y)
		self.name = generateStation()

	def draw(self, surf):
		pygame.draw.circle(surf, [0,0,255], self.pos.toScreen(surf.get_size()).ints(), 10)
		pygame.draw.circle(surf, [255,255,255], self.pos.toScreen(surf.get_size()).ints(), 7)
		label = displayFont.render(self.name, 1, [0,0,0])
		surf.blit(label, self.pos.toScreen(surf.get_size()).addVec(Vec2(5,5)).ints())

class Line():

	# direc = Vec2(1,1)
	# points = []
	# col = [255,0,0]

	def __init__(self, pos, direc, col):
		self.pos = pos
		self.direc = direc
		self.col = col
		self.points = []
		self.points.append(self.pos)
		self._walk(20)

	def _walk(self, n):
		if n == 0: return

		self.pos = self.pos.addVec(Vec2(choice([0, self.direc.x]), choice([0, self.direc.y])))
		self.points.append(self.pos)

		self._walk(n - 1)

	def draw(self, surf):
		for n in range(len(self.points) - 1):
			pygame.draw.line(surf, self.col, self.points[n].toScreen(surf.get_size()).ints(), self.points[n + 1].toScreen(surf.get_size()).ints(), 5)


class Map():

	stations = []

	def __init__(self, noStations):
		for _ in range(noStations):
			self.stations.append(Station(randint(0, xGrid), randint(0, yGrid)))

	def draw(self, surf):
		for station in self.stations:
			station.draw(surf)

if __name__ == "__main__":
	xSize, ySize = 1200,800
	screen = pygame.display.set_mode((xSize, ySize))
	pygame.display.set_caption("Tube Map")

	map = Map(20)
	line1 = Line(Vec2(0,0), Vec2(1,1), [255,0,0])
	line2 = Line(Vec2(15,0), Vec2(-1,1), [0,0,125])

	clock = pygame.time.Clock()
	frameCount = 0
	mouseHold = False
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

		screen.fill([255,255,255])

		line1.draw(screen)
		line2.draw(screen)
		map.draw(screen)

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
