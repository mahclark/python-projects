import pygame
import os
import time
import math
import random
from random import randint
import sys
from ctypes import windll

def roll_text(string):
    text = ''
    for i in range(len(string)):
        print(string[i], end='', flush=True)
        time.sleep(0.04)

os.system('mode con: cols=70 lines=50')

dir_path = os.path.dirname(os.path.realpath(__file__))

if 'idlelib.run' in sys.modules:
    print("Run in CMD for optimised experience.")
    print("")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)

for i in range(31):
    if i < 10:
        pygame.image.load(dir_path + "/Game Files/Images/Hitler/Boss/hitler_boss_0{0}.bmp".format(i))
    elif i >= 10:
        pygame.image.load(dir_path + "/Game Files/Images/Hitler/Boss/hitler_boss_{0}.bmp".format(i))

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

setWindowPos = windll.user32.SetWindowPos
setWindowPos(pygame.display.get_wm_info()['window'], -1, 400, 300, 0, 0, 0x0001)

#Screen
infoObject = pygame.display.Info()
scrW, scrH = infoObject.current_w, infoObject.current_h
xShift = scrW/2 - 300
yShift = scrH/2 - 300
xSize, ySize = scrW, scrH#600, 600
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Mission_")

try:
    shotgun_reload = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/shotgun_reload.wav"))
    shotgun_blast = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/shotgun_blast.wav"))
except:
    print("can't load sound")

xOffset = []

backgSizex = 1000
backgSizey = 50
backg = pygame.image.load(dir_path + "/Game Files/Images/grass.bmp")
backg = pygame.transform.scale(backg, (backgSizex, backgSizey))
for y in range(50):
    xOffset.append(randint(0,backgSizex))
for y in range(0, int(ySize/backgSizey) + 1):
        for x in range(0, int(xSize/backgSizex + 1)):
            screen.blit(backg,(x*backgSizex,y*backgSizey))

mx, my = pygame.mouse.get_pos()
pygame.mouse.set_visible(False)
mouseHold = False
clicked = False
clickFrame = 0
firstDone = False
soundStart = False
openFrame = 0
gifC = 0
px, py = pygame.mouse.get_pos()
swing = False
sFrame = 0
cFrame = 0

#----------------------Main Loop----------------------#

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
            if not clicked and firstDone:
                clicked = True
                clickFrame = frameCount

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False

    

    mx, my = pygame.mouse.get_pos()
    if mx - px > 200 and mouseHold and not swing:
        swing = True
        sFrame = frameCount

    px, py = mx, my
            
    screen.fill([150,200,255])

    for y in range(0, int(ySize/backgSizey) + 1):
        for x in range(0, int(xSize/backgSizex + 2)):
            screen.blit(backg,(x*backgSizex - xOffset[y],y*backgSizey + ySize/2+150))

    if not clicked:
        gifC = int(frameCount/10 - 10)
        if gifC > 16:
            gifC = 16
            firstDone = True
            
    elif mouseHold:
        if not swing:
            if gifC < 19:
                gifC += .2
                if gifC > 19:
                    gifC = 19
            elif gifC > 19:
                gifC -= .2
                if gifC < 19:
                    gifC = 19


    elif not mouseHold and not swing:
        gifC += 1
        if gifC > 21:
            gifC = 21

    if swing == True:
        if gifC < 23:
            gifC = 23
        elif gifC <= 30:
            gifC += .2
        elif 31 > gifC > 30:
            gifC += .01
        else:
            gifC += .1
                
    if gifC > 34:
        gifC = 34

    if gifC < 0:
        img = pygame.image.load(dir_path + "/Game Files/Images/Hitler/Boss/hitler_boss_0{0}.bmp".format(0))
    elif 10 > gifC >= 0:
        img = pygame.image.load(dir_path + "/Game Files/Images/Hitler/Boss/hitler_boss_0{0}.bmp".format(int(gifC)))
    elif gifC >= 10:
        img = pygame.image.load(dir_path + "/Game Files/Images/Hitler/Boss/hitler_boss_{0}.bmp".format(int(gifC)))
    img = pygame.transform.scale(img, (384,600))
    screen.blit(img,(xShift+600-384, yShift))

    if sFrame + 250 < frameCount and swing == True:
        done = True

    #Back
    pygame.draw.rect(screen, [1,1,2], [0,0, xSize, yShift])
    pygame.draw.rect(screen, [1,1,2], [0,0, xShift, ySize])
    pygame.draw.rect(screen, [1,1,2], [xSize-xShift,0, xShift, ySize])
    pygame.draw.rect(screen, [1,1,2], [0,ySize-yShift, xSize, yShift])

    myFont = pygame.font.SysFont("dotum", 40)
    label = myFont.render("Click to stab", 1, (255,255,255))
    if frameCount > 500 and not clicked:
        screen.blit(label, (xShift,yShift-30))

    label = myFont.render("Click and swipe right to finish", 1, (255,255,255))
    if frameCount > 300 + clickFrame and clicked and not swing:
        screen.blit(label, (xShift,yShift-30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("")
os.system('cls')
time.sleep(2)
roll_text("by Max Clark")
time.sleep(2)
print("")
print("")
roll_text("Thank you for playing.")
input("")
