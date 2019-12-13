import pygame
import time
from math import sqrt, sin, cos, tan, asin, atan, pi

mouseHold = False

pixel = 5
fill = 3
coneStart = .7

#	r = cylinder radius
#	x = offset along surface
#	alpha = angle of axis to viewer + 90
#	d = cylinder length / 2
#	angle = view angle

def heightAdjustment(r, h):
	return sqrt(r**2 - h**2)*abs(r)/r

def getOffset(D, r, angle, alpha, h): #same formulae as viewAngle(), but rearranged
	#r = heightAdjustment(r, h)
	return (tan(angle)*(D - r*cos(alpha)) - r*sin(alpha))/(cos(alpha) - sin(alpha)*tan(angle))

def viewAngle(D, r, x, alpha, h):
	r = heightAdjustment(r, h)
	perp_offset = r*sin(alpha) + x*cos(alpha)
	depth = D - r*cos(alpha) + x*sin(alpha)
	return atan(perp_offset/depth)

def angleQuad(D, r, d, alpha, h):
	return (viewAngle(D, -r, -d, alpha, h),
			viewAngle(D, r, -d, alpha, h),
			viewAngle(D, r, d, alpha, h),
			viewAngle(D, -r, d, alpha, h))

def angleTop(D, r, d, alpha, h):
	return (viewAngle(D, r, d*coneStart, alpha, h),
			viewAngle(D, -r, d*coneStart, alpha, h),
			viewAngle(D, -r, -d*coneStart, alpha, h),
			viewAngle(D, r, -d*coneStart, alpha, h))

def toScreen(angle, h, xSize, ySize):
	x = tan(angle)*500/2 + int(xSize)/2
	y = h + ySize/2
	return (int(x),int(y))

def toAngle(pos, xSize, ySize):
	x, y = pos
	return atan((x - xSize/2)*2/500)

end = [
	[.7,.7,.7,.7,.7,.7],
	[.7,.7,.9,.9,.7,.7],
	[.7,.9,.99,.99,.9,.7],
	[.7,.9,.99,.99,.9,.7],
	[.7,.7,.9,.9,.7,.7],
	[.7,.7,.7,.7,.7,.7]]
side = [[.5,.8,.5,.8,.5,.8,.8]]
top = [[.8]]

def getColor(x, r, d, h, colors):
	y = .5*x/d +.5
	try:
		val = 255*colors[int((.5*h/r +.5)*len(colors))][int(y*len(colors[0]))]
	except: return ([], False)

	if colors == end:
		return ([255,val,val*.7], True)
	elif colors == side:
		#print([val,val*(y),val*(y)])
		return ([val,val*abs(y**.3),val*abs(y**.3)], True)
	elif colors == top:
		return ([val,val*abs(y**.3),val*abs(y**.3)], True)
	else:
		return ([val,val,val], True)

def adjustHeight(D, r, x, alpha, h):
	perp_offset = r*sin(alpha) + x*cos(alpha)
	depth = D - r*cos(alpha) + x*sin(alpha)

	dist = sqrt(perp_offset**2 + depth**2)

	return 30*8*h/dist

def drawEnd(D, r, x, d, alpha, h, surf):
	angle = toAngle((x, h), surf.get_size()[0], surf.get_size()[1])
	offset = getOffset(D, d, angle, alpha, h)

	col, success = getColor(offset, r, r, h, end)
	if success:
		pos = toScreen(angle, adjustHeight(D, d, offset, alpha, h), surf.get_size()[0], surf.get_size()[1])
		pygame.draw.rect(surf, col, (pos[0], pos[1], pixel, pixel + fill))

def drawTop(D, r, x, d, alpha, h, surf):
	angle = toAngle((x, h), surf.get_size()[0], surf.get_size()[1])
	offset = getOffset(D, d*coneStart, angle, alpha, h)

	col, success = getColor(d*coneStart, r, abs(d), h, top)
	if success:
		pos = toScreen(angle, adjustHeight(D, d*coneStart, offset, alpha, h), surf.get_size()[0], surf.get_size()[1])
		pygame.draw.rect(surf, col, (pos[0], pos[1], pixel, pixel + fill))

def drawSide(D, r, screenX, d, alpha, h, surf):
	coneWeight = 1

	angle = toAngle((screenX, h), surf.get_size()[0], surf.get_size()[1])
	offset = getOffset(D, heightAdjustment(r, h), angle, alpha, h)

	if offset > d*coneStart:
		coneWeight = (d - offset)/(d*(1 - coneStart))

	if offset < -d*coneStart:
		coneWeight = (-offset)/(d)

	col, success = getColor(offset, r, d, h, side)
	if success:
		pos = toScreen(angle, coneWeight*adjustHeight(D, heightAdjustment(r, h), offset, alpha, h), surf.get_size()[0], surf.get_size()[1])
		pygame.draw.rect(surf, col, (pos[0], pos[1], pixel, pixel + fill))

def draw(alpha, surf, light):
	xSize, ySize = surf.get_size()

	r = 30
	D = r*8# + r*sin(frameCount/100)
	d = r*3

	for h in range(-r, r, pixel):

		t1,t2,t3,t4 = angleTop(D, r, d, alpha, h)
		top1 = toScreen(t1, h, xSize, ySize)
		top2 = toScreen(t2, h, xSize, ySize)
		top3 = toScreen(t3, h, xSize, ySize)
		top4 = toScreen(t4, h, xSize, ySize)

		for x in range(top3[0], top4[0], pixel):
			drawTop(D, r, x, -d, alpha + pi/2, h, surf)

		for x in range(top1[0], top2[0], pixel):
			drawTop(D, r, x, d, alpha + pi/2, h, surf)

	# 	pos1 = toScreen(a1, h)
	# 	pos2 = toScreen(a2, h)
	# 	pos3 = toScreen(a3, h)
	# 	pos4 = toScreen(a4, h)

	# 	t1,t2 = angleTop(D, r, d, alpha, h)
	# 	top1 = toScreen(t1, h)
	# 	top2 = toScreen(t2, h)

	# 	for x in range(pos3[0], pos2[0], pixel):
	# 		drawSide(D, r, x, d, alpha, h, surf)

	# 	for x in range(pos1[0], pos4[0], pixel):
	# 		drawSide(D, -r, x, d, alpha, h, surf)

	for h in range(-r, r, pixel):
		a1,a2,a3,a4 = angleQuad(D, r, d, alpha, h)

		xSize = surf.get_size()[0]
		ySize = surf.get_size()[1]

		pos1 = toScreen(a1, h, xSize, ySize)
		pos2 = toScreen(a2, h, xSize, ySize)
		pos3 = toScreen(a3, h, xSize, ySize)
		pos4 = toScreen(a4, h, xSize, ySize)

		for x in range(pos2[0], pos3[0], pixel):
			drawSide(D, r, x, d, alpha, h, surf)

		for x in range(pos4[0], pos1[0], pixel):
			drawSide(D, -r, x, d, alpha, h, surf)

		for x in range(pos1[0], pos2[0], pixel):
			drawEnd(D, r, x, d, alpha - pi/2, h, surf)

#----------------------Main Loop----------------------#
if __name__ == "__main__":
	xSize, ySize = 600, 450
	screen = pygame.display.set_mode((xSize, ySize))
	pygame.display.set_caption("Pygame Template")

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

		alpha = mx/100 #(frameCount/60)%(2*pi) #sin(frameCount/60)*pi/2.5
		
		draw(alpha, screen, 0)

		#done = True
		pygame.display.flip()
		clock.tick(60)

pygame.quit()
