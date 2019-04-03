import pygame
import math
import time
import random
from random import randint
import sys
from ctypes import windll
from math import atan2, degrees, pi
import os

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

lockSave = chp1 + chp2 + "1"

tsaved = lockSave.encode(encoding='UTF-8')
newFile = open(dir_path + "/Game Files/Saves/been.txt", "wb")
newFile.write(tsaved)
newFile = open(dir_path + "/Game Files/Saves/been.txt", "rb")


if chp3 == "0":
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
    binRead = newFile.read(1).decode(encoding='UTF-8')
except:
    binRead = "1"

def roll_text(string):
    text = ''
    for i in range(len(string)):
    
        print(string[i], end='', flush=True)
        time.sleep(0.04)

def getAngle(x1:float,y1:float,x2:float,y2:float):
    dx = x2 - x1
    dy = y2 - y1
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    return degs

def rot_center(image, rect, angle, custom):
    #rotate an image while keeping its center
    if antiA == True:
        rot_image = pygame.transform.rotozoom(image, angle, 1)
    else:
        rot_image = pygame.transform.rotate(image, angle)
    if custom == False:
        rot_rect = rot_image.get_rect(center=rect.center)
    else:
        rot_rect = rot_image.get_rect(center=[rect_x + 41.4*math.sin(math.radians(angle+55.9)), rect_y + 41.4*math.cos(math.radians(angle+55.9))])
    return rot_image,rot_rect

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)

# Variables
BLACK = (0, 0, 0)
BACK = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FLESH = (255, 217, 179)
ZOMBIE = (30, 123, 123)
DEAD = (138,7,7)
BULLET = (38, 38, 38)

pSpeed = 4
zSpeed = 2
infZom = False

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
    roll_text("Mission 3")
    time.sleep(1)
    print("")
    print("")
    roll_text("As you may have heard, there is a zombie outbreak in Germany. ")
    time.sleep(1)
    roll_text("We have selected you to remove this threat to mankind. ")
    time.sleep(1)
    roll_text("They are very")
    print("")
    roll_text("dangerous; do not let them touch you. ")
    time.sleep(1)
    roll_text("Good luck. ")
    time.sleep(1)
    print("")
    print("")
    roll_text("(WASD or arrow keys to move, select weapon with numbers 1-4, click to shoot)")
    time.sleep(1)
    print("")
else:
    roll_text("Brief skipped. ")
    
roll_text("(Press enter when ready)")
input("")
print("")

#Settings
nZombies = 100
antiA = True
zOrbit = False
pan = False

cZombies = 0
waves = 2
weapon = 1

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
SetWindowPos = windll.user32.SetWindowPos
SetWindowPos(pygame.display.get_wm_info()['window'], -1, 400, 300, 0, 0, 0x0001)

try:
    rain = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/rain.wav"))
    lightning = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/lightning.wav"))
    axe_swing = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/axe_swing.wav"))
    pistol = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/pistol.wav"))
    shotgun = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/shotgun_blast_2.wav"))
    minigun = pygame.mixer.Sound(os.path.join(dir_path + "/Game Files/Sound/minigun.wav"))
except:
    print("Can't load sound.")

rain.play(-1)

infoObject = pygame.display.Info()
scrW, scrH = infoObject.current_w, infoObject.current_h
xSize, ySize = scrW, scrH
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Mission_1")
#pygame.mouse.set_visible(False)

myFont = pygame.font.SysFont("monospace", 15)

rect_x = xSize/2
rect_y = ySize/2
hitDelay = 120
shotDelay = 0
bulletLimit = 100
bulletSpeed = 30
timesOver = 0
totalCount = 0
shotCount = 0
hitCount = 0
SGCount = 0
SGPellets = 5
MGCount = 0
MGRate = 1
swingTick = 0

axeW = 88
axeH = 100
ax2 = pygame.image.load(dir_path + "/Game Files/Images/Weapons/blank_img.bmp")
axe = pygame.image.load(dir_path + "/Game Files/Images/Weapons/axe_100x88.bmp")
axe = pygame.transform.scale(axe, (axeW,axeH))
ax2 = pygame.transform.scale(ax2, (22,50))
pistW = 30
pistH = 30
pistX = random.randrange(300-pistW/2, 900-pistW/2)
pistY = random.randrange(200-pistH/2, 600-pistH/2)
shotW = 30
shotH = 30
shotX = random.randrange(0, xSize-shotW)
shotY = random.randrange(0, ySize-shotH)
miniW = 30
miniH = 30
miniX = random.randrange(0, xSize-miniW)
miniY = random.randrange(0, ySize-miniH)
hasPist = False
hasShot = True
hasMini = True
pistAmmo = 100
shotAmmo = 100
miniAmmo = 0
currentAmmo = 0
pistDropped = True
shotDropped = False
miniDropped = False
swing = False
swingBack = False
panx = 0
pany = 0

backgSize = 1000
backg = pygame.image.load(dir_path + "/Game Files/Images/grass.bmp")
backg = pygame.transform.scale(backg, (backgSize, backgSize))
for y in range(0, int(ySize/backgSize) + 1):
        for x in range(0, int(xSize/backgSize + 1)):
            screen.blit(backg,(x*backgSize,y*backgSize))

zd = {}
bd = {}
randd = {}
if nZombies != "inf":
    nZombies += 1
    uprange = nZombies
else:
    uprange = 100000

#Zombie Properties
for x in range(1,uprange):
    
    side = random.randint(0,3)
    if side == 0:
        randd["randx{0}".format(x)] = -30
        randd["randy{0}".format(x)] = random.randint(0,ySize)
    elif side == 1:
        randd["randx{0}".format(x)] = random.randint(0,xSize)
        randd["randy{0}".format(x)] = -30
    elif side == 2:
        randd["randx{0}".format(x)] = xSize + 30
        randd["randy{0}".format(x)] = random.randint(0,ySize)
    elif side == 3:
        randd["randx{0}".format(x)] = random.randint(0,xSize)
        randd["randy{0}".format(x)] = ySize + 30
        
    zd["panx{0}".format(x)] = 0
    zd["pany{0}".format(x)] = 0
    zd["canMove{0}".format(x)] = True
    zd["moveBack{0}".format(x)] = False
    zd["speedBack{0}".format(x)] = 50
    zd["axed{0}".format(x)] = False
    zd["zgif{0}".format(x)] = pygame.image.load(dir_path + "/Game Files/Images/Zombies/zombie_0{0}.bmp".format(randint(0,5)))
    zd["zgif{0}".format(x)] = pygame.transform.scale(zd["zgif{0}".format(x)], (100,100))
    dgifn = randint(6,10)
    if dgifn < 10:
        zd["dgif{0}".format(x)] = pygame.image.load(dir_path + "/Game Files/Images/Zombies/zombie_0{0}.bmp".format(dgifn))
    else:
        zd["dgif{0}".format(x)] = pygame.image.load(dir_path + "/Game Files/Images/Zombies/zombie_{0}.bmp".format(randint(10,11)))
    zd["dgif{0}".format(x)] = pygame.transform.scale(zd["dgif{0}".format(x)], (100,100))
    zd["newZom{0}".format(x)] = (0,0)
    zd["first{0}".format(x)] = True

