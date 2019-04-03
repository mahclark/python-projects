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

bsaved = dir_path.encode(encoding='UTF-8')
newFile = open(dir_path + "/Game Files/Saves/path.txt", "wb")
newFile.write(bsaved)
newFile = open(dir_path + "/Game Files/Saves/path.txt", "rb")

try:
    newFile = open(dir_path + "/Game Files/Saves/lock.txt", "rb")
    txtRead = newFile.read().decode(encoding='UTF-8')
except:
    txtRead = "failed"
    
chp1 = txtRead[0]
chp2 = txtRead[1]
chp3 = txtRead[2]


if 'idlelib.run' in sys.modules:
    print("Run in CMD for optimised experience.")
    print("")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

setWindowPos = windll.user32.SetWindowPos
setWindowPos(pygame.display.get_wm_info()['window'], -1, 400, 300, 0, 0, 0x0001)

#Screen
infoObject = pygame.display.Info()
scrW, scrH = infoObject.current_w, infoObject.current_h
xShift = scrW/2 - 300
yShift = scrH/2 - 225
xSize, ySize = scrW, scrH
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Mission_")

mx, my = pygame.mouse.get_pos()
mouseHold = False
text1 = "Play Game"
text2 = "Chapter Select"
text3 = "Settings"
text4 = "Quit"

#----------------------Main Loop----------------------#

pix = 13
click = False
chapter = 0
select = False
sett = False
leave = False

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    click = False
    frameCount += 1
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            click = True

    for xp in  range(int(xSize/pix + 1)):
        xp = xp*pix
        for yp in range(int(ySize/pix + 1)):
            yp = yp*pix
            if randint(0,200) == 0:
                col = [randint(20, 80), 0, 0]
                pygame.draw.rect(screen, col, (xp,yp,pix,pix))
                
    if not (select and chp1 != "1"):
        lab1 = (200,200,200)
    else:
        lab1 = (100,100,100)
    if not (select and chp2 != "1"):
        lab2 = (200,200,200)
    else:
        lab2 = (100,100,100)
    if not (select and chp3 != "1"):
        lab3 = (200,200,200)
    else:
        lab3 = (100,100,100)
    lab4 = (200,200,200)
    
    if 250 < mx < 650:

        label_text1 = ["Amazing", "Beautiful", "Magnificent"]
        label_text2 = ["Outstanding", "Perfect", "Exquisite"]
        label_text3 = ["100%", "Full", "Maximum"]

        #Label 1
        if 200 < my < 300:
            if not (select and chp1 != "1"):
                lab1 = (222,50,50)
            if click == True and select == False and not sett:
                done = True
            elif click == True and chp1 == "1" and not sett:
                chapter = 1
                done = True
            elif click == True and sett:
                rand_text = label_text1[randint(0,len(label_text1)-1)]
                while text1 == "Graphics: " + rand_text:
                    rand_text = label_text1[randint(0,len(label_text1)-1)] 
                text1 = "Graphics: " + rand_text
                screen.fill([0,0,0])

        #Label 2
        if 300 < my < 400:
            if not (select and chp2 != "1"):
                lab2 = (222,50,50)
            if click == True and select == False and not sett:
                if chp1 == "1":
                    text1 = "Reign of Hitler"
                else:
                    text1 = "Locked"
                if chp2 == "1":
                    text2 = "Zombie Apocalypse"
                else:
                    text2 = "Locked"
                if chp3 == "1":
                    text3 = "Demonic Uprising"
                else:
                    text3 = "Locked"
                text4 = "Back"
                screen.fill([0,0,0])
                select = True
            elif click == True and chp2 == "1" and not sett:
                chapter = 2
                done = True
            elif click == True and sett:
                rand_text = label_text2[randint(0,len(label_text2)-1)]
                while text2 == "Gameplay: " + rand_text:
                    rand_text = label_text2[randint(0,len(label_text2)-1)] 
                text2 = "Gameplay: " + rand_text
                screen.fill([0,0,0])

        #Label 3
        if 400 < my < 500:
            if not (select and chp3 != "1"):
                lab3 = (222,50,50)
            if click == True and select == True and not sett and chp3 == "1":
                chapter = 3
                done = True
            if click and not select and not sett:
                text1 = "Graphics: Amazing"
                text2 = "Gameplay: Perfect"
                text3 = "General Awesomeness: 100%"
                text4 = "Back"
                screen.fill([0,0,0])
                sett = True
            elif click == True and sett:
                rand_text = label_text3[randint(0,len(label_text3)-1)]
                while text3 == "General Awesomeness: " + rand_text:
                    rand_text = label_text3[randint(0,len(label_text3)-1)] 
                text3 = "General Awesomeness: " + rand_text
                screen.fill([0,0,0])
                

        #Label 4
        if 500 < my < 600:
            lab4 = (222,50,50)
            if click == True and (select or sett):
                text1 = "Play Game"
                text2 = "Chapter Select"
                text3 = "Settings"
                text4 = "Quit"
                screen.fill([0,0,0])
                select = False
                sett = False
            elif click == True:
                done = True
                leave = True
    
    font = pygame.font.SysFont("agencyfb",80)#agency fb", 80)
    label1 = font.render(text1, 1, lab1)
    label2 = font.render(text2, 1, lab2)
    label3 = font.render(text3, 1, lab3)
    label4 = font.render(text4, 1, lab4)
    screen.blit(label1, (250,200))
    screen.blit(label2, (250,300))
    screen.blit(label3, (250,400))
    screen.blit(label4, (250,500))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
if chapter == 1 or (chapter == 0 and not leave):
    exec(open(dir_path + "/Game Files/Missions/Mission_1.py").read(), globals())
elif chapter == 2:
    exec(open(dir_path + "/Game Files/Missions/News_Flash.py").read(), globals())
elif chapter == 3:
    exec(open(dir_path + "/Game Files/Missions/Cut_Scene_1.py").read(), globals())
