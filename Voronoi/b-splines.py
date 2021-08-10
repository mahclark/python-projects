import pygame
import numpy as np

knot = [0,1,2,3,3,3]
k = 3

def N(i,k,t):
	if k == 1:
		if knot[i] <= t and t < knot[i+1]:
			return 1
		else:
			return 0

	result = 0
	
	left = N(i,k-1,t)
	if left != 0:
		result += left*(t - knot[i])/(knot[i + k - 1] - knot[i])

	right = N(i+1,k-1,t)
	if right != 0:
		result += right*(knot[i + k] - t)/(knot[i + k] - knot[i + 1])

	return result

def P(t, points):
	x, y = 0, 0
	for i in range(len(points)):
		n = N(i, k, t)
		x += n*points[i][0]
		y += n*points[i][1]

	return (x, y)

def draw(points, surf):
	prev = None
	for t in np.linspace(knot[0], knot[-1], 100)[:-1]:
		p = P(t, points)
		p = (t, N(0,3,t))
		if prev != None:
			pygame.draw.line(surf, [0,0,0], conv(prev, surf.get_size()), conv(p, surf.get_size()))
		prev = p

def conv(p, size):
	x, y = p
	return (int(size[0]/2 + x*40), int(size[1]/2 - y*40))

if __name__ == "__main__":
	xSize, ySize = 500, 500
	screen = pygame.display.set_mode((xSize, ySize))
	pygame.display.set_caption("B-Splines")
	pygame.init()

	points = [(0,0), (4,0), (4,4)]
	surf = pygame.Surface((500,500))
	surf.fill([255,255,255])
	draw(points, surf)

	clock = pygame.time.Clock()
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
	
				
		screen.fill([255,255,255])

		screen.blit(surf, (0,0))

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()