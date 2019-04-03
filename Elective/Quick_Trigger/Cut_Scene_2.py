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

for i in range(35):
    if i < 10:
        pygame.image.load(dir_path + "/Game Files/Images/Devil/devil_death_0{0}.bmp".format(i))
    elif i >= 10:
        pygame.image.load(dir_path + "/Game Files/Images/Devil/devil_death_{0}.bmp".format(i))

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
                shotgun_blast.play()

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([150,200,255])

    for y in range(0, int(ySize/backgSizey) + 1):
        for x in range(0, int(xSize/backgSizex + 2)):
            screen.blit(backg,(x*backgSizex - xOffset[y],y*backgSizey + ySize/2+100))

    if not clicked:
        gifC = int(frameCount/10 - 10)
    else:
        gifC = int((frameCount - clickFrame)/8 + 12)
        
    if gifC > 34:
        gifC = 34

    if gifC < 0:
        img = pygame.image.load(dir_path + "/Game Files/Images/Devil/devil_death_0{0}.bmp".format(0))
    elif gifC <= 9:
        if soundStart == False:
            shotgun_reload.play()
            soundStart = True
        img = pygame.image.load(dir_path + "/Game Files/Images/Devil/devil_death_0{0}.bmp".format(gifC))
        if gifC > 5:  
            firstDone = True
    elif gifC <= 12:
        img = pygame.image.load(dir_path + "/Game Files/Images/Devil/devil_death_{0}.bmp".format(gifC))
    elif clicked == False:
        img = pygame.image.load(dir_path + "/Game Files/Images/Devil/devil_death_{0}.bmp".format(12))
    else:
        img = pygame.image.load(dir_path + "/Game Files/Images/Devil/devil_death_{0}.bmp".format(gifC))
    img = pygame.transform.scale(img, (600,600))
    screen.blit(img,(xShift, yShift))

    if clicked and frameCount - clickFrame > 200:
        done = True

    #Back
    pygame.draw.rect(screen, [1,1,2], [0,0, xSize, yShift])
    pygame.draw.rect(screen, [1,1,2], [0,0, xShift, ySize])
    pygame.draw.rect(screen, [1,1,2], [xSize-xShift,0, xShift, ySize])
    pygame.draw.rect(screen, [1,1,2], [0,ySize-yShift, xSize, yShift])

    myFont = pygame.font.SysFont("dotum", 40)
    label = myFont.render("Click to shoot", 1, (255,255,255))
    if frameCount > 500 and not clicked:
        screen.blit(label, (xShift,yShift-30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exec(open(dir_path + "/Game Files/Missions/Cut_Scene_3.py").read(), globals())
