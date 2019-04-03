import pygame
import os
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
    lockFile = open(dir_path + "/Game Files/Saves/been.txt", "rb")
    txtRead = lockFile.read().decode(encoding='UTF-8')
except:
    txtRead = "failed"

chp1 = txtRead[0]
chp2 = txtRead[1]
chp3 = txtRead[2]

lockSave = "1" + chp2 + chp3

tsaved = lockSave.encode(encoding='UTF-8')
newFile = open(dir_path + "/Game Files/Saves/been.txt", "wb")
newFile.write(tsaved)
newFile = open(dir_path + "/Game Files/Saves/been.txt", "rb")


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
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")
    binRead = newFile.read().decode(encoding='UTF-8')
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

if binRead == "1":
    time.sleep(1)
    if 'idlelib.run' in sys.modules:
        print("")
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
    roll_text("Mission 2")
    time.sleep(1)
    print("")
    print("")
    roll_text("Your mission is to eliminate Hitler. ")
    time.sleep(1)
    roll_text("Execute him at all costs; do not let him escape. ")
    time.sleep(1)
    roll_text("Watch out for window frames. ")
    time.sleep(1)
else:
    roll_text("Brief skipped.")
    
roll_text(" (Press enter when ready)")
input("")
print("")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)

BLACK    = (   0,   0,   0) ; WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0) ; RED      = ( 255,   0,   0)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
SetWindowPos = windll.user32.SetWindowPos
SetWindowPos(pygame.display.get_wm_info()['window'], -1, 400, 300, 0, 0, 0x0001)

infoObject = pygame.display.Info()
scrW, scrH = infoObject.current_w, infoObject.current_h
xShift = scrW/2 - 385
yShift = scrH/2 - 220
xSize, ySize = scrW, scrH #770, 440
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Mission_1")
pygame.mouse.set_visible(False)

try:
    gunshot = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/gunshot.wav"))
except:
    print("can't load sound")

mx, my = pygame.mouse.get_pos()
still = False
spL = 500
gifC = 1 #Current Hitler GIF
dif = 150 #Window Gap
shoot = False
shot = False
sf = 0 #shoot frame
mouseHold = False
hit = False
hitKx = randint(0,4) #The X Hitler Constant
hitKy = randint(0,2) #The Y Hitler Constant
hitlerMove = False
moveC = 0

#----------------------Main Loop----------------------#

