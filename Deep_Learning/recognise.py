import numpy as np
import os
import pygame
import time
from math import sqrt
import net

cwd = os.getcwd()

classes = 10

X = []
y = []

for i in range(classes):
	c = cwd + "\\data\\{0}".format(i)

	try: examples = [line.rstrip('\n') for line in open(c)]
	except:
		print("Warning: no examples for", i)
		print()
		examples = []

	for example in examples:
		example = example.split(" ")
		X.append(example)
		target = [0 for _ in range(classes)]
		target[i] = 1
		y.append(target)

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

X = np.array(X)
y = np.array(y)

X, y = unison_shuffled_copies(X, y)

X = X.T.astype(np.float)
y = y.T.astype(np.float)

X_train = X#[:,:X.shape[1]*4//5]
Y_train = y#[:,:X.shape[1]*4//5]
#training on all data, not testing

X_test = X[:,X.shape[1]*4//5:]
Y_test = y[:,X.shape[1]*4//5:]

num_epochs = 20000 #number of passes through the training set
layers_units = [X.shape[0], 10, y.shape[0]] #layer 0 is the input layer - each value in list = number of nodes in that layer
print("Layer 1:", X.shape[0])
learning_rate = 1e-1 #size of our step

print("No. of training examples:", X_train.shape[1])
print("No. of test examples:", X_test.shape[1])
print()

parameters, train_costs = net.train(X_train, Y_train, num_epochs, layers_units, learning_rate, .1)
# evaluate_model(train_costs, parameters, X_train, Y_train, X_test, Y_test)

xSize, ySize = 600, 450
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Neural Network")
pygame.init()

mouseHold = False

size = 16
scale = 10

content = np.zeros((size,size))

result = [0 for _ in range(classes)]
cache = None
hasTested = False

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
	frameCount += 1
	test = False
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
			if keys[pygame.K_a]:
				test = True
				hasTested = True

			if keys[pygame.K_ESCAPE]:
				content = np.zeros((size,size))
			
	screen.fill([255,255,255])

	for y in range(size):
		for x in range(size):
			if mouseHold:
				dx = x + 1/2 - mx/scale
				dy = y + 1/2 - my/scale
				dist = sqrt(dx**2 + dy**2)

				if abs(dx) < .5 and abs(dy) < .5: content[y][x] = 1

				content[y][x] = max(content[y][x], sqrt(min(1,max(0, 1*(0.8 - abs(dist))))))

			pygame.draw.rect(screen, [content[y][x]*255, content[y][x]*255, content[y][x]*255], (1 + x*scale, 1 + y*scale, scale, scale))

	if test or True:
		X = []
		for y in range(size):
			for x in range(size):
				X.append(content[y][x])
		X = np.reshape(np.array(X).T, (256,1))

		cache = net.forward(X, parameters)
		L = len(parameters)//2

		result = cache['A' + str(L)].T[0]

		# print("Chosen: ", np.argmax(result))

	myfont = pygame.font.SysFont("monospace", 30)

	for i in range(classes):
		label = myfont.render(str(i) + ":", 1, (0,0,0))
		res = myfont.render(str(int(10000*max(0,min(1,result[i])))/100) + "%", 1, (200,20,20) if i == np.argmax(result) else (0,0,0))
		screen.blit(label, (250, 10 + i*35))
		screen.blit(res, (350, 10 + i*35))

	smallfont = pygame.font.SysFont("monospace", 15)

	label1 = smallfont.render("Draw a digit in the black square", 1, (0,0,0))
	label2 = smallfont.render("Press Esc to cancel drawing", 1, (0,0,0))
	label3 = smallfont.render("Please note, the network has been trained on my handwriting", 1, (0,0,0))
	screen.blit(label1, (10, 370))
	screen.blit(label2, (10, 395))
	screen.blit(label3, (10, 420))

	if frameCount > 60*60*3:
		done = True

	pygame.display.flip()
	clock.tick(60)

pygame.quit()