import pygame
import time
from random import randint
from math import atan2, pi, sqrt
import flock

xSize, ySize = flock.xSize, flock.ySize
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Shadows")

mouseHold = False

blockColor = (50,90,230)

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
		


class Block():

	def __init__(self, points):
		self.points = [Vec2(p[0],p[1]) for p in points]
		self.center = Vec2.average(self.points)

	def draw(self, surf):
		pygame.draw.polygon(surf, blockColor, [p.toPair() for p in self.points])

	def shade(self, surf, light):
		angles = []
		for point in self.points:
			d = point.addVec(light.mult(-1))

			angles.append(d.toAngle())

		angles = [(a - self.center.addVec(light.mult(-1)).toAngle() + pi)%(2*pi) for a in angles]

		high = angles.index(max(angles))
		low = angles.index(min(angles))

		shadowPoints = []
		adding = False
		for n, point in enumerate(self.points):
			if adding:
				shadowPoints.append(point.toPair())

			if n == high or n == low:
				if adding: break
				adding = True
				shadowPoints.append(light.addVec(self.points[high + low - n].addVec(light.mult(-1)).sendOffScreen()).toPair())

				corners = [self.points[high], self.points[low], Vec2(0,0), Vec2(xSize,0), Vec2(xSize,ySize), Vec2(0,ySize)]
				adj_corners = [(a.addVec(light.mult(-1)).toAngle() - self.center.addVec(light.mult(-1)).toAngle() + pi)%(2*pi) for a in corners]
				s_corners = sorted(adj_corners)
				d = (adj_corners[n == low] > adj_corners[n == high])*2 - 1
				index = s_corners.index(adj_corners[n == high])
				while True:
					index += d
					if (index == s_corners.index(adj_corners[n == low])):
						break
					shadowPoints.append(corners[adj_corners.index(s_corners[index])].toPair())

				# for corner in [Vec2(0,0), Vec2(xSize,0), Vec2(xSize,ySize), Vec2(0,ySize)]:
				# 	trio = [(a.addVec(light.mult(-1)).toAngle() - self.center.addVec(light.mult(-1)).toAngle() + pi)%(2*pi) for a in [corner, self.points[high], self.points[low]]]
				# 	if trio.index(max(trio)) and trio.index(min(trio)):
				# 		shadowPoints.append(corner.toPair())

				shadowPoints.append(light.addVec(self.points[n].addVec(light.mult(-1)).sendOffScreen()).toPair())
				shadowPoints.append(point.toPair())

		pygame.draw.polygon(surf, [0,0,0], shadowPoints)#[255*0.7,240*0.7,230*0.7]



class Scene():
	blocks = []

	def __init__(self):
		pass

	def add(self, block):
		self.blocks.append(block)

	def draw(self, surf):		
		for block in self.blocks:
			block.draw(surf)

	def shade(self, surf, light):
		s = pygame.Surface((xSize,ySize))
		s.fill([255,255,255])
		s.set_alpha(68)

		for block in self.blocks:
			block.shade(s, light)

		surf.blit(s,(0,0))

	def collides(self, checkPos):
		try:
			return screen.get_at(checkPos.ints()) in [blockColor, (187, 176, 168)]
		except: #Offscreen
			return True

scene = Scene()
scene.add(Block([(50,50),(100,46),(200,155),(150,200)]))
scene.add(Block([(250,250),(300,246),(400,355)]))
scene.add(Block([(700,130),(700,300),(920,200)]))
scene.add(Block([(620,460),(590,390),(730,391),(720,500)]))

light = Vec2(400,200)

birds = flock.Flock(100)

#----------------------Main Loop----------------------#

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
	frameCount += 1
	mx, my = pygame.mouse.get_pos()
	keys = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseHold = True
			print(screen.get_at((mx,my)))

		if event.type == pygame.MOUSEBUTTONUP:
			mouseHold = False

	light = birds.move(True, flock.Vec2(mx, my), mouseHold, scene)
	if keys[pygame.K_LSHIFT]:
		light = Vec2(mx,my)

	screen.fill([255,240,230])

	screen.blit(birds.draw(), (0,0))

	scene.shade(screen, light)
	scene.draw(screen)

	if (frameCount > 60*60*3):
		print("TIMEOUT")
		done = True

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
