import pygame
import time
import os
from random import randint

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 600, 400
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Neural Network Jump")

#[223,484,153,146]
memory = [randint(100,700),randint(100,700),randint(0,300),randint(0,300)]
best = memory

def aneuron(a): #Senses Distance
    if a < al: return 1
    else: return 0
def bneuron(b): #Senses Distance
    if b < bl: return 1
    else: return 0
def cneuron(c): #Senses Speed
    if cl < c and c < cl + 100:
        return 1
    else: return 0
def dneuron(d): #Senses Speed
    if dl < d and d < dl + 100:
        return 1
    else: return 0

def neuron(a,b,c,d):  #Causes Jump
    if a + b + c + d > 1: #Fires if two or more signals received
        return 1
    else:
        return 0

#----------------------Main Loop----------------------#

moving = False
jump = False
fail = False
jumped = False
px = xSize + 25
py = 300
vv = 5
speed = 50#randint(50,200)
count = 0
best_count = 0
zero_count = 0

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([255,255,255])

    al,bl,cl,dl = memory #Setting limits

    if not moving and not jump: #Starts moving obstacle
        if randint(0,20) == 1:
            moving = True
            px = xSize + 200

    #Firing neurons
    asig = aneuron(abs(px - 100))
    bsig = bneuron(abs(px - 100))
    csig = cneuron(speed)
    dsig = dneuron(speed)

    if neuron(asig,bsig,csig,dsig) == 1 and not jump and not jumped and moving:
        jump = True
        jumped = True
    
    if moving:
        px -= speed/10 #Moves obstacle
        if px <= -50: #Resets Obstacle
            moving = False
            if fail: #Resets memory
                print(count)
                if count == 0: zero_count += 1
                else: zero_count = 0
                if zero_count < 5: #Mutates from best memory
                    if best_count <= count:
                        best_count = count
                        best = memory
                    weighting = best_count/(best_count + 2)
                    memory = [randint(100,700)*(1-weighting) + best[0]*weighting, randint(100,700)*(1-weighting) + best[1]*weighting, randint(0,300)*(1-weighting) + best[2]*weighting, randint(0,300)*(1-weighting) + best[3]*weighting]
                else: #Creats completely new memory
                    print("reset")
                    memory = [randint(100,700),randint(100,700),randint(0,300),randint(0,300)]
                    
                count = 0
            else:
                count += 1 #Number of consequetive successful jumps
                
            fail = False
            speed = randint(50,200)
            jumped = False

    if jump: #Performs jump
        py -= vv
        vv -= 0.15
        if py >= 300:
            jump = False
            py = 300
            vv = 5

    if 50 <= px and px <= 150 and py > 250: #Detects collision
        fail = True

    pygame.draw.rect(screen,[0,0,255],(100,py,50,50))
    pygame.draw.rect(screen,[255,0,0],(px,300,50,50))
    pygame.draw.line(screen,[0,0,0],(0,350),(xSize,350))

    font = pygame.font.SysFont("twcen", 25)
    txt1 = str(asig) + str(bsig) + str(csig) + str(dsig)
    txt2 = str([int(i) for i in memory])
    txt3 = str(speed)
    lbl1 = font.render(txt1, 1, [0,0,0])
    lbl2 = font.render(txt2, 1, [0,0,0])
    lbl3 = font.render(txt3, 1, [0,0,0])
    screen.blit(lbl1,(10,ySize - 30))
    screen.blit(lbl2,(100,ySize - 30))
    screen.blit(lbl3,(xSize - 45,ySize - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
