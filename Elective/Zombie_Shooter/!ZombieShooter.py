import pygame
import math
import random
from math import atan2, degrees, pi

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

##byteArray = [1,0,1,1,1,0]
##newByteArray = bytearray(byteArray)
##newFile = open("binaryFile", "wb")
##newFile.write(newByteArray)
##newFile = open("binaryFile", "rb")
##print(newFile.read(0))
##print(newFile.read(1))
##print(newFile.read(2))
##print(newFile.read(3))
##print(newFile.read(4))
##print(newFile.read(1))
##print(newFile.read(2))


# Variables
BLACK = (0, 0, 0)
BACK = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FLESH = (255, 217, 179)
ZOMBIE = (30, 123, 123)
DEAD = (138,7,7)
BULLET = (38, 38, 38)

pSpeed = 2
zSpeed = 1
infZom = False

#Settings
zError = True
while zError:
    print("How many zombies would you like?")
    nZombies = input("")
    zError = False
    if nZombies.lower() == "inf":
        infZom = True
    else:
        try:
            nZombies = int(nZombies)
        except ValueError:
            zError = True
            print("error")

antiAns = ""
while antiAns.lower() != "on" and antiAns != "off":
    print("Would you like axe anti aliasing on or off?")
    antiAns = input("")
    if antiAns.lower() == "on":
        antiA = True
    else:
        antiA = False

orbitAns = ""
while orbitAns.lower() != "yes" and orbitAns != "no":
    print("Would you like zombie orbiting?")
    orbitAns = input("")
    if orbitAns.lower() == "yes":
        zOrbit = True
    else:
        zOrbit = False

panAns = ""
while panAns.lower() != "yes" and panAns != "no":
    print("Would you like camera panning?")
    panAns = input("")
    if panAns.lower() == "yes":
        pan = True
    else:
        pan = False

cZombies = 0
waves = 2
weapon = 1

pygame.init()

xSize = 1200
ySize = 800
size = (xSize, ySize)
screen = pygame.display.set_mode(size)

myFont = pygame.font.SysFont("monospace", 15)

rect_x = xSize/2
rect_y = ySize/2
hitDelay = 120
shotDelay = 0
bulletLimit = 100
bulletSpeed = 20
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
hasShot = False
hasMini = False
pistAmmo = 0
shotAmmo = 0
miniAmmo = 0
currentAmmo = 0
pistDropped = True
shotDropped = True
miniDropped = True
swing = False
swingBack = False
panx = 0
pany = 0

backgSize = 350
backg = pygame.image.load("brick_back.bmp")
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

bd["bull_x{0}".format(shotCount)] = -4
bd["bull_y{0}".format(shotCount)] = -4
bd["recx{0}".format(shotCount)] = rect_x
bd["recy{0}".format(shotCount)] = rect_y
bd["posx{0}".format(shotCount)] = xSize/2-2
bd["posy{0}".format(shotCount)] = ySize/2-2
 
pygame.display.set_caption("Zombie Shooter")
done = False
clock = pygame.time.Clock()

# -------- Main Loop -----------
repeat = False
mouseHold = False
hit = False
dead = False
SGFiring = False
paused = False

while not done:
    keys = pygame.key.get_pressed()
    fired = False

    if weapon == 2:
        currentAmmo = pistAmmo
    elif weapon == 3:
        currentAmmo = shotAmmo
    elif weapon == 4:
        currentAmmo = miniAmmo
    else:
        currentAmmo = 0
    
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
                elif weapon == 3:
                    shotAmmo -= 1
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
            
    #Background