bd["bull_x{0}".format(shotCount)] = -4
bd["bull_y{0}".format(shotCount)] = -4
bd["recx{0}".format(shotCount)] = rect_x
bd["recy{0}".format(shotCount)] = rect_y
bd["posx{0}".format(shotCount)] = xSize/2-2
bd["posy{0}".format(shotCount)] = ySize/2-2

rains = 200
rSpeed = 20
bound = 1000
click = False
rain = {}

for x in range(1,rains):
    rain["alive{0}".format(x)] = False
    rain["height{0}".format(x)] = 40
    rain["rainx{0}".format(x)] = randint(0,xSize + 200) - 100
    rain["rainy{0}".format(x)] = randint(0,ySize + 200) - 100
    rain["destx{0}".format(x)] = (xSize/2 - rain["rainx{0}".format(x)])/8 + rain["rainx{0}".format(x)] + randint(-10,10)
    rain["desty{0}".format(x)] = (ySize/2 - rain["rainy{0}".format(x)])/8 + rain["rainy{0}".format(x)] + randint(-10,10)
 
pygame.display.set_caption("Zombie Shooter")
done = False
clock = pygame.time.Clock()

#----------------------Initial Loop----------------------#

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            done = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([0,0,0])
    ifont = pygame.font.SysFont("dotum", 40)
    label = ifont.render("Please Click", 1, (255,255,255))
    screen.blit(label, (0,0))
    
    pygame.display.flip()
    
done = False

#----------------------Main Loop----------------------#
repeat = False
mouseHold = False
hit = False
dead = False
SGFiring = False
paused = False
deadCheck = False
killAll = False
frameCount = 0
doneFrame = 0
gifC = 0

