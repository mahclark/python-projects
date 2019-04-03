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
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_ESCAPE]:
                print("pressed")
        print(string[i], end='', flush=True)
        time.sleep(0.04)

os.system('mode con: cols=70 lines=50')

dir_path = os.path.dirname(os.path.realpath(__file__))

if 'idlelib.run' in sys.modules:
    print("Run in CMD for optimised experience.")
    print("")

try:
    lockFile = open(dir_path + "/Game Files/Saves/lock.txt", "rb")
    txtRead = lockFile.read().decode(encoding='UTF-8')
except:
    txtRead = "failed"

chp1 = txtRead[0]
chp2 = txtRead[1]
chp3 = txtRead[2]

lockSave = chp1 + chp2 + "1"

tsaved = lockSave.encode(encoding='UTF-8')
newFile = open(dir_path + "/Game Files/Saves/lock.txt", "wb")
newFile.write(tsaved)
newFile = open(dir_path + "/Game Files/Saves/lock.txt", "rb")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)

pygame.mixer.pre_init(22050, -16, 2, 4096)
pygame.init()

setWindowPos = windll.user32.SetWindowPos
setWindowPos(pygame.display.get_wm_info()['window'], -1, 400, 300, 0, 0, 0x0001)

FLESH = (255, 217, 179)

try:
    wind = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/wind.wav"))
except:
    print("can't load sound")

#Screen
infoObject = pygame.display.Info()
scrW, scrH = infoObject.current_w, infoObject.current_h
xShift = scrW/2 - 300
yShift = scrH/2 - 225
xSize, ySize = scrW, scrH#600, 450
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Mission_")

xOffset = []

backgSizex = 1000
backgSizey = 1000
backg = pygame.image.load(dir_path + "/Game Files/Images/grass.bmp")
backg = pygame.transform.scale(backg, (backgSizex, backgSizey))
for y in range(50):
    xOffset.append(randint(0,backgSizex))
for y in range(0, int(ySize/backgSizey) + 1):
        for x in range(0, int(xSize/backgSizex + 1)):
            screen.blit(backg,(x*backgSizex,y*backgSizey))

mx, my = pygame.mouse.get_pos()
mouseHold = False
skyy = 0
angled = False
angledFrame = 0
groundLevel = False

#----------------------Main Loop----------------------#

pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    #pygame.mixer.Sound.set_volume(wind, 0.4)
    #if angled != True or backgSizey < 50:
        #wind.play()
    frameCount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([150,200,255])
    
    #Background
    if backgSizey > 200:
        skyy = frameCount/2
        pygame.draw.circle(screen, (255,255,0), (60,int(220-backgSizey/2)),80)
    elif skyy > 300:
        skyy = 1200 - frameCount
        angled = True
        angledFrame = frameCount
        pygame.draw.circle(screen, (255,255,0), (60,120),80)
    else:
        pygame.draw.circle(screen, (255,255,0), (60,120),80)

    if backgSizey > 100:
        backgSizey = int(1000 - frameCount)
        backg = pygame.image.load(dir_path + "/Game Files/Images/grass.bmp")
        backg = pygame.transform.scale(backg, (backgSizex, backgSizey))
        
    for y in range(0, int(ySize/backgSizey) + 1):
        for x in range(0, int(xSize/backgSizex + 2)):
            screen.blit(backg,(x*backgSizex - xOffset[y],y*backgSizey + skyy))

    if angled == True:
        if backgSizey > 50:
            pygame.mixer.fadeout(2000)
            backgSizey -= 1
            backg = pygame.image.load(dir_path + "/Game Files/Images/grass.bmp")
            backg = pygame.transform.scale(backg, (backgSizex, backgSizey))
            person = pygame.image.load(dir_path + "/Game Files/Images/Guy/behind_0.bmp")
            person = pygame.transform.scale(person, (500,500))
            screen.blit(person, (70, ySize + 100 - (frameCount - angledFrame)*12))
        else:
            groundLevel = True

    if groundLevel == True:
        person = pygame.image.load(dir_path + "/Game Files/Images/Guy/behind_0.bmp")
        person = pygame.transform.scale(person, (500,500))
        screen.blit(person, (70, ySize + 100 - 50*12))
            
    if frameCount > 1000:
        gifC = int((frameCount - 1000)/10)
        if gifC < 8:
            hell = pygame.image.load(dir_path + "/Game Files/Images/Hell/hell_{0}.bmp".format(gifC))
        hell = pygame.transform.scale(hell, (500, 200))
        screen.blit(hell, (xSize/2, ySize/2))

    if frameCount > 1150:
        devil = pygame.image.load(dir_path + "/Game Files/Images/Devil/devil_death_00.bmp")
        devil = pygame.transform.scale(devil, (128, 128))
        if (frameCount - 1150)/2 <= 128:
            devil = pygame.transform.chop(devil, (0, int((frameCount - 1150)/2), 0, 128-int((frameCount - 1150)/2)))
            screen.blit(devil, (xSize/2 + 250, ySize/2 + 114 - int((frameCount - 1150)/2)))
        else:
            screen.blit(devil, (xSize/2 + 250, ySize/2 - 14))

    if frameCount > 1500:
        hitler = pygame.image.load(dir_path + "/Game Files/Images/Hitler/Boss/hitler_boss_00.bmp")
        hitler = pygame.transform.scale(hitler, (128, 200))
        if (frameCount - 1500)/2 <= 100:
            hitler = pygame.transform.chop(hitler, (0, int((frameCount - 1500)/2), 0, 200-int((frameCount - 1500)/2)))
            screen.blit(hitler, (xSize/2 + 120, ySize/2 + 114 - int((frameCount - 1500)/2)))
        else:
            hitler = pygame.transform.chop(hitler, (0, 100, 0, 100))
            screen.blit(hitler, (xSize/2 + 120, ySize/2 + 14))
        
    if frameCount > 1850:
        done = True

    #Light
    dark = int(170 - frameCount/5)
    if dark < 0:
        dark = 0

    s = pygame.Surface((xSize,ySize))
    s.set_alpha(dark)
    s.fill((0,0,0))
    screen.blit(s, (0,0))

    if angled == True:
        if backgSizey > 50:
            person = pygame.image.load(dir_path + "/Game Files/Images/Guy/behind_0.bmp")
            person = pygame.transform.scale(person, (500,500))
            screen.blit(person, (70, ySize + 100 - (frameCount - angledFrame)*12))
        else:
            groundLevel = True

    if groundLevel == True:
        person = pygame.image.load(dir_path + "/Game Files/Images/Guy/behind_0.bmp")
        person = pygame.transform.scale(person, (500,500))
        screen.blit(person, (70, ySize + 100 - 50*12))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

exec(open(dir_path + "/Game Files/Missions/Cut_Scene_2.py").read(), globals())
