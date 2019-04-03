import pygame
import random
import time
import math

print("This is the Snow Machine. Control the size of the sun using the red slider.")
input("(Press enter to continue)")

clock = pygame.time.Clock()
pygame.init()

BACK = [int(135/2), int(206/2), int(250/2)]
WHITE = [255,255,255]
RED = [255,0,0]
BROWN = [87,59,12]
YELLOW = [255,255,0]
SIZE = [400, 400]

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Snow_Machine")

snow_list = []
alive = []
snowSize = []

sliderPos = 200
sunR = 50-sliderPos/8
mox = 0
moy = 0
mouseHold = False
mouseDrag = False

for i in range(4000):
        x = random.randrange(0, 400)
        y = random.randrange(-400, 400)
        snow_list.append([x, y])
        snowSize.append(2)
        if random.randrange(400) < sliderPos:
            alive.append([0,0]) #1st means currently alive, 2nd means due to be alive
        else:
            alive.append([1,0])

#------------------Main Loop------------------#
done = False
while done == False:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
    
    screen.fill(BACK)
    mox, moy = pygame.mouse.get_pos()
    
    if mouseHold == True and mox <= sliderPos + 5 and mox >= sliderPos - 5 and moy >= 370 and moy <= 380:
        mouseDrag = True

    if mouseHold == True and mouseDrag == True:
        sliderPos = mox
        sunR = 50-sliderPos/8
        BACK = [int(135*(1-sliderPos/400)), int(206*(1-sliderPos/400)), int(250*(1-sliderPos/400))]
    elif mouseHold == False:
        mouseDrag = False

    sun = pygame.draw.circle(screen, YELLOW, (50,100), int(sunR))
    
    for i in range(len(snow_list)):
        if random.randrange(400) < math.pow(sliderPos,2)/math.pow(400,1):
            alive[i][1] = 1
        else:
            alive[i][1] = 0

        if alive[i][0] == 1:
                pygame.draw.circle(screen, WHITE, (snow_list[i][0], round(snow_list[i][1])), int(snowSize[i]))

        snowSize[i] = math.pow(snow_list[i][1]/10+1.5+4*(sliderPos/400),20)/math.pow(40,19)+2
        if snowSize[i] > 20+20*(sliderPos/400):
            snowSize[i] = 20+20*(sliderPos/400)

        if snow_list[i][1] < 351:# - round(sliderPos/10):
            snow_list[i][1] += random.randrange(1,3)
        else:
            snow_list[i][1] += random.randrange(1,3)#5)/10
            #snowSize[i] = 10
            #if alive[i][0] == 1:
                #pygame.draw.polygon(screen, WHITE, [(snow_list[i][0],round(snow_list[i][1])), (0,365), (400,365)])
            

        if snow_list[i][1] > 380:
            y = random.randrange(-410, -50)
            snow_list[i][1] = y
            x = random.randrange(0, 400)
            snow_list[i][0] = x
            #snowSize[i] = 2
        elif snow_list[i][1] < 0:
            alive[i][0] = alive[i][1]
    
    grass = pygame.draw.rect(screen, (0,int(92+74*(1-sliderPos/400)), int(9+8*(1-sliderPos/400))), (0, 360-int(5*(1-sliderPos/400)), 400 ,5+int(5*(1-sliderPos/400))))
    ground = pygame.draw.rect(screen, BROWN, (0, 365, 400 ,45))
    slider = pygame.draw.rect(screen, RED, (sliderPos-5, 370, 10 ,10))
    
    pygame.display.flip()
    clock.tick(60)
 
# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit ()