while not done:
    if swing == True:
        click = False
    frameCount += 1
    mx, my = pygame.mouse.get_pos()
    moving = False
    
    keys = pygame.key.get_pressed()
    fired = False

    if weapon == 2:
        currentAmmo = pistAmmo
        gifC = 6
    elif weapon == 3:
        currentAmmo = shotAmmo
        gifC = 4
    elif weapon == 4:
        currentAmmo = miniAmmo
        gifC = 8
    else:
        currentAmmo = 0
        gifC = 0
    
    if shotCount > bulletLimit:
        timesOver += 1
        shotCount = 0

    #Keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if keys[pygame.K_ESCAPE]:
            if paused == False:
                paused = True
            else:
                paused = False
        if keys[pygame.K_1]:
            weapon = 1
            currentAmmo = 0
        if keys[pygame.K_2]:
            if hasPist == True:
                weapon = 2
                currentAmmo = pistAmmo
        if keys[pygame.K_3]:
            if hasShot == True:
                weapon = 3
                currentAmmo = shotAmmo
        if keys[pygame.K_4]:
            if hasMini == True:
                weapon = 4
                currentAmmo = miniAmmo
        if event.type == pygame.KEYDOWN:
            repeat = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            if shotDelay >= 10 and paused == False and (hasPist == True or hasShot == True) and weapon != 1 and currentAmmo > 0:
                shotDelay = 0
                if weapon == 2:
                    pistAmmo -= 1
                    pistol.play()
                    gifC = 7
                elif weapon == 3:
                    shotAmmo -= 1
                    shotgun.play()
                mox, moy = pygame.mouse.get_pos()
                if mox != rect_x and moy != rect_y:
                    totalCount += 1
                    shotCount += 1
                    
                bd["posx{0}".format(shotCount-1)], bd["posy{0}".format(shotCount-1)] = pygame.mouse.get_pos()
                SGposx = bd["posx{0}".format(shotCount-1)]
                SGposy = bd["posy{0}".format(shotCount-1)]
                bd["recx{0}".format(shotCount-1)] = rect_x
                bd["recy{0}".format(shotCount-1)] = rect_y

                bd["bull_x{0}".format(shotCount-1)] = rect_x
                bd["bull_y{0}".format(shotCount-1)] = rect_y
                hit = False
                BULLET = (38, 38, 38)
                fired = True
            elif weapon == 1:
                swing = True
                
    screen.fill(BACK)
    
    if repeat == True and paused == False:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            moving = True
            if pan == False:
                rect_x -= pSpeed
            else:
                panx += pSpeed
                for x in range(1,cZombies):
                    zd["panx{0}".format(x)] += pSpeed
                rect_x = xSize/2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            moving = True
            if pan == False:
                rect_x += pSpeed
            else:
                panx -= pSpeed
                for x in range(1,cZombies):
                    zd["panx{0}".format(x)] -= pSpeed
                rect_x = xSize/2
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            moving = True
            if pan == False:
                rect_y -= pSpeed
            else:
                pany += pSpeed
                for x in range(1,cZombies):
                    zd["pany{0}".format(x)] += pSpeed
                rect_y = ySize/2
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            moving = True
            if pan == False:
                rect_y += pSpeed
            else:
                pany -= pSpeed
                for x in range(1,cZombies):
                    zd["pany{0}".format(x)] -= pSpeed
                rect_y = ySize/2
            
    #Background
    for y in range(0, int(ySize/backgSize) + 1):
        for x in range(0, int(xSize/backgSize + 1)):
            screen.blit(backg,(x*backgSize,y*backgSize))

    for x in range(1,cZombies):
        if zd["speedBack{0}".format(x)] == 0:
            zd["zombie{0}".format(x)] = zd["dgif{0}".format(x)]
            #zd["zombie{0}".format(x)] = pygame.transform.scale(zd["zombie{0}".format(x)], (100,100))
            screen.blit(zd["zombie{0}".format(x)], [randd["randx{0}".format(x)]-50 + panx, randd["randy{0}".format(x)]-50 + pany])
            zd["zomRec{0}".format(x)] = pygame.Rect([randd["randx{0}".format(x)]-15 + panx, randd["randy{0}".format(x)]-15 + pany, 30, 30])
    
    #Text
    scoreLabel = myFont.render("Score: " + str(hitCount), 1, (0,0,0))
    screen.blit(scoreLabel, (0, 0))
    ammoLabel = myFont.render("Ammo: " + str(currentAmmo), 1, (0,0,0))
    if weapon == 1:
        ammoLabel = myFont.render("Ammo: inf", 1, (0,0,0))
    screen.blit(ammoLabel, (0, ySize - 20))
    
    #Image
    #Axe
    axeX = rect_x
    axeY = rect_y

    ax2 = pygame.image.load(dir_path + "/Game Files/Images/Weapons/blank_img.bmp")
    if weapon == 1:
        axe = pygame.image.load(dir_path + "/Game Files/Images/Weapons/axe_100x88.bmp")
        axe = pygame.transform.scale(axe, (axeW,axeH))
        ax2 = pygame.transform.scale(ax2, (22,50))
        if weapon == 1 and swing == False and swingBack == False:
            mox, moy = pygame.mouse.get_pos()
            degs = getAngle(rect_x,rect_y,mox,moy)
            oldRec2 = ax2.get_rect(center=(axeX,axeY))
            ax2, newRec2 = rot_center(ax2,oldRec2,degs - 90,True)
            
            oldRect = axe.get_rect(center=(axeX,axeY))
            axe, newRect = rot_center(axe,oldRect,degs - 90,False)
            screen.blit(axe, newRect)
            
        axeRect = axe.get_rect()
        axeRect.x = axeX
        axeRect.y = axeY
        
        ax2Rect = ax2.get_rect()
        ax2Rect.x = axeX
        ax2Rect.y = axeY

    #Pistol
    pist = pygame.image.load(dir_path + "/Game Files/Images/Weapons/pistol_30x30.bmp")
    pist = pygame.transform.scale(pist, (pistW,pistH))
    pistRect = pist.get_rect()
    if pistDropped == True and hasPist == False:
        screen.blit(pist,(pistX + panx, pistY + pany))
    pistRect.x = pistX + panx
    pistRect.y = pistY + pany

    #Shotgun
    shot = pygame.image.load(dir_path + "/Game Files/Images/Weapons/shotgun_30x30.bmp")
    shot = pygame.transform.scale(shot, (shotW,shotH))
    shotRect = shot.get_rect()
    if shotDropped == True and hasShot == False:
        screen.blit(shot,(shotX + panx, shotY + pany))
    shotRect.x = shotX + panx
    shotRect.y = shotY + pany

    #Minigun
    mini = pygame.image.load(dir_path + "/Game Files/Images/Weapons/mini_30x30.bmp")
    mini = pygame.transform.scale(mini, (miniW,miniH))
    miniRect = mini.get_rect()
    if miniDropped == True and hasMini == False:
        screen.blit(mini,(miniX + panx, miniY + pany))
    miniRect.x = miniX + panx
    miniRect.y = miniY + pany

    #Move Axe
    newRec2 = axe.get_rect(center=(axeX,axeY))
    if swing == True and weapon == 1:
        if click == True:
            axe_swing.play()
        if swingTick == 0:
            mox, moy = pygame.mouse.get_pos()
        swingTick += 2
        oldRect = axe.get_rect(center=(axeX,axeY))
        degs = getAngle(rect_x,rect_y,mox,moy)
        ax2, newRec2 = rot_center(ax2,oldRect,degs - 90 + swingTick*12, True)
        #screen.blit(ax2, newRec2)
        axe, newRect = rot_center(axe,oldRect,degs - 90 + swingTick*12, False)
        screen.blit(axe, newRect)
        if swingTick >= 20:
            swingBack = True
            swing = False
    elif swingBack == True:
        swingTick -= 1.5
        oldRect = axe.get_rect(center=(axeX,axeY))
        degs = getAngle(rect_x,rect_y,mox,moy)
        ax2, newRec2 = rot_center(ax2,oldRect,degs - 90 + swingTick*12, True)
        #screen.blit(ax2, newRec2)
        axe, newRect = rot_center(axe,oldRect,degs - 90 + swingTick*12, False)
        screen.blit(axe, newRect)
        if swingTick <= 0:
            swingTick = 0
            swingBack = False
            swing = False
    
    newerRect = newRec2
        
    #Move Bullets 
    if (weapon == 3 and fired == True) or SGFiring == True:
        gifC = 5
        SGCount += 1
        if SGCount <= int(SGPellets):
            SGFiring = True
            if shotDelay >= 0 and paused == False:
                shotDelay = 0
                mox, moy = pygame.mouse.get_pos()
                if mox != rect_x and moy != rect_y:
                    totalCount += 1
                    shotCount += 1
                if  SGCount == 0:
                    bd["posx{0}".format(shotCount-1)], bd["posy{0}".format(shotCount-1)] = pygame.mouse.get_pos()
                    SGposx = bd["posx{0}".format(shotCount-1)]
                    SGposy = bd["posy{0}".format(shotCount-1)]
                else:
                    bd["posx{0}".format(shotCount-1)] = SGposx + random.randint(0,30) - 15
                    bd["posy{0}".format(shotCount-1)] = SGposy + random.randint(0,30) - 15

                bd["recx{0}".format(shotCount-1)] = rect_x
                bd["recy{0}".format(shotCount-1)] = rect_y

                bd["bull_x{0}".format(shotCount-1)] = rect_x
                bd["bull_y{0}".format(shotCount-1)] = rect_y
                hit = False
                BULLET = (38, 38, 38)
                fired = True
        else:
            SGCount = 0
            SGFiring = False
        
    if weapon == 4 and mouseHold == True:
        if frameCount % 2 == 0:
            gifC = 8
        else:
            gifC = 9
        minigun.play()
        MGCount += 1
        if MGCount == int(MGRate):
            MGCount = 0
            if shotDelay >= 0 and paused == False:
                shotDelay = 0
                mox, moy = pygame.mouse.get_pos()
                if mox != rect_x and moy != rect_y:
                    totalCount += 1
                    shotCount += 1
                    
                bd["posx{0}".format(shotCount-1)], bd["posy{0}".format(shotCount-1)] = pygame.mouse.get_pos()

                bd["recx{0}".format(shotCount-1)] = rect_x
                bd["recy{0}".format(shotCount-1)] = rect_y

                bd["bull_x{0}".format(shotCount-1)] = rect_x
                bd["bull_y{0}".format(shotCount-1)] = rect_y
                hit = False
                BULLET = (38, 38, 38)
                fired = True

    if totalCount <= bulletLimit:
        rang = totalCount
    else:
        rang = bulletLimit
    for i in range(rang):
        if i > bulletLimit:
            i -= bulletLimit*timesOver
        if weapon == 2:
            distance = math.sqrt(math.pow(bd["posx{0}".format(i)] - bd["recx{0}".format(i)], 2) + math.pow(bd["posy{0}".format(i)] - bd["recy{0}".format(i)], 2))
            if distance != 0 and paused == False:
                bd["bull_x{0}".format(i)] += bulletSpeed*(bd["posx{0}".format(i)] - bd["recx{0}".format(i)])/distance
                bd["bull_y{0}".format(i)] += bulletSpeed*(bd["posy{0}".format(i)] - bd["recy{0}".format(i)])/distance
                bd["bullet{0}".format(i)] = pygame.draw.rect(screen, BULLET, [bd["bull_x{0}".format(i)], bd["bull_y{0}".format(i)], 4, 4])
        elif weapon == 3:
            distance = math.sqrt(math.pow(bd["posx{0}".format(i)] - bd["recx{0}".format(i)], 2) + math.pow(bd["posy{0}".format(i)] - bd["recy{0}".format(i)], 2))
            if distance != 0 and paused == False:
                bd["bull_x{0}".format(i)] += bulletSpeed*(bd["posx{0}".format(i)] - bd["recx{0}".format(i)])/distance
                bd["bull_y{0}".format(i)] += bulletSpeed*(bd["posy{0}".format(i)] - bd["recy{0}".format(i)])/distance
                bd["bullet{0}".format(i)] = pygame.draw.rect(screen, BULLET, [bd["bull_x{0}".format(i)], bd["bull_y{0}".format(i)], 4, 4])
        elif weapon == 4:
            distance = math.sqrt(math.pow(bd["posx{0}".format(i)] - bd["recx{0}".format(i)], 2) + math.pow(bd["posy{0}".format(i)] - bd["recy{0}".format(i)], 2))
            if distance != 0 and paused == False:
                bd["bull_x{0}".format(i)] += bulletSpeed*(bd["posx{0}".format(i)] - bd["recx{0}".format(i)])/distance
                bd["bull_y{0}".format(i)] += bulletSpeed*(bd["posy{0}".format(i)] - bd["recy{0}".format(i)])/distance
                bd["bullet{0}".format(i)] = pygame.draw.rect(screen, BULLET, [bd["bull_x{0}".format(i)], bd["bull_y{0}".format(i)], 4, 4])

    #Light
    darkb = 50
    sb = pygame.Surface((xSize,ySize))
    sb.set_alpha(darkb)
    sb.fill((0,0,0))
    screen.blit(sb, (0,0))

    #Person
    person = pygame.image.load(dir_path + "/Game Files/Images/Guy/top_guy_0{0}.bmp".format(gifC))
    person = pygame.transform.scale(person, (150,150))
    oldPerson = person.get_rect(center=(rect_x,rect_y))
    degs = getAngle(rect_x,rect_y,mx,my)
    person, newPerson = rot_center(person, oldPerson, degs - 90, False)
    screen.blit(person, newPerson)
    person = pygame.Rect(rect_x-15, rect_y-15, 30, 30)
    
    #person = pygame.draw.rect(screen, FLESH, [rect_x-15, rect_y-15, 30, 30])

    #Check Weapon Pickup
    if person.colliderect(pistRect) == True and hasPist == False:
        pistW = 0
        pistH = 0
        swing = False
        swingback = False
        pistDropped = False
        hasPist = True
        pistAmmo += 20
        weapon = 2

    if person.colliderect(shotRect) == True and hasShot == False:
        shotW = 0
        shotH = 0
        swing = False
        swingback = False
        shotDropped = False
        hasShot = True
        shotAmmo += 20
        weapon = 3

    if person.colliderect(miniRect) == True and hasMini == False:
        miniW = 0
        miniH = 0
        swing = False
        swingback = False
        miniDropped = False
        hasMini = True
        weapon = 4
    
    #Create / Move Zombies
    czDead = False
        
    if infZom == True:
        nZombies = cZombies + 1
        upperRange = int(25*math.sin(cZombies/10 - 4.7) + 30)
        #print("1 /", int(25*math.sin(cZombies/10 - 4.7) + 30))
    else:
        upperRange = int((1 + (nZombies - cZombies))/2)
        
    if cZombies < nZombies and random.randint(1, upperRange) == 1:
        cZombies += 1
        #if cZombies != 1:
            #print(cZombies-1)
    deadCheck = True
    for x in range(1,cZombies):
        if zd["moveBack{0}".format(x)] == False:
            zSpeed = int(randint(5,20)/5)
        else:
            zSpeed = 2
        if zd["speedBack{0}".format(x)] != 0:
            czDead = False
            deadCheck = False
            
            if zd["first{0}".format(x)] == True:
                zd["zombie{0}".format(x)] = zd["zgif{0}".format(x)]
                
            if  zd["first{0}".format(x)] == True or moving == True or frameCount == 1:
                zd["zombie{0}".format(x)] = zd["zgif{0}".format(x)]
                oldZom = zd["zombie{0}".format(x)].get_rect(center=(randd["randx{0}".format(x)],randd["randy{0}".format(x)]))
                degs = getAngle(randd["randx{0}".format(x)], randd["randy{0}".format(x)],rect_x,rect_y)
                zd["zombie{0}".format(x)], zd["newZom{0}".format(x)] = rot_center(zd["zombie{0}".format(x)], oldZom, degs - 90, False)
            else:
                zd["newZom{0}".format(x)] = zd["zombie{0}".format(x)].get_rect(center=(randd["randx{0}".format(x)],randd["randy{0}".format(x)]))
                
            screen.blit(zd["zombie{0}".format(x)], zd["newZom{0}".format(x)])
            zd["zomRec{0}".format(x)] = pygame.Rect(randd["randx{0}".format(x)]-20, randd["randy{0}".format(x)]-20, 40, 40)
            
            if zd["first{0}".format(x)] == True:
                zd["first{0}".format(x)] = False
        else:
            czDead = True
        if pan == False or zd["moveBack{0}".format(x)] == False or 1 == 1:
            distx = zSpeed*(rect_x - randd["randx{0}".format(x)] - zd["panx{0}".format(x)])/math.sqrt(math.pow(rect_x - randd["randx{0}".format(x)] - zd["panx{0}".format(x)], 2) + math.pow(rect_y - randd["randy{0}".format(x)] - zd["pany{0}".format(x)], 2))
            disty = zSpeed*(rect_y - randd["randy{0}".format(x)] - zd["pany{0}".format(x)])/math.sqrt(math.pow(rect_x - randd["randx{0}".format(x)] - zd["panx{0}".format(x)], 2) + math.pow(rect_y - randd["randy{0}".format(x)] - zd["pany{0}".format(x)], 2))
        else: 
            distx = zSpeed*(xSize/2 - randd["randx{0}".format(x)] - zd["panx{0}".format(x)])/math.sqrt(math.pow(xSize/2 - randd["randx{0}".format(x)] - zd["panx{0}".format(x)], 2) + math.pow(ySize/2 - randd["randy{0}".format(x)] - zd["pany{0}".format(x)], 2))
            disty = zSpeed*(ySize/2 - randd["randy{0}".format(x)] - zd["pany{0}".format(x)])/math.sqrt(math.pow(xSize/2 - randd["randx{0}".format(x)] - zd["panx{0}".format(x)], 2) + math.pow(ySize/2 - randd["randy{0}".format(x)] - zd["pany{0}".format(x)], 2))

        if zd["canMove{0}".format(x)] == True and zd["moveBack{0}".format(x)] == False and paused == False:
            randd["randx{0}".format(x)] += distx
            randd["randy{0}".format(x)] += disty
            
        elif zd["canMove{0}".format(x)] == True and zd["moveBack{0}".format(x)] == True and paused == False:
            if zd["axed{0}".format(x)] == False:
                randd["randx{0}".format(x)] -= math.pow(zd["speedBack{0}".format(x)],3)/2500*distx
                randd["randy{0}".format(x)] -= math.pow(zd["speedBack{0}".format(x)],3)/2500*disty
            else:
                randd["randy{0}".format(x)] += math.pow(zd["speedBack{0}".format(x)],3)/2500*distx
                randd["randx{0}".format(x)] -= math.pow(zd["speedBack{0}".format(x)],3)/2500*disty
                
            if zd["speedBack{0}".format(x)] > 5:
                if zOrbit == False or zd["axed{0}".format(x)] == False:
                    zd["speedBack{0}".format(x)] -= 8
                else:
                    zd["speedBack{0}".format(x)] = 30
            else:
                zd["speedBack{0}".format(x)] = 0
            
        #Check if Zombies Hit
        #Check Axe Hit
        if newRec2.colliderect(zd["zomRec{0}".format(x)]) == True and swing == True and czDead == False and zd["axed{0}".format(x)] == False:
            side = random.randint(0,3)
            hitCount += 1
            #Drop Weapons
