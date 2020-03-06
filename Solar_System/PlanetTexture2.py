import pygame
import time
import os
from math import sqrt, sin, cos, tan, pi, asin, acos, atan
from functions import read

dir_path = os.path.dirname(os.path.realpath(__file__))

class Vec3():

	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def mult(self, n):
		return Vec3(self.x*n, self.y*n, self.z*n)

	def addVec(self, vec):
		return Vec3(self.x + vec.x, self.y + vec.y, self.z + vec.z)

	def multVec(self, vec):
		return Vec3(self.x * vec.x, self.y * vec.y, self.z * vec.z)

	def avg(self, vec):
		return self.addVec(vec).mult(.5)

	def abs(self):
		return sqrt(self.x**2 + self.y**2 + self.z**2)

	def normalise(self):
		return self.mult(1/self.abs())

	def xPhi(self):
		return atan(self.x/self.z)

	def yPhi(self):
		return atan(self.y/sqrt(self.x**2 + self.z**2))

	def dot(self, vec):
		return self.x*vec.x + self.y*vec.y + self.z*vec.z

	def ints(self):
		return (int(self.x), int(self.y), int(self.z))

class Planet():

	maxPixelRad = 20
	fov = pi/3
	rot = 0
	dist = 100
	light = Vec3(1,0,-.3).normalise()

	def __init__(self, radius, textureFile, col1, col2):
		self.radius = radius
		self._makeTexture(textureFile)
		self.col1 = Vec3(col1[0], col1[1], col1[2])
		self.col2 = Vec3(col2[0], col2[1], col2[2])

	def rotBy(self, angle):
		self.rot += angle

	def setDist(self, dist):
		self.dist = dist

	def setLight(self, light):
		self.light = light.normalise()

	def _makeTexture(self, textureFile):
		self.texture = []
		text = read(textureFile).split("\n")
		for textRow in text:
			row = []
			for patch in textRow:
				row.append(patch == "#")
			self.texture.append(row)

	def _getTexture(self, P):
		xPhi, yPhi = P.xPhi(), P.yPhi()
		yIndex = int(len(self.texture)*((yPhi - pi/2)%pi)/pi)
		xIndex = int(len(self.texture[yIndex])*((xPhi - pi/2 - self.rot)%(2*pi))*.5/pi)

		return self.texture[yIndex][xIndex]

		
	def draw(self, surf):
		xSize, ySize = surf.get_size()
		viewAngle = asin(self.radius/self.dist)
		viewRad = tan(viewAngle)*xSize/2

		self.pixel = max(1,int(viewRad/self.maxPixelRad))

		for y in range(-int(viewRad), int(viewRad) + 1, self.pixel):
			r = sqrt(viewRad**2 - y**2)
			for x in range(-int(r), int(r) + 1, self.pixel):
				xAngle = viewAngle*x/viewRad
				yAngle = viewAngle*y/viewRad

				V = Vec3(tan(xAngle), tan(yAngle), 1).normalise()
				lam = self.dist*V.z/(V.abs()**2) - sqrt((self.dist*V.z/(V.abs()**2))**2 + (self.radius**2 - self.dist**2)/(V.abs()**2))

				P = V.mult(lam).addVec(Vec3(0,0,-self.dist))

				col = (self.col1 if self._getTexture(Vec3(P.x, P.y, -P.z)) else self.col2).mult(1)

				if viewRad > 5:
					shade = P.dot(self.light)
					# if shade < 3 and shade > -3:
					# 	col = col.avg(Vec3(.9,.5,.0)).mult(.8)
					# el
					if shade < 0:
						col = col.mult(.25)

				pygame.draw.rect(surf, col.mult(255).ints(), (xSize/2 + x, ySize/2 + y, self.pixel, self.pixel))



if __name__ == "__main__":

	pygame.init()

	xSize, ySize = 1000, 750
	screen = pygame.display.set_mode((xSize, ySize))
	pygame.display.set_caption("Pygame Template")

	earth = Planet(50, "\Textures\Text_Earth.txt", [92/255,135/255,45/255], [37/255,78/255,124/255])

	clock = pygame.time.Clock()
	frameCount = 0
	done = False
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
				
		screen.fill([0,0,0])

		earth.draw(screen)
		#earth.rotBy(pi/100)
		earth.rot = mx/100
		earth.setDist(50 + ySize - my)
		earth.setLight(Vec3(10*sin(frameCount/100), 0, 10*cos(frameCount/100)))

		if frameCount%20 == 0:
			print(clock.get_fps())

		pygame.display.flip()

		clock.tick(60)

	pygame.quit()
