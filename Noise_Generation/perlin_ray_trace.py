import pygame
import time
import threading
import perlin_noise
from math import sqrt, pi, cos, sin, atan, atan2, acos, ceil
from Vec2 import Vec2
from random import random

class Vec3:

	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def mod(self):
		return sqrt(self.x**2 + self.y**2 + self.z**2)

	def normalise(self):
		mod = self.mod()
		if mod == 0:
			return self.copy()
		return self.mult(1/mod)

	def mult(self, a):
		return Vec3(self.x*a, self.y*a, self.z*a)

	def multVec(self, v):
		return Vec3(self.x*v.x, self.y*v.y, self.z*v.z)

	def addVec(self, v):
		return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

	def dot(self, v):
		return self.x*v.x + self.y*v.y + self.z*v.z

	def rotX(self, a):
		return Vec3(
			self.x,
			self.y*cos(a) - self.z*sin(a),
			self.y*sin(a) + self.z*cos(a))

	def rotY(self, a):
		return Vec3(
			self.x*cos(a) + self.z*sin(a),
			self.y,
			-self.x*sin(a) + self.z*cos(a))

	def rotZ(self, a):
		return Vec3(
			self.x*cos(a) - self.y*sin(a),
			self.x*sin(a) - self.y*cos(a),
			self.z)

	def copy(self):
		return Vec3(self.x, self.y, self.z)

	def rawInts(self):
		return (int(self.x), int(self.y), int(self.z))

	def raw(self):
		return (self.x, self.y, self.z)

	def lerp(v1, v2, i):
		return Vec3(v1.x*(1 - i) + v2.x*i, v1.y*(1 - i) + v2.y*i, v1.z*(1 - i) + v2.z*i)

class Camera:

	def __init__(self, pos, rot):
		self.pos = pos
		self.rot = rot

	def fromViewVec(pos, v):
		x = atan2(v.y, sqrt(v.x**2 + v.z**2))
		y = atan2(v.z, v.x) - pi/2
		if y < -pi:
			y += 2*pi

		return Camera(pos, Vec3(x, y, 0))