##            if random.randrange(1,2) == 1 and pistDropped == False:
##                pistX = randd["randx{0}".format(x)]
##                pistY = randd["randy{0}".format(x)]
##                screen.blit(pist,(pistX, pistY))
##                pistDropped = True
            if random.randrange(0,30) == 1 and shotDropped == False:
                shotX = randd["randx{0}".format(x)]
                shotY = randd["randy{0}".format(x)]
                screen.blit(shot,(shotX, shotY))
                shotDropped = True
            elif random.randrange(0,200) == 1 and miniDropped == False:
                miniX = randd["randx{0}".format(x)]
                miniY = randd["randy{0}".format(x)]
                screen.blit(mini,(miniX, miniY))
                miniDropped = True
            zd["moveBack{0}".format(x)] = True
            zd["speedBack{0}".format(x)] = 45
            zd["axed{0}".format(x)] = True
            zd["dgif{0}".format(x)] = pygame.image.load(dir_path + "/Game Files/Images/Zombies/zombie_{0}.bmp".format(randint(12,15)))
            zd["dgif{0}".format(x)] = pygame.transform.scale(zd["dgif{0}".format(x)], (100,100))
##            randd["randx{0}".format(x)] = -300
##            randd["randy{0}".format(x)] = -300
##            zd["canMove{0}".format(x)] = True

        #Check Bullet Hit
        for i in range(rang):
            if i > bulletLimit:
                i -= bulletLimit*timesOver
            if distance != 0 and hit == False and paused == False and czDead == False:
                if hit == False and bd["bullet{0}".format(i)].colliderect(zd["zomRec{0}".format(x)]) == True and zd["moveBack{0}".format(x)] == False:
                    #hit = True
                    bd["bull_x{0}".format(i)] = -10000
                    bd["bull_y{0}".format(i)] = -10000
                    hitDelay = 0
                    hitCount += 1
                    bd["recx{0}".format(i)] = rect_x
                    bd["recy{0}".format(i)] = rect_y
                    side = random.randint(0,3)
                    #Drop Weapons
