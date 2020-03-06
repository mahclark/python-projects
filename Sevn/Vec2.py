from math import sqrt

class Vec2():

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

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

	def avg(self, vec):
		return self.addVec(vec).mult(0.5)

	def toPair(self):
		return (self.x, self.y)

	def toInts(self):
		return (int(self.x), int(self.y))

	def average(vecs):
		return Vec2(sum([vec.x for vec in vecs])/len(vecs), sum([vec.y for vec in vecs])/len(vecs))