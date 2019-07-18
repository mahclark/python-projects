import pygame
import time
import numpy as np
from math import sqrt
import os

cwd = os.getcwd()

xSize, ySize = 600, 450
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Make Data")
pygame.init()

mouseHold = False

size = 16
scale = 10

content = np.zeros((size,size))

num = 0

def count():
	s = ""
	for i in range(10):
		c = cwd + "\\data\\{0}".format(i)

		try: examples = [line.rstrip('\n') for line in open(c)]
		except: examples = []

		s += str(len(examples)) + "\t"
	print(s)

count()

def save(content):
	with open(cwd + "\\data\\{0}".format(num), "a") as myfile:
		s = ""
		for y in range(size):
			for x in range(size):
				s += str(content[y][x]) + " "
			# s = s[:-1] + ","
		s = s[:-1] + "\n"

		myfile.write(s)

	count()

	return np.zeros((size,size))

saved = False

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

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False

        if event.type == pygame.KEYUP:
        	if keys[pygame.K_s]:
        		content = save(content)
        		saved = True

        	if keys[pygame.K_ESCAPE]:
        		content = np.zeros((size,size))
        		saved = False

        	if keys[pygame.K_1]:
        		num = 1
        	if keys[pygame.K_2]:
        		num = 2
        	if keys[pygame.K_3]:
        		num = 3
        	if keys[pygame.K_4]:
        		num = 4
        	if keys[pygame.K_5]:
        		num = 5
        	if keys[pygame.K_6]:
        		num = 6
        	if keys[pygame.K_7]:
        		num = 7
        	if keys[pygame.K_8]:
        		num = 8
        	if keys[pygame.K_9]:
        		num = 9
        	if keys[pygame.K_0]:
        		num = 0
            
    screen.fill([255,255,255])

    myfont = pygame.font.SysFont("monospace", 30)
    label = myfont.render(str(num), 1, (0,0,0))
    screen.blit(label, (300, 20))

    if saved:
    	pygame.draw.rect(screen, [0,255,0], (200,20,50,50))
    else:
    	pygame.draw.rect(screen, [255,0,0], (200,20,50,50))

    for y in range(size):
    	for x in range(size):
    		if mouseHold:
    			dx = x + 1/2 - mx/scale
    			dy = y + 1/2 - my/scale
    			dist = sqrt(dx**2 + dy**2)

    			if abs(dx) < .5 and abs(dy) < .5: content[y][x] = 1

    			content[y][x] = max(content[y][x], sqrt(min(1,max(0, 1*(0.8 - abs(dist))))))

    		pygame.draw.rect(screen, [content[y][x]*255, content[y][x]*255, content[y][x]*255], (1 + x*scale, 1 + y*scale, scale, scale))

    # pygame.draw.rect(screen, [0,0,0], (0,0,size*scale + 2,size*scale + 2), 1)

    # if frameCount > 60*20:
    # 	done = True

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