##                    if random.randrange(1,2) == 1 and pistDropped == False:
##                        pistX = randd["randx{0}".format(x)]
##                        pistY = randd["randy{0}".format(x)]
##                        screen.blit(pist,(pistX, pistY))
##                        pistDropped = True
                    if random.randrange(1,30) == 1 and shotDropped == False:
                        shotX = randd["randx{0}".format(x)]
                        shotY = randd["randy{0}".format(x)]
                        screen.blit(shot,(shotX, shotY))
                        shotDropped = True
                    elif random.randrange(1,200) == 1 and miniDropped == False:
                        miniX = randd["randx{0}".format(x)]
                        miniY = randd["randy{0}".format(x)]
                        screen.blit(mini,(miniX, miniY))
                        miniDropped = True
                    zd["moveBack{0}".format(x)] = True
                    if weapon == 2:
                        zd["speedBack{0}".format(x)] = 35
                    else:
                        zd["speedBack{0}".format(x)] = 55-math.sqrt(math.pow(abs(randd["randx{0}".format(x)] - rect_x), 2)+math.pow(abs(randd["randy{0}".format(x)] - rect_y), 2))/30
                        #print(math.sqrt(math.pow(abs(randd["randx{0}".format(x)] - rect_x), 2)*math.pow(abs(randd["randy{0}".format(x)] - rect_y), 2)))
                    zd["axed{0}".format(x)] = False
##                    randd["randx{0}".format(x)] = -300
##                    randd["randy{0}".format(x)] = -300
##                    zd["canMove{0}".format(x)] = False
                
        if dead == False and zd["moveBack{0}".format(x)] == False and person.colliderect(zd["zomRec{0}".format(x)]) == True:
            dead = True
            done = True
            print("eaten")

    if killAll == False and deadCheck == True and cZombies >= nZombies:
        doneFrame = frameCount
        killAll = True
        
    if killAll == True and frameCount - doneFrame > 100:
        done = True

    shotDelay += 1

    if paused == True:
        BACK = (217, 217, 217)
    else:
        BACK = (255, 255, 255)

    #Light
    dark = 170
    r = frameCount % bound
    if 0 <= r < 10 or 25 <= r < 35:
        dark = 0
    elif r == 35:
        bound = randint(1000,2000)
        lightning.play()

    s = pygame.Surface((xSize,ySize))
    s.set_alpha(dark)
    s.fill((0,0,0))
    screen.blit(s, (0,0))
        
    #Rain
    for x in range(1,rains):
        if rain["alive{0}".format(x)] == True:
            rain["height{0}".format(x)] -= 1
            h = rain["height{0}".format(x)]
            rx, ry = rain["rainx{0}".format(x)], rain["rainy{0}".format(x)]
            dx, dy = rain["destx{0}".format(x)], rain["desty{0}".format(x)]
            dist = math.sqrt(math.pow(dx - rx, 2) + math.pow(dy - ry, 2))

            if dist != 0:
                rain["rainx{0}".format(x)] += rSpeed*(dx - rx)/dist
                rain["rainy{0}".format(x)] += rSpeed*(dy - ry)/dist
            
            rx, ry = rain["rainx{0}".format(x)], rain["rainy{0}".format(x)]
            
            fx = rx + (dx - rx)/3
            fy = ry + (dy - ry)/3
            pygame.draw.line(screen, [200,200,200], (rx, ry), (fx,fy), int(3*h/40 - 2*math.sqrt(math.pow(xSize/2 - rx, 2) + math.pow(ySize/2 - ry, 2))/xSize))
            
            if h <= 0:
                rain["height{0}".format(x)] = 40
                rain["rainx{0}".format(x)] = randint(0,xSize + 200) - 100
                rain["rainy{0}".format(x)] = randint(0,ySize + 200) - 100
                rain["destx{0}".format(x)] = (xSize/2 - rain["rainx{0}".format(x)])/2 + rain["rainx{0}".format(x)]
                rain["desty{0}".format(x)] = (ySize/2 - rain["rainy{0}".format(x)])/2 + rain["rainy{0}".format(x)]
        elif randint(0,100) == 1:
            rain["alive{0}".format(x)] = True

        
    pygame.display.flip()
 
    clock.tick(30)
