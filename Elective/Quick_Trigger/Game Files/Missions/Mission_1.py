import pygame
import os
import inspect
import time
import math
import random
from random import randint
import sys
from ctypes import windll

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

lockSave = "1" + chp2 + chp3

tsaved = lockSave.encode(encoding='UTF-8')
newFile = open(dir_path + "/Game Files/Saves/lock.txt", "wb")
newFile.write(tsaved)
newFile = open(dir_path + "/Game Files/Saves/lock.txt", "rb")


if chp1 == "0":
    saved = "1"
    bsaved = saved.encode(encoding='UTF-8')
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "wb")
    newFile.write(bsaved)
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")
    
else:
    ans = input("Would you like to skip brief? (y or n): ")
    print("")
    if ans.lower() == "y":
        saved = "0"
    else:
        saved = "1"
    bsaved = saved.encode(encoding='UTF-8')
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "wb")
    newFile.write(bsaved)
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")

try:
    skipFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")
    binRead = skipFile.read().decode(encoding='UTF-8')
except:
    binRead = "1"


def roll_text(string):
    text = ''
    for i in range(len(string)):
        print(string[i], end='', flush=True)
        time.sleep(0.04)
        
def set_gifC(gifC):
    if gifC <= 40:
        return 1
    else:
        return gifC-39

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)

BLACK    = (   0,   0,   0) ; WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0) ; RED      = ( 255,   0,   0)

pygame.mixer.pre_init(44100, -16, 1, 2048)
pygame.init()

if binRead == "1":
    time.sleep(1)
    roll_text("Loading brief")
    time.sleep(0.5)
    print(".",end='', flush=True)
    time.sleep(0.5)
    print(".",end='', flush=True)
    time.sleep(0.5)
    print(".")
    time.sleep(3)
    roll_text("Brief loaded.")
    time.sleep(1)
    roll_text(" (Press enter to open brief)")
    input("")
    print("")
    print("")
    print("-----------------------------Brief Opened-----------------------------")
    time.sleep(1)
    roll_text("Agent 47")
    time.sleep(1)
    print("")
    print("")
    roll_text("Mission 1")
    time.sleep(1)
    print("")
    print("")
    roll_text("Your mission is to get to the vantage point.")
    time.sleep(1)
    roll_text(" Execute all guards in")
    print("")
    roll_text("your way.")
    time.sleep(1)
    roll_text(" You will recieve your next brief when you reach the security access point.")
    time.sleep(1)
else:
    roll_text("Brief skipped.")

roll_text(" (Press enter when ready)")
input("")
print("")


SetWindowPos = windll.user32.SetWindowPos
SetWindowPos(pygame.display.get_wm_info()['window'], -1, 400, 300, 0, 0, 0x0001)

#Screen
infoObject = pygame.display.Info()
scrW, scrH = infoObject.current_w, infoObject.current_h
xShift = scrW/2 - 300
yShift = scrH/2 - 225
xSize, ySize = scrW, scrH#600, 450
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Mission_1")

pygame.mouse.set_visible(True)

if randint(0,1) == 0:
    g1x = xShift-300
    g2x = xShift-450
else:
    g1x = xSize-xShift+450
    g2x = xSize-xShift+300
g1d = False
g2d = False
gVel = 40
shot = False
alerted = False
dead = False
firstFired = False
moveFreq = 40
curg1 = 0
curg2 = 0
already_g1d = False
already_g2d = False
g2df = False

try:
    pistol = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/pistol.wav"))
    silenced = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/silenced_pistol.wav"))
    footstep = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/footstep.wav"))
except:
    print("can't load sound")

mx, my = pygame.mouse.get_pos()
mouseHold = False

#----------------------Initial Loop----------------------#

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            done = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([0,0,0])
    myFont = pygame.font.SysFont("dotum", 40)
    label = myFont.render("Please Click", 1, (255,255,255))
    screen.blit(label, (0,0))
    
    pygame.display.flip()

pygame.mouse.set_visible(False)
done = False
clock = pygame.time.Clock()
frameCount = 0