done = False
clock = pygame.time.Clock()
frameCount = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shoot == False:
                mouseHold = True
                shot = True
                gunshot.play()
        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([150,150,150])
    frameCount += 1
    mx, my = pygame.mouse.get_pos()
    cx, cy = mx, my
    if cx > xSize - xShift:
        cx = xSize - xShift
    if cx < xShift:
        cx = xShift    
    if cy > ySize - yShift:
        cy = ySize - yShift
    if cy < yShift:
        cy = yShift

    if gifC >= 53:
        gifC = 1
    else:
        gifC += .2

    for i in range(4):
        for t in range(3):
            backW = pygame.draw.rect(screen, WHITE, (xShift+70+dif*i,yShift+70+dif*t,32,32))
            cover = pygame.draw.rect(screen, WHITE, (xShift+70+dif*i+32,yShift+70+dif*t,150,32))
            
    if mouseHold == True:
        shoot = True

    if shoot == True:
        sf += 6
        if sf <= 5*math.sqrt(10):
            cy = my - 2*(10 - math.pow(sf/5 - math.sqrt(10), 2))
        elif sf <= 25*math.sqrt(10):
            cy = my - 2*(10 - math.pow(sf/20 - math.sqrt(10)/4, 2))
        if cy < yShift:
            cy = yShift
        if sf > 25*math.sqrt(10):
            shoot = False
            sf = 0

    if hitlerMove == True and hit == False:
        if moveC <= 60:
            moveC += 1
        else:
            done = True
    
    if set_gifC(gifC) < 10:
        hitler = pygame.image.load(dir_path + "/Game Files/Images/Hitler/l0_hitler_0{0}.bmp".format(int(set_gifC(gifC))))
    else:
        hitler = pygame.image.load(dir_path + "/Game Files/Images/Hitler/l0_hitler_{0}.bmp".format(int(set_gifC(gifC))))

    if hit == True:
        if frameCount-killFrame <= 32:
            hitler = pygame.transform.scale(hitler, (32, 32-frameCount+killFrame))
            screen.blit(hitler,(xShift+70+dif*hitKx+moveC/1, yShift+70+dif*hitKy+frameCount-killFrame))
    else:
        screen.blit(hitler,(xShift+70+dif*hitKx+moveC/1, yShift+70+dif*hitKy))
            
    if hit == True:
        if 0 <= (frameCount - killFrame)/2 <= 3:
            stain = pygame.image.load(dir_path + "/Game Files/Images/Blood/blood_{0}.bmp".format(int((frameCount - killFrame)/2)))
        else:
            stain = pygame.image.load(dir_path + "/Game Files/Images/Blood/blood_{0}.bmp".format(3))
        screen.blit(stain,(kx-16, ky-16))
        if (frameCount - killFrame)/2 > 40:
            done = True

    for t in range(3):
        for i in range(5):
            cover1 = pygame.draw.rect(screen, [150,150,150], (xShift+70+dif*i+32,yShift+70+dif*t,118,32))
        if t == 0:
            cover2 = pygame.draw.rect(screen, [150,150,150], (xShift,yShift+dif*t,xSize - xShift*2,dif - 80))
        else:
            cover2 = pygame.draw.rect(screen, [150,150,150], (xShift,yShift+dif*t - 48,xSize - xShift*2,dif - 32))
            
    cover3 = pygame.draw.rect(screen, [150,150,150], (xShift,yShift+dif*3 - 48,xSize - xShift*2,dif - 32))
    cover4 = pygame.draw.rect(screen, [150,150,150], (xShift,yShift,70,ySize - yShift*2))
            
    #Windows
    for i in range(5):
        i += xShift/dif
        for t in range(3):
            t += yShift/dif
            hTop = pygame.draw.line(screen, BLACK, (70+dif*i, 70+dif*t), (102+dif*i, 70+dif*t), 1)
            hMid = pygame.draw.line(screen, BLACK, (70+dif*i, 86+dif*t), (102+dif*i, 86+dif*t), 1)
            hBot = pygame.draw.line(screen, BLACK, (70+dif*i, 102+dif*t), (102+dif*i, 102+dif*t), 1)
            vLef = pygame.draw.line(screen, BLACK, (70+dif*i, 70+dif*t), (70+dif*i, 102+dif*t), 1)
            vMid = pygame.draw.line(screen, BLACK, (86+dif*i, 70+dif*t), (86+dif*i, 102+dif*t), 1)
            vRig = pygame.draw.line(screen, BLACK, (102+dif*i, 70+dif*t), (102+dif*i, 102+dif*t), 1)

    if hit == False and shot == True and xShift+70+dif*hitKx < mx < xShift+102+dif*hitKx and yShift+70+dif*hitKy < my < yShift+102+dif*hitKy and mx != xShift+86+dif*hitKx and my != yShift+86+dif*hitKy and screen.get_at((mx, my)) != (255,255,255,255):
        hit = True
        killFrame = frameCount
        kx, ky = mx, my
    elif shot == True and xShift+70+dif*hitKx < mx < xShift+102+dif*hitKx and yShift+70+dif*hitKy < my < yShift+102+dif*hitKy:
        hitlerMove = True
    
    #Crosshair
    black = pygame.image.load(dir_path + "/Game Files/Images/black.png")
    screen.blit(black,(cx-770, cy-500))
    lLine = pygame.draw.line(screen, BLACK, (cx - 100, cy), (cx - 10, cy), 1)
    rLine = pygame.draw.line(screen, BLACK, (cx + 100, cy), (cx + 10, cy), 1)
    uLine = pygame.draw.line(screen, BLACK, (cx, cy - 100), (cx, cy - 10), 1)
    dLine = pygame.draw.line(screen, BLACK, (cx, cy + 100), (cx, cy + 10), 1)
    cRect = pygame.draw.rect(screen, BLACK, (cx-1, cy-1, 3, 3))

    pygame.draw.rect(screen, [50,50,50], [0,0, xSize, yShift])
    pygame.draw.rect(screen, [50,50,50], [0,0, xShift, ySize])
    pygame.draw.rect(screen, [50,50,50], [xSize-xShift,0, xShift, ySize])
    pygame.draw.rect(screen, [50,50,50], [0,ySize-yShift, xSize, yShift])

    shot = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

if hit == True:
    roll_text("Mission complete.")
    time.sleep(1)
    print("")
    print("")
    if binRead == "1":
        print("-----------------------------Brief Closed-----------------------------")
        print("")
    roll_text("(Press enter to load newspaper)")
    input("")
    print("")
    print("")
    exec(open(dir_path + "/Game Files/Missions/News_Flash.py").read(), globals())
else:
    roll_text("Hitler escaped.")
    time.sleep(1)
    roll_text(" Mission failed.")
    time.sleep(1)