#----------------------Text Loop----------------------#
if not dead:
    done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            done = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            
    screen.fill([0,0,0])
    font1 = pygame.font.SysFont("dotum", 40)
    font2 = pygame.font.SysFont("dotum", 25)
    label1 = font1.render("Oh look, it's Zombie Hitler!", 1, (255,255,255))
    label2 = font2.render("(Click to Continue)", 1, (255,255,255))
    screen.blit(label1, (xSize/6,ySize/3))
    screen.blit(label2, (xSize/6,ySize/3 + 36))
    
    pygame.display.flip()

frameCount = 0

#-----------------------Hitler Zombie Loop-----------------------#

if not dead:
    done = False

side = random.randint(0,3)
if side == 0:
    hitx = -30
    hity = random.randint(0,ySize)
elif side == 1:
    hitx = random.randint(0,xSize)
    hity = -30
elif side == 2:
    hitx = xSize + 30
    hity = random.randint(0,ySize)
elif side == 3:
    hitx = random.randint(0,xSize)
    hity = ySize + 30
hitpx = 0
hitpy = 0
hitMove = True
hitHealth = 200

pygame.mouse.set_visible(True)
repeat = False
mouseHold = False
hit = False
SGFiring = False
paused = False
deadCheck = False
killHit = False
frameCount = 0
doneFrame = 0