#----------------------Main Loop----------------------#

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if dead == False:
                mouseHold = True
                shot = True
                silenced.play()

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([150,150,150])
    frameCount += 1
    mx, my = pygame.mouse.get_pos()

    wdif = 0
    
    #Back Walls
    backWall = pygame.draw.rect(screen, [10,42,150], [xShift,yShift+100,600,250])
    for i in range(10):
        pygame.draw.rect(screen, [10,42,120], [xShift+20+wdif,yShift+100,6,250])
        wdif += 60
    wdif = 0
    for i in range(8):
        pygame.draw.rect(screen, [10,42,120], [xShift,yShift+120+wdif,600,6])
        wdif += 30

    if frameCount % moveFreq == 0:
        if g1d == False:
            g1x += gVel
        if g2d == False:
            g2x += gVel

        if gVel != 0 and not (g1d and g2d):
            footstep.play()
        
        #Select gif image
        if curg1 < 3:
            curg1 += 1
        else:
            curg1 = 0
        if curg2 < 3:
            curg2 += 1
        else:
            curg2 = 0
            
        if gVel == 0 and randint(0,3) == 1 and g1d == False:
            curg1 = 1
            firstFired = True
            pistol.play()
        elif gVel == 0:
            curg1 = 0
        if gVel == 0 and randint(0,3) == 1 and g2d == False:
            curg2 = 1
            firstFired = True
            pistol.play()
        elif gVel == 0:
            curg2 = 0

        if g1d == True and already_g1d == False:
            curg1 = 0
            already_g1d = True
        elif g1d == True:
            curg1 = 1
        if g2d == True and already_g2d == False:
            curg2 = 0
            already_g2d = True
        elif g2d == True:
            curg2 = 1

    #Make guards
    if g1d == True and curg1 <= 1 and not (curg1 == 1 and already_g1d == False):
        guard1 = pygame.image.load(dir_path + "/Game Files/Images/Guard/guard_d{0}.bmp".format(curg1))
    elif gVel != 0 or curg1 > 1:
        guard1 = pygame.image.load(dir_path + "/Game Files/Images/Guard/guard_{0}.bmp".format(curg1))
    else:
        guard1 = pygame.image.load(dir_path + "/Game Files/Images/Guard/guard_s{0}.bmp".format(curg1))
    guard1 = pygame.transform.scale(guard1, (250,250))
    if gVel > 0:
        guard1 = pygame.transform.flip(guard1, True, False)
    
    if g2d == True and curg2 <= 1 and not (curg2 == 1 and already_g2d == False):
        guard2 = pygame.image.load(dir_path + "/Game Files/Images/Guard/guard_d{0}.bmp".format(curg2))
    elif gVel != 0 or curg2 > 1:
        guard2 = pygame.image.load(dir_path + "/Game Files/Images/Guard/guard_{0}.bmp".format(curg2))
    else:
        guard2 = pygame.image.load(dir_path + "/Game Files/Images/Guard/guard_s{0}.bmp".format(curg2))
    guard2 = pygame.transform.scale(guard2, (250,250))
    if gVel > 0:
        guard2 = pygame.transform.flip(guard2, True, False)

    if g2df:
        screen.blit(guard2, (g2x, yShift+130))
        screen.blit(guard1, (g1x, yShift+130))
    else:
        screen.blit(guard1, (g1x, yShift+130))
        screen.blit(guard2, (g2x, yShift+130))
    
    if g2x > xShift+600:
        gVel = -40
    elif g1x < xShift-250:
        gVel = 40
    
    #Side Walls
    leftWall = pygame.draw.polygon(screen, [5,21,75], [(xShift,yShift),(xShift+100,yShift+50),(xShift+100,yShift+400),(xShift,yShift+450)])
    rightWall = pygame.draw.polygon(screen, [5,21,75], [(xShift+600,yShift),(xShift+500,yShift+50),(xShift+500,yShift+400),(xShift+600,yShift+450)])

    pygame.draw.rect(screen, [1,1,2], [0,0, xSize, yShift])
    pygame.draw.rect(screen, [1,1,2], [0,0, xShift, ySize])
    pygame.draw.rect(screen, [1,1,2], [xSize-xShift,0, xShift, ySize])
    pygame.draw.rect(screen, [1,1,2], [0,ySize-yShift, xSize, yShift])

    missColors = [(10,42,150,255), (10,42,120,255), (5,21,75,255), (150,150,150,255), (1,1,2,255)]
    
    if shot == True and dead == False:
        shotc = screen.get_at((mx, my))
        if g1d == False and g1x + 45 < mx < g1x + 190 and shotc not in missColors:
            g1d = True
        elif g2d == False and g2x + 45 < mx < g2x + 190 and shotc not in missColors:
            g2d = True
        if g2d and not g1d:
            g2df = True
        alerted = True
        alertFrame = frameCount
        killFrame = frameCount

    if alerted == True:
        moveFreq = 10
        if g2x < xShift+10 and g1x < xShift+160:
            gVel = 40
        elif g1x > xShift+350 and g2x > xShift+200:
            gVel = -40
        else:
            gVel = 0
        if not (g1d and g2d) and firstFired == True:
            dead = True
            killFrame = frameCount
            alerted = False
        elif frameCount - alertFrame > 100 and g1d and g2d:
            done = True
    
    if dead == True:
        blood = pygame.Surface((xSize,ySize))
        blood.set_alpha(frameCount-killFrame)
        blood.fill((210,20,20))
        screen.blit(blood, (0,0))
        if frameCount-killFrame > 300:
            done = True

    #Crosshair
    if dead == False:        
        pygame.draw.line(screen, [0,0,0], (mx-10,my),(mx+10,my), 1)
        pygame.draw.line(screen, [0,0,0], (mx,my-10),(mx,my+10), 1)
        pygame.draw.rect(screen, [0,0,0], [mx-2,my-2,5,5])
        pygame.draw.rect(screen, [255,255,255], [mx-1,my-1,3,3])

    shot = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

if dead == True:
    roll_text("You died.")
    time.sleep(1)
    roll_text(" Mission failed.")
    time.sleep(1)
    print("")
    print("")
    if binRead == "1":
        print("-----------------------------Brief Closed-----------------------------")
    time.sleep(3)
else:
    roll_text("Mission complete.")
    time.sleep(1)
    print("")
    print("")
    if binRead == "1":
        print("-----------------------------Brief Closed-----------------------------")
    print("")
    roll_text("(Press enter to load next brief)")
    input("")
    exec(open(dir_path + "/Game Files/Missions/Puzzle_1.py").read(), globals())
