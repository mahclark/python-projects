import pygame
import math

clock = pygame.time.Clock()
pygame.init()

#Colours
BACK = (255, 255, 255)
DARK = (129,79,47)
KDARK = (108,65,32)
VDARK = (75,46,21)
LIGHT = (175,111,70)
LRED = (208,42,34)
DRED = (129,18,5)
WHITE = (237,232,237)

#Screen
xSize = 500
ySize= 450
Size = 450
size = [xSize, ySize]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Doom_Imp")

y = 0
vari = 7
length = 20
count = 0
down = False

done = False
while not done:
    screen.fill(BACK)

    #Shoulders
    shoulder1 = pygame.draw.rect(screen, DARK, [190, 100-y/5, 120, 30+y/5])
    shoulder2 = pygame.draw.rect(screen, DARK, [170, 110-y/5, 160, 30+y/5])
    shoulder3 = pygame.draw.rect(screen, DARK, [150, 125-y/5, 200, 80+y/5])
    jawShadow1 = pygame.draw.rect(screen, KDARK, [165, 130, 170, 40])
    jawShadow2 = pygame.draw.rect(screen, KDARK, [190, 100-y/5, 120, 100+y/3+y/5])
    jawShadow3 = pygame.draw.rect(screen, VDARK, [180, 140, 140, 20])
    jawShadow4 = pygame.draw.rect(screen, VDARK, [200, 120+y/3, 100, 60])
    jawShadow5 = pygame.draw.rect(screen, VDARK, [210, 120+y/3, 80, 70])

    #Head
    backHead = pygame.draw.rect(screen, DARK, [190, 50, 120, 30])
    backHeadTop1 = pygame.draw.rect(screen, KDARK, [200, 30, 100, 20])
    backHeadTop2 = pygame.draw.rect(screen, DARK, [210, 20, 80, 50])
    backHeadTop3 = pygame.draw.rect(screen, KDARK, [223, 13, 54, 10])
    browShadow1 = pygame.draw.rect(screen, VDARK, [210, 60, 80, 15])
    browShadow2 = pygame.draw.rect(screen, VDARK, [225, 60, 50, 18])
    foreheadShadow = pygame.draw.rect(screen, KDARK, [235, 45, 30, 10])
    midBrow = pygame.draw.rect(screen, LIGHT, [225, 59-y/10, 50, 10])
    leftBrow = pygame.draw.rect(screen, LIGHT, [205, 55-y/10, 30, 10])
    rightBrow = pygame.draw.rect(screen, LIGHT, [265, 55-y/10, 30, 10])

    #Jaw
    bottomJaw = pygame.draw.rect(screen, DARK, [213, 80, 74, 95+y])
    backJaw1 = pygame.draw.rect(screen, DARK, [208, 80, 84, 80+y])
    backJaw2 = pygame.draw.rect(screen, DARK, [200, 80, 100, 40])
    mouthShadow1 = pygame.draw.rect(screen, VDARK, [220, 100, 60, 40+y])
    mouthShadow2 = pygame.draw.rect(screen, KDARK, [220, 110, 60, 40+y])
    leftMouth = pygame.draw.rect(screen, LIGHT, [217, 95, 7, 55+y])
    rightMouth = pygame.draw.rect(screen, LIGHT, [276, 95, 7, 55+y])
    tongue = pygame.draw.rect(screen, LRED, [230, 110, 40, 40+y])
    backTongue = pygame.draw.rect(screen, DRED, [240, 110, 20, 20+y/2])
    upperTeeth = pygame.draw.rect(screen, WHITE, [230, 100, 40, 10])
    lowerTeeth = pygame.draw.rect(screen, WHITE, [230, 150+y, 40, 10])
    noseShadow = pygame.draw.rect(screen, KDARK, [230, 78, 40, 22])
    nose = pygame.draw.rect(screen, DARK, [240, 90, 20, 10])

    #Eyes
    leftEyeShadow = pygame.draw.rect(screen, VDARK, [215, 70, 25, 15])
    leftEyeBack = pygame.draw.rect(screen, DRED, [215, 70, 15, 15])
    leftEye = pygame.draw.rect(screen, LRED, [220, 70, 10, 10])
    rightEyeShadow = pygame.draw.rect(screen, VDARK, [260, 70, 25, 15])
    rightEyeBack = pygame.draw.rect(screen, DRED, [270, 70, 15, 15])
    rightEye = pygame.draw.rect(screen, LRED, [270, 70, 10, 10])

    #Text
    myFont = pygame.font.SysFont("monospace", 15)
    label = myFont.render("Inspired by the Doom monster: ", 1, (0,0,0))
    screen.blit(label, (70,240))
    fps = int(clock.get_fps())
    fpsLabel = myFont.render(str(fps), 1, (0,0,0))
    screen.blit(fpsLabel, (0,420))

    dot = pygame.draw.rect(screen, LRED, [370, 150+y*10, 10, 10])
    #Image
    img = pygame.image.load("doom_imp.bmp")
    img = pygame.transform.scale(img, (100,140))
    screen.blit(img,(220, 260))
    
    count += 1
    y = vari*math.sin(count/length)-4
    #print(pygame.display.get_active())
    #if int(y*1000) == -10999:
        #print(count)
    #print(y)
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