while not done:
    frameCount += 1
    
    if hitHealth >= 12:
        hitSpeed = 1.5*math.pow(hitHealth/10-1,1/6)
    else:
        hitSpeed = 0.095*hitHealth
        
    mx, my = pygame.mouse.get_pos()
    
    keys = pygame.key.get_pressed()
    fired = False

    if weapon == 2:
        currentAmmo = pistAmmo
        gifC = 6
    elif weapon == 3:
        currentAmmo = shotAmmo
        gifC = 4
    elif weapon == 4:
        currentAmmo = miniAmmo
        gifC = 8
    else:
        currentAmmo = 0
        gifC = 0
    
    if shotCount > bulletLimit:
        timesOver += 1
        shotCount = 0

    #Keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if keys[pygame.K_ESCAPE]:
            if paused == False:
                paused = True
            else:
                paused = False
        if keys[pygame.K_1]:
            weapon = 1
            currentAmmo = 0
        if keys[pygame.K_2]:
            if hasPist == True:
                weapon = 2
                currentAmmo = pistAmmo
        if keys[pygame.K_3]:
            if hasShot == True:
                weapon = 3
                currentAmmo = shotAmmo
        if keys[pygame.K_4]:
            if hasMini == True:
                weapon = 4
                currentAmmo = miniAmmo
        if event.type == pygame.KEYDOWN:
            repeat = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            if shotDelay >= 10 and paused == False and (hasPist == True or hasShot == True) and weapon != 1 and currentAmmo > 0:
                shotDelay = 0
                if weapon == 2:
                    pistAmmo -= 1
                    pistol.play()
                    gifC = 7
                elif weapon == 3:
                    shotAmmo -= 1
                    shotgun.play()
                    gifC = 5
                mox, moy = pygame.mouse.get_pos()
                if mox != rect_x and moy != rect_y:
                    totalCount += 1
                    shotCount += 1
                    
                bd["posx{0}".format(shotCount-1)], bd["posy{0}".format(shotCount-1)] = pygame.mouse.get_pos()
                SGposx = bd["posx{0}".format(shotCount-1)]
                SGposy = bd["posy{0}".format(shotCount-1)]
                bd["recx{0}".format(shotCount-1)] = rect_x
                bd["recy{0}".format(shotCount-1)] = rect_y

                bd["bull_x{0}".format(shotCount-1)] = rect_x
                bd["bull_y{0}".format(shotCount-1)] = rect_y
                hit = False
                BULLET = (38, 38, 38)
                fired = True
            elif weapon == 1:
                swing = True
                
    screen.fill(BACK)

    prevx, prevy = rect_x, rect_y
    
    if repeat == True and paused == False:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if pan == False:
                rect_x -= pSpeed
            else:
                panx += pSpeed
                for x in range(1,cZombies):
                    zd["panx{0}".format(x)] += pSpeed
                rect_x = xSize/2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if pan == False:
                rect_x += pSpeed
            else:
                panx -= pSpeed
                for x in range(1,cZombies):
                    zd["panx{0}".format(x)] -= pSpeed
                rect_x = xSize/2
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if pan == False:
                rect_y -= pSpeed
            else:
                pany += pSpeed
                for x in range(1,cZombies):
                    zd["pany{0}".format(x)] += pSpeed
                rect_y = ySize/2
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if pan == False:
                rect_y += pSpeed
            else:
                pany -= pSpeed
                for x in range(1,cZombies):
                    zd["pany{0}".format(x)] -= pSpeed
                rect_y = ySize/2

    if rect_x != prevx and rect_y != prevy:
        if rect_x > prevx:
            rect_x = prevx
            rect_x += pSpeed/math.sqrt(2)
        else:
            rect_x = prevx
            rect_x -= pSpeed/math.sqrt(2)
            
        if rect_y > prevy:
            rect_y = prevy
            rect_y += pSpeed/math.sqrt(2)
        else:
            rect_y = prevy
            rect_y -= pSpeed/math.sqrt(2)

    #Background
    for y in range(0, int(ySize/backgSize) + 1):
        for x in range(0, int(xSize/backgSize + 1)):
            screen.blit(backg,(x*backgSize,y*backgSize))
    
    if hitMove == False:
        #hitler = pygame.draw.rect(screen, DEAD, [hitx-25 + hitpx, hity-25 + hitpy, 50, 50])
        #newHit = hitler.get_rect(center=(hitx,hity))
        #hitler = pygame.transform.scale(hitler, (100,100))
        screen.blit(hitler, newHit)
        #hitRect = pygame.Rect(hitx-40, hity-40, 80, 80)
    
    #Text
    scoreLabel = myFont.render("Score: " + str(hitCount), 1, (0,0,0))
    screen.blit(scoreLabel, (0, 0))
    ammoLabel = myFont.render("Ammo: " + str(currentAmmo), 1, (0,0,0))
    if weapon == 1:
        ammoLabel = myFont.render("Ammo: inf", 1, (0,0,0))
    screen.blit(ammoLabel, (0, ySize - 20))
    
    #Image
    #Axe
    axeX = rect_x
    axeY = rect_y

    ax2 = pygame.image.load(dir_path + "/Game Files/Images/Weapons/blank_img.bmp")
    if weapon == 1:
        axe = pygame.image.load(dir_path + "/Game Files/Images/Weapons/axe_100x88.bmp")
        axe = pygame.transform.scale(axe, (axeW,axeH))
        ax2 = pygame.transform.scale(ax2, (22,50))
        if weapon == 1 and swing == False and swingBack == False:
            mox, moy = pygame.mouse.get_pos()
            degs = getAngle(rect_x,rect_y,mox,moy)
            oldRec2 = ax2.get_rect(center=(axeX,axeY))
            ax2, newRec2 = rot_center(ax2,oldRec2,degs - 90,True)
            
            oldRect = axe.get_rect(center=(axeX,axeY))
            axe, newRect = rot_center(axe,oldRect,degs - 90,False)
            screen.blit(axe, newRect)
            
        axeRect = axe.get_rect()
        axeRect.x = axeX
        axeRect.y = axeY
        
        ax2Rect = ax2.get_rect()
        ax2Rect.x = axeX
        ax2Rect.y = axeY

    #Move Axe
    newRec2 = axe.get_rect(center=(axeX,axeY))
    if swing == True:
        if swingTick == 0:
            mox, moy = pygame.mouse.get_pos()
        swingTick += 1
        oldRect = axe.get_rect(center=(axeX,axeY))
        degs = getAngle(rect_x,rect_y,mox,moy)
        ax2, newRec2 = rot_center(ax2,oldRect,degs - 90 + swingTick*12, True)
        #screen.blit(ax2, newRec2)
        axe, newRect = rot_center(axe,oldRect,degs - 90 + swingTick*12, False)
        screen.blit(axe, newRect)
        if swingTick >= 20:
            swingBack = True
            swing = False
    elif swingBack == True:
        swingTick -= 1
        oldRect = axe.get_rect(center=(axeX,axeY))
        degs = getAngle(rect_x,rect_y,mox,moy)
        ax2, newRec2 = rot_center(ax2,oldRect,degs - 90 + swingTick*12, True)
        #screen.blit(ax2, newRec2)
        axe, newRect = rot_center(axe,oldRect,degs - 90 + swingTick*12, False)
        screen.blit(axe, newRect)
        if swingTick <= 0:
            swingTick = 0
            swingBack = False
            swing = False
    
    newerRect = newRec2
        
    #Move Bullets 
    if (weapon == 3 and fired == True) or SGFiring == True:
        SGCount += 1
        if SGCount <= int(SGPellets):
            SGFiring = True
            if shotDelay >= 0 and paused == False:
                shotDelay = 0
                mox, moy = pygame.mouse.get_pos()
                if mox != rect_x and moy != rect_y:
                    totalCount += 1
                    shotCount += 1
                if  SGCount == 0:
                    bd["posx{0}".format(shotCount-1)], bd["posy{0}".format(shotCount-1)] = pygame.mouse.get_pos()
                    SGposx = bd["posx{0}".format(shotCount-1)]
                    SGposy = bd["posy{0}".format(shotCount-1)]
                else:
                    bd["posx{0}".format(shotCount-1)] = SGposx + random.randint(0,30) - 15
                    bd["posy{0}".format(shotCount-1)] = SGposy + random.randint(0,30) - 15

                bd["recx{0}".format(shotCount-1)] = rect_x
                bd["recy{0}".format(shotCount-1)] = rect_y

                bd["bull_x{0}".format(shotCount-1)] = rect_x
                bd["bull_y{0}".format(shotCount-1)] = rect_y
                hit = False
                BULLET = (38, 38, 38)
                fired = True
        else:
            SGCount = 0
            SGFiring = False
        
    if weapon == 4 and mouseHold == True:
        if frameCount % 2 == 0:
            gifC = 8
        else:
            gifC = 9
        minigun.play()
        MGCount += 1
        if MGCount == int(MGRate):
            MGCount = 0
            if shotDelay >= 0 and paused == False:
                shotDelay = 0
                mox, moy = pygame.mouse.get_pos()
                if mox != rect_x and moy != rect_y:
                    totalCount += 1
                    shotCount += 1
                    
                bd["posx{0}".format(shotCount-1)], bd["posy{0}".format(shotCount-1)] = pygame.mouse.get_pos()

                bd["recx{0}".format(shotCount-1)] = rect_x
                bd["recy{0}".format(shotCount-1)] = rect_y

                bd["bull_x{0}".format(shotCount-1)] = rect_x
                bd["bull_y{0}".format(shotCount-1)] = rect_y
                hit = False
                BULLET = (38, 38, 38)
                fired = True

    #Person
    person = pygame.image.load(dir_path + "/Game Files/Images/Guy/top_guy_0{0}.bmp".format(gifC))
    person = pygame.transform.scale(person, (150,150))
    oldPerson = person.get_rect(center=(rect_x,rect_y))
    degs = getAngle(rect_x,rect_y,mx,my)
    person, newPerson = rot_center(person, oldPerson, degs - 90, False)
    screen.blit(person, newPerson)
    person = pygame.Rect(rect_x-15, rect_y-15, 30, 30)

    if totalCount <= bulletLimit:
        rang = totalCount
    else:
        rang = bulletLimit
    for i in range(rang):
        if i > bulletLimit:
            i -= bulletLimit*timesOver
        if weapon == 2:
            distance = math.sqrt(math.pow(bd["posx{0}".format(i)] - bd["recx{0}".format(i)], 2) + math.pow(bd["posy{0}".format(i)] - bd["recy{0}".format(i)], 2))
            if distance != 0 and paused == False:
                bd["bull_x{0}".format(i)] += bulletSpeed*(bd["posx{0}".format(i)] - bd["recx{0}".format(i)])/distance
                bd["bull_y{0}".format(i)] += bulletSpeed*(bd["posy{0}".format(i)] - bd["recy{0}".format(i)])/distance
                bd["bullet{0}".format(i)] = pygame.draw.rect(screen, BULLET, [bd["bull_x{0}".format(i)], bd["bull_y{0}".format(i)], 4, 4])
        elif weapon == 3:
            distance = math.sqrt(math.pow(bd["posx{0}".format(i)] - bd["recx{0}".format(i)], 2) + math.pow(bd["posy{0}".format(i)] - bd["recy{0}".format(i)], 2))
            if distance != 0 and paused == False:
                bd["bull_x{0}".format(i)] += bulletSpeed*(bd["posx{0}".format(i)] - bd["recx{0}".format(i)])/distance
                bd["bull_y{0}".format(i)] += bulletSpeed*(bd["posy{0}".format(i)] - bd["recy{0}".format(i)])/distance
                bd["bullet{0}".format(i)] = pygame.draw.rect(screen, BULLET, [bd["bull_x{0}".format(i)], bd["bull_y{0}".format(i)], 4, 4])
        elif weapon == 4:
            distance = math.sqrt(math.pow(bd["posx{0}".format(i)] - bd["recx{0}".format(i)], 2) + math.pow(bd["posy{0}".format(i)] - bd["recy{0}".format(i)], 2))
            if distance != 0 and paused == False:
                bd["bull_x{0}".format(i)] += bulletSpeed*(bd["posx{0}".format(i)] - bd["recx{0}".format(i)])/distance
                bd["bull_y{0}".format(i)] += bulletSpeed*(bd["posy{0}".format(i)] - bd["recy{0}".format(i)])/distance
                bd["bullet{0}".format(i)] = pygame.draw.rect(screen, BULLET, [bd["bull_x{0}".format(i)], bd["bull_y{0}".format(i)], 4, 4])

    hitGif = int(7-7/200*hitHealth)
    if hitGif == 5 or hitGif == 6:
        if int(frameCount/10) % 2 == 0:
            hitGif = 5
        else:
            hitGif = 6
    if hitMove == False:
        hitler = pygame.image.load(dir_path + "/Game Files/Images/Hitler/hitler_top_{0}.bmp".format(7))
        hitler = pygame.image.load(dir_path + "/Game Files/Images/Hitler/hitler_top_{0}.bmp".format(hitGif))
        hitler = pygame.transform.scale(hitler, (100,100))
        oldHit = hitler.get_rect(center=(hitx,hity))
        #degs = getAngle(hitx,hity, rect_x,rect_y)
        hitler, newHit = rot_center(hitler, oldHit, last - 90, False)
        #screen.blit(hitler, newHit)
    
    #Create / Move Hitler
    if hitMove == True:
        #hitler = pygame.draw.rect(screen, ZOMBIE, [hitx-25 + hitpx, hity-25 + hitpy, 50, 50])
        
        hitler = pygame.image.load(dir_path + "/Game Files/Images/Hitler/hitler_top_{0}.bmp".format(hitGif))
        hitler = pygame.transform.scale(hitler, (100,100))
        oldHit = hitler.get_rect(center=(hitx,hity))
        degs = getAngle(hitx,hity, rect_x,rect_y)
        last = degs
        hitler, newHit = rot_center(hitler, oldHit, degs - 90, False)
        screen.blit(hitler, newHit)
        hitRect = pygame.Rect(hitx-40, hity-40, 80, 80)
            
    if pan == False:
        distx = hitSpeed*(rect_x - hitx - hitpx)/math.sqrt(math.pow(rect_x - hitx - hitpx, 2) + math.pow(rect_y - hity - hitpy, 2))
        disty = hitSpeed*(rect_y - hity - hitpy)/math.sqrt(math.pow(rect_x - hitx - hitpx, 2) + math.pow(rect_y - hity - hitpy, 2))
    else: 
        distx = hitSpeed*(xSize/2 - hitx - hitpx)/math.sqrt(math.pow(xSize/2 - hitx - hitpx, 2) + math.pow(ySize/2 - hity - hitpy, 2))
        disty = hitSpeed*(ySize/2 - hity - hitpy)/math.sqrt(math.pow(xSize/2 - hitx - hitpx, 2) + math.pow(ySize/2 - hity - hitpy, 2))

    #Health Bar
    redSide = pygame.draw.rect(screen, [255,0,0], [hitx-25, hity-50 + hitpy, 50, 5])
    if hitHealth != 0:
        greenSide = pygame.draw.rect(screen, [0,255,0], [hitx-25, hity-50 + hitpy, hitHealth/4, 5])

    if hitMove == True and paused == False:
        hitx += distx
        hity += disty
            
    #Check Axe Hit
    if newRec2.colliderect(hitRect) == True and swing == True:
        hitHealth -= 1

    #Check Bullet Hit
    for i in range(rang):
        if i > bulletLimit:
            i -= bulletLimit*timesOver
        if distance != 0 and hit == False and paused == False:
            if hit == False and bd["bullet{0}".format(i)].colliderect(hitRect) == True:
                hitHealth -= 1
                bd["bull_x{0}".format(i)] = -10000
                bd["bull_y{0}".format(i)] = -10000
                hitDelay = 0
                hitCount += 1
                bd["recx{0}".format(i)] = rect_x
                bd["recy{0}".format(i)] = rect_y
                side = random.randint(0,3)
                
    if dead == False and person.colliderect(hitRect) == True:
        dead = True
        done = True
        print("eaten")

    if killHit == False and hitHealth <= 0:
        hitMove = False
        doneFrame = frameCount
        killHit = True
        
    if hitHealth < 0:
        hitHealth = 0
        
    if killHit == True and frameCount - doneFrame > 100:
        done = True

    shotDelay += 1

    if paused == True:
        BACK = (217, 217, 217)
    else:
        BACK = (255, 255, 255)

    #Light
    dark = 170
    r = frameCount % bound
    if 0 <= r < 10 or 25 <= r < 35:
        dark = 0
    elif r == 35:
        bound = randint(1000,2000)
        lightning.play()

    s = pygame.Surface((xSize,ySize))
    s.set_alpha(dark)
    s.fill((0,0,0))
    screen.blit(s, (0,0))

    #Rain
    for x in range(1,rains):
        if rain["alive{0}".format(x)] == True:
            rain["height{0}".format(x)] -= 1
            h = rain["height{0}".format(x)]
            rx, ry = rain["rainx{0}".format(x)], rain["rainy{0}".format(x)]
            dx, dy = rain["destx{0}".format(x)], rain["desty{0}".format(x)]
            dist = math.sqrt(math.pow(dx - rx, 2) + math.pow(dy - ry, 2))

            if dist != 0:
                rain["rainx{0}".format(x)] += rSpeed*(dx - rx)/dist
                rain["rainy{0}".format(x)] += rSpeed*(dy - ry)/dist
            
            rx, ry = rain["rainx{0}".format(x)], rain["rainy{0}".format(x)]
            
            fx = rx + (dx - rx)/3
            fy = ry + (dy - ry)/3
            pygame.draw.line(screen, [200,200,200], (rx, ry), (fx,fy), int(3*h/40))
            
            if h <= 0:
                rain["height{0}".format(x)] = 40
                rain["rainx{0}".format(x)] = randint(0,xSize + 200) - 100
                rain["rainy{0}".format(x)] = randint(0,ySize + 200) - 100
                rain["destx{0}".format(x)] = (xSize/2 - rain["rainx{0}".format(x)])/4 + rain["rainx{0}".format(x)]
                rain["desty{0}".format(x)] = (ySize/2 - rain["rainy{0}".format(x)])/4 + rain["rainy{0}".format(x)]
        elif randint(0,100) == 1:
            rain["alive{0}".format(x)] = True
        
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

if not dead:
    roll_text("Mission complete.")
    time.sleep(1)
    print("")
    print("")
    if binRead == "1":
        print("-----------------------------Brief Closed-----------------------------")
        print("")
    roll_text("(Press enter when ready)")
    input("")
    print("")
    print("")
    exec(open(dir_path + "/Game Files/Missions/Cut_Scene_1.py").read(), globals())
else:
    roll_text("You died.")
    time.sleep(1)
    roll_text(" Mission failed.")
    time.sleep(1)
    print("")
    print("")
    if binRead == "1":
        print("-----------------------------Brief Closed-----------------------------")
        print("")
