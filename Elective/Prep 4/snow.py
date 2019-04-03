import pygame
import random
import time
import math

clock = pygame.time.Clock()
pygame.init()

BLACK = [0,0,0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
xSize = 1280
ySize = 1024
SIZE = [xSize, ySize]

screen = pygame.display.set_mode(SIZE,pygame.FULLSCREEN)
pygame.display.set_caption("Rainbow Snow")

snow_list = []
alive = []

sliderPos = 200

frameCount = 0

for i in range(2000):
    x = random.randrange(0, 1440)
    y = random.randrange(0, 900)
    snow_list.append([x, y])


#------------------Main Loop------------------#
done = False
while done == False:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True
    frameCount += 1
    
    screen.fill(BLACK)
    
    for i in range(len(snow_list)):
        minC = round(255*(math.sin(math.radians((2*frameCount+314*(snow_list[i][0]/2880))/1))+1)/2)
        
        if snow_list[i][1] < 0 or snow_list[i][1] > ySize:
            pygame.draw.circle(screen, WHITE, snow_list[i], 2)
        elif snow_list[i][1] < 180:
            pygame.draw.circle(screen, [255,minC+(255-minC)*snow_list[i][1]/180,minC], snow_list[i], 2)
        elif snow_list[i][1] < 360:
            pygame.draw.circle(screen, [255-(255-minC)*(snow_list[i][1]-180)/180,255,minC], snow_list[i], 2)
        elif snow_list[i][1] < 540:
            pygame.draw.circle(screen, [minC,255,minC+(255-minC)*(snow_list[i][1]-360)/180], snow_list[i], 2)
        elif snow_list[i][1] < 720:
            pygame.draw.circle(screen, [minC,255-(255-minC)*(snow_list[i][1]-540)/180,255], snow_list[i], 2)
        elif snow_list[i][1] < 900:
            pygame.draw.circle(screen, [minC,minC,255-(255-minC)*(snow_list[i][1]-720)/180], snow_list[i], 2)

        snow_list[i][1] += random.randrange(1,3)

        if snow_list[i][1] > 900:
            y = random.randrange(-50, -10)
            snow_list[i][1] = y
            x = random.randrange(0, 1440)
            snow_list[i][0] = x
    
    pygame.display.flip()
    clock.tick(60)
 
# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit ()