class Renderer:

	waterLevel = 0.5
	peakLevel = 0.7

	waterCol = Vec3(0.2, 0.34, 0.66)
	landCol = Vec3(0.29, 0.68, 0.3)
	peakCol = Vec3(1,1,1)
	skyCol = Vec3(82, 162, 209).mult(1/255)#Vec3(0.72, 0.87, 0.94).mult(1/2)
	sunCol = Vec3(252,248,192).mult(1/255)
	sunsetCol = Vec3(227, 124, 34).mult(1/255)

	def __init__(self, pixelSize=10, xLand=400, yLand=400):
		self.camera = Camera(Vec3(200, 6, 200), Vec3(-pi/2,0,0))
		self.pixelSize = pixelSize
		self.xLand, self.yLand = xLand, yLand
		self.sunVec = Vec3(1,0,1).normalise()
		self.generated = False
		self.rendering = False


	def makeLand(self):
		xLand, yLand = self.xLand, self.yLand
		(v0, n0) = perlin_noise.makeNoise((200,200), (xLand, yLand))
		(v1, n1) = perlin_noise.makeNoise((50,50), (xLand, yLand))
		(v2, n2) = perlin_noise.makeNoise((25,25), (xLand, yLand))
		(v3, n3) = perlin_noise.makeNoise((10,10), (xLand, yLand))

		print("rendering landscape...")

		valueLevels = [v0,v1,v2,v3]
		normalLevels = [n0,n1,n2,n3]

		levelWeights = (1, 0.3, 0.2, 0.1)

		self.maxHeight = 0
		self.heights = []
		self.normals = []

		for y in range(yLand):
			row = []
			for x in range(xLand):

				value = (sum([levelWeights[i]*valueLevels[i][y][x] for i in [0,1,2]]) + sum(levelWeights))/2/sum(levelWeights)

				if value > self.peakLevel:
					value = (value - self.peakLevel)*3 + self.peakLevel

				if value > self.maxHeight:
					self.maxHeight = value

				# if value < self.waterLevel:
				# 	value = self.waterLevel

				row.append(value)
			self.heights.append(row)

		for y in range(yLand):
			row = []
			for x in range(xLand):

				value = self.heights[y][x]

				normalSum = Vec3()
				for normalLevel, weight in zip(normalLevels, levelWeights):
					v = normalLevel[y][x]
					vec3 = Vec3(v[0], v[2], v[1])
					normalSum = normalSum.addVec(vec3.mult(weight))

				normal = normalSum.normalise()
				row.append(normal)
			self.normals.append(row)

		self.generated = True

	def draw(self, surf):
		self.rendering = True
		xSize, ySize = surf.get_size()
		xGrid, yGrid = xSize//self.pixelSize, ySize//self.pixelSize

		xWeight = 1
		yWeight = 100
		zWeight = 1

		for y in range(yGrid):
			for x in range(xGrid):
				ray = Vec3((xGrid//2 - x), (y - yGrid//2), xGrid).normalise()
				ray = ray.rotX(self.camera.rot.x)
				ray = ray.rotY(-self.camera.rot.y)
				ray = ray.rotZ(self.camera.rot.z)
				ray = ray.multVec(Vec3(1/xWeight, 1/yWeight, 1/zWeight))

				ray = self.scaleRay(ray)

				col = self.trace(self.camera.pos, ray).mult(255).rawInts()
				pygame.draw.rect(surf, col, (x*pixelSize, y*pixelSize, pixelSize, pixelSize))

		self.rendering = False

	def scaleRay(self, ray):
		scale = 1

		if ray.x != 0 and ray.z != 0:
			scale = min(1/abs(ray.x), 1/abs(ray.z))
			ray2 = ray.mult(scale)
			if 1/abs(ray.x) < 1/abs(ray.z):
				ray2.x = 1
			else:
				ray2.z = 1
		elif ray.x != 0:
			scale = 1/ray.x
			ray2 = 1
			ray2.x = int(ray2.x)
		elif ray.z != 0:
			scale = 1/ray.z
			ray2 = ray.mult(scale)
			ray2.z = 1

		return ray2

	def draw2D(self, surf):
		xSize, ySize = surf.get_size()

		for y in range(ySize):
			for x in range(xSize):
				yPos = int(y*yLand/ySize)
				xPos = int(x*xLand/xSize)

				height = self.heights[yPos][xPos]

				if height <= self.waterLevel:
					col = self.waterCol
				else:
					col = Vec3((height - 0.5)/(self.maxHeight - 0.5), height/self.maxHeight, (height - 0.5)/(self.maxHeight - 0.5))

				pygame.draw.rect(surf, col.mult(255).rawInts(), (x, y, 1, 1))


	def trace(self, origin, ray, reflectLimit=5):
		# if origin.y <= self.heights[origin.z][origin.x]:
		# 	return Vec3(1,0,0)

		current = origin.copy()
		while True:
			current = current.addVec(ray)

			# print(ray.raw(), current.raw())
			rayWaterAngle = atan(ray.y/sqrt(ray.x**2 + ray.z**2))

			if (current.x > self.xLand - 1 and ray.x >= 0) or (current.x < 0 and ray.x <= 0) or (current.z > self.yLand - 1 and ray.z >= 0) or (current.z < 0 and ray.z <= 0) or (current.y < 0 and ray.y <= 0) or (current.y > self.maxHeight and ray.y >= 0):
				angleToSun = acos(ray.multVec(Vec3(1,100,1)).normalise().dot(self.sunVec))
				if ray.y < 0:
					newOrigin = current.addVec(ray.mult((self.waterLevel - current.y)/ray.y))
					return self.traceWater(reflectLimit, ray, newOrigin, height, rayWaterAngle)

				if angleToSun < pi/64:
					return self.sunCol
				return Vec3.lerp(self.sunsetCol, self.skyCol, max(0, min(1, rayWaterAngle*200 + angleToSun/(pi/2))))

			if current.x > self.xLand - 1 or current.x < 0 or current.z > self.yLand - 1 or current.z < 0:
				continue

			current.x = int(current.x*100)/100
			current.z = int(current.z*100)/100

			if current.x % 1 == 0 and current.z % 1 == 0:
				height = self.heights[int(current.z)][int(current.x)]
			elif current.x % 1 == 0:
				height1 = self.heights[int(current.z)][int(current.x)]
				height2 = self.heights[ceil(current.z)][int(current.x)]
				height = height2*(current.z - int(current.z)) + height1*(ceil(current.z) - current.z)
			else:
				if current.z % 1 != 0:
					print(current.raw(), ray.raw())
				assert current.z % 1 == 0
				height1 = self.heights[int(current.z)][int(current.x)]
				height2 = self.heights[int(current.z)][ceil(current.x)]
				height = height2*(current.x - int(current.x)) + height1*(ceil(current.x) - current.x)

			if current.y <= max(height, self.waterLevel):
				normal = self.normals[int(current.z)][int(current.x)]
				if height <= self.waterLevel:
					return self.traceWater(reflectLimit, ray, current, height, rayWaterAngle)

				elif height <= self.peakLevel:
					if self.sunVec.dot(normal) >= 0:
						return self.landCol
					else:
						return self.landCol.mult(0.5)
				else:
					if self.sunVec.dot(normal) >= 0:
						return self.peakCol
					else:
						return self.peakCol.mult(0.5)

	def traceWater(self, reflectLimit, ray, current, height, rayWaterAngle):
		if reflectLimit == 0:
			return self.waterCol

		refRay = Vec3(ray.x, -ray.y*(random()%0.2 + 0.8), ray.z).rotY((random() - 0.5)/50)
		refRay = self.scaleRay(refRay)
		reflectCol = self.trace(Vec3(int(current.x), self.waterLevel, int(current.z)), refRay, reflectLimit - 1)
		
		
		return Vec3.lerp(reflectCol, self.waterCol, (0.1 - rayWaterAngle/(0.2 + pi/2)))


	def getInfo(self, u, v):
		x = int(u*self.xLand)
		y = int(v*self.yLand)

		return (x, y, self.heights[y][x])

class Generator(threading.Thread):

	def __init__(self, threadID, surf, renderer):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.surf = surf
		self.renderer = renderer

	def run(self):
		renderer.makeLand()
		renderer.draw2D(self.surf)

class RenderThread(threading.Thread):

	def __init__(self, threadID, surf, renderer):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.surf = surf
		self.renderer = renderer

	def run(self):
		renderer.draw(self.surf)

if __name__ == "__main__":
	xSize, ySize = 1400, 600
	screen = pygame.display.set_mode((xSize, ySize))
	pygame.display.set_caption("Perlin Ray Tracing")
	pygame.init()

	selector = pygame.Surface((500, 500))
	overlay = pygame.Surface((500, 500), pygame.SRCALPHA, 32)
	info = pygame.Surface((500, 100))
	view = pygame.Surface((900, 600))

	pixelSize = 2
	xLand, yLand = 400, 400
	renderer = Renderer(pixelSize, xLand, yLand)
	# renderer.draw(screen)

	generator = Generator(1, selector, renderer)
	generator.start()

	smallFont = pygame.font.SysFont("Bahnschrift", 20)

	x = 0
	y = 0
	height = 0

	viewVec = None

	clock = pygame.time.Clock()
	frameCount = 0
	mouseHold = False
	done = False
	while not done:
		frameCount += 1
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseHold = True

				if renderer.generated and selector.get_rect().collidepoint(mx, my):
					x, y, height = renderer.getInfo(mx/500, my/500)

			if event.type == pygame.MOUSEBUTTONUP:
				mouseHold = False

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					if renderer.generated and not renderer.rendering:
						view.fill([0,0,0])
						renderer.camera = Camera.fromViewVec(Vec3(x, max(height, renderer.waterLevel) + 0.02, y), viewVec)
						renderThread = RenderThread(2, view, renderer)
						renderThread.start()

		if renderer.generated and selector.get_rect().collidepoint(mx, my) and mouseHold:
			vx, vy, _ = renderer.getInfo(mx/500, my/500)
			viewVec = Vec3(vx - x, 0, vy - y)

		screen.fill([0,0,0])
		overlay.fill([255,255,255,0])
		info.fill([170,170,170])

		if viewVec != None:
			pygame.draw.line(overlay, [255,0,0], (x*500/xLand, y*500/yLand), ((x + viewVec.x)*500/xLand, (y + viewVec.z)*500/yLand))

		xLbl = smallFont.render("x: " + str(x), 1, [255,255,255])
		yLbl = smallFont.render("y: " + str(y), 1, [255,255,255])
		heightLbl = smallFont.render("altitude: " + str(int(100*height)/100), 1, [255,255,255])
		if viewVec != None:
			camLbl = smallFont.render(str(viewVec.raw()) + " " + str(renderer.camera.rot.raw()), 1, [255,255,255])

		info.blit(xLbl, (10, 10))
		info.blit(yLbl, (10, 30))
		info.blit(heightLbl, (10, 50))
		if viewVec != None:
			info.blit(camLbl, (10, 70))

		screen.blit(selector, (0, 0))
		screen.blit(overlay, (0, 0))
		screen.blit(info, (0, 500))
		screen.blit(view, (500, 0))

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