##    for y in range(0, int(ySize/backgSize) + 1):
##        for x in range(0, int(xSize/backgSize + 1)):
##            screen.blit(backg,(x*backgSize,y*backgSize))

    for x in range(1,cZombies):
        if zd["moveBack{0}".format(x)] == True:
            zd["zombie{0}".format(x)] = pygame.draw.rect(screen, DEAD, [randd["randx{0}".format(x)]-15 + panx, randd["randy{0}".format(x)]-15 + pany, 30, 30])
    
    #Text
    scoreLabel = myFont.render("Score: " + str(hitCount), 1, (0,0,0))
    screen.blit(scoreLabel, (0, 0))
    ammoLabel = myFont.render("Ammo: " + str(currentAmmo), 1, (0,0,0))
    if weapon == 1:
        ammoLabel = myFont.render("Ammo: inf", 1, (0,0,0))
    screen.blit(ammoLabel, (0, 780))
    
    #Image
    #Axe
    axeX = rect_x
    axeY = rect_y

    ax2 = pygame.image.load("blank_img.bmp")
    if weapon == 1:
        axe = pygame.image.load("axe_100x88.bmp")
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
    pist = pygame.image.load("pistol_30x30.bmp")
    pist = pygame.transform.scale(pist, (pistW,pistH))
    pistRect = pist.get_rect()
    if pistDropped == True:# and hasPist == False:
        screen.blit(pist,(pistX + panx, pistY + pany))
    pistRect.x = pistX + panx
    pistRect.y = pistY + pany

    #Shotgun
    shot = pygame.image.load("shotgun_30x30.bmp")
    shot = pygame.transform.scale(shot, (shotW,shotH))
    shotRect = shot.get_rect()
    if shotDropped == True:# and hasShot == False:
        screen.blit(shot,(shotX + panx, shotY + pany))
    shotRect.x = shotX + panx
    shotRect.y = shotY + pany

    #Minigun
    mini = pygame.image.load("mini_30x30.bmp")
    mini = pygame.transform.scale(mini, (miniW,miniH))
    miniRect = mini.get_rect()
    if miniDropped == True:
        screen.blit(mini,(miniX + panx, miniY + pany))
    miniRect.x = miniX + panx
    miniRect.y = miniY + pany

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
                
    person = pygame.draw.rect(screen, FLESH, [rect_x-15, rect_y-15, 30, 30])

    #Check Weapon Pickup
    if person.colliderect(pistRect) == True:# and hasPist == False:
        pistW = 0
        pistH = 0
        swing = False
        swingback = False
        #pistDropped = False
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
        if cZombies != 1:
            print(cZombies-1)
    for x in range(1,cZombies):
        if zd["moveBack{0}".format(x)] == False:
            czDead = False
            zd["zombie{0}".format(x)] = pygame.draw.rect(screen, ZOMBIE, [randd["randx{0}".format(x)]-15 + zd["panx{0}".format(x)], randd["randy{0}".format(x)]-15 + zd["pany{0}".format(x)], 30, 30])
        else:
            czDead = True
        if pan == False or zd["moveBack{0}".format(x)] == False or 1 ==1:
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
                
            if zd["speedBack{0}".format(x)] > 0:
                if zOrbit == False or zd["axed{0}".format(x)] == False:
                    zd["speedBack{0}".format(x)] -= 8
                else:
                    zd["speedBack{0}".format(x)] = 30
            else:
                zd["speedBack{0}".format(x)] = 0
            
        #Check if Zombies Hit
        #Check Axe Hit
        if newRec2.colliderect(zd["zombie{0}".format(x)]) == True and swing == True and czDead == False:
            side = random.randint(0,3)
            hitCount += 1
            #Drop Weapons
            if random.randrange(1,2) == 1 and pistDropped == False:
                pistX = randd["randx{0}".format(x)]
                pistY = randd["randy{0}".format(x)]
                screen.blit(pist,(pistX, pistY))
                pistDropped = True
            elif random.randrange(1,2) == 1:# and shotDropped == False:
                shotX = randd["randx{0}".format(x)]
                shotY = randd["randy{0}".format(x)]
                screen.blit(shot,(shotX, shotY))
                shotDropped = True
            elif random.randrange(1,50) == 1 and miniDropped == False:
                miniX = randd["randx{0}".format(x)]
                miniY = randd["randy{0}".format(x)]
                screen.blit(mini,(miniX, miniY))
                miniDropped = True
            zd["moveBack{0}".format(x)] = True
            zd["speedBack{0}".format(x)] = 45
            zd["axed{0}".format(x)] = True
##            randd["randx{0}".format(x)] = -300
##            randd["randy{0}".format(x)] = -300
##            zd["canMove{0}".format(x)] = True

        #Check Bullet Hit
        for i in range(rang):
            if i > bulletLimit:
                i -= bulletLimit*timesOver
            if distance != 0 and hit == False and paused == False and czDead == False:
                if hit == False and bd["bullet{0}".format(i)].colliderect(zd["zombie{0}".format(x)]) == True:
                    #hit = True
                    bd["bull_x{0}".format(i)] = -10000
                    bd["bull_y{0}".format(i)] = -10000
                    hitDelay = 0
                    hitCount += 1
                    bd["recx{0}".format(i)] = rect_x
                    bd["recy{0}".format(i)] = rect_y
                    side = random.randint(0,3)
                    #Drop Weapons
                    if 1==1:#random.randrange(1,2) == 1 and pistDropped == False:
                        pistX = randd["randx{0}".format(x)]
                        pistY = randd["randy{0}".format(x)]
                        screen.blit(pist,(pistX, pistY))
                        pistDropped = True
                    elif random.randrange(1,2) == 1 and shotDropped == False:
                        shotX = randd["randx{0}".format(x)]
                        shotY = randd["randy{0}".format(x)]
                        screen.blit(shot,(shotX, shotY))
                        shotDropped = True
                    elif random.randrange(1,50) == 1 and miniDropped == False:
                        miniX = randd["randx{0}".format(x)]
                        miniY = randd["randy{0}".format(x)]
                        screen.blit(mini,(miniX, miniY))
                        miniDropped = True
                    zd["moveBack{0}".format(x)] = True
                    zd["speedBack{0}".format(x)] = 50
                    zd["axed{0}".format(x)] = False
##                    randd["randx{0}".format(x)] = -300
##                    randd["randy{0}".format(x)] = -300
##                    zd["canMove{0}".format(x)] = False
                
        if dead == False and zd["moveBack{0}".format(x)] == False and person.colliderect(zd["zombie{0}".format(x)]) == True:
            dead = True
            done = True
            print("eaten")
    

    shotDelay += 1

    if paused == True:
        BACK = (217, 217, 217)
    else:
        BACK = (255, 255, 255)
        
    pygame.display.flip()
 
    clock.tick(60)
# ------------------ End Main Loop -------------------------------

pygame.quit()
