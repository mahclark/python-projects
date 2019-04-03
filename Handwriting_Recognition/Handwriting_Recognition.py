import pygame
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 600, 450
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pygame Template")

#Variables
box = 100
learnt = ["1","2","3","h","e","l","o","あ","い","う","え","お","食","意"]
w_char = "2"
bit = {}
num = {}
trySum = {}
acc = {}
for item in learnt:
    bit["{0}".format(item)] = []
    num["{0}".format(item)] = 0
    acc["{0}".format(item)] = 0
    trySum["{0}".format(item)] = 0

    try:
        with open(dir_path + "/heatmaps/{0}bit".format(item), 'r') as f:
            load = [line.rstrip('\n') for line in f]
        
        for i in load:
            bit["{0}".format(item)].append(int(i))

        with open(dir_path + "/heatmaps/{0}bit_num".format(item), 'r') as f:
            num_load = [line.rstrip('\n') for line in f]
            num["{0}".format(item)] = int(num_load[0])

        
    except:
        print("failed to load ", item)
        for i in range(box-1):
            for i in range(box-1):
                bit["{0}".format(item)].append(0)
                num["{0}".format(item)] = 1

#Setup graphics
def setup() :
    screen.fill([255,255,255])
    mx, my = pygame.mouse.get_pos()
    px, py = mx, my
    pygame.draw.lines(screen, [0,0,0], True, [(0,0),(box,0),(box,box),(0,box)])
setup()

#----------------------Main Loop----------------------#

clock = pygame.time.Clock()
frameCount = 0
done = False
mouseHold = False

while not done:
    mouseClick = False
    mouseUp = False
    mx, my = pygame.mouse.get_pos()
    frameCount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True
            mouseClick = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False
            mouseUp = True
            
    #Drawing
    if mouseHold and mx < box and my < box and px < box and py < box:
        pygame.draw.line(screen, [0,0,0], (mx,my), (px,py), 6)
    elif mouseHold and (px < box and py < box) and (mx > box or my > box):
        if mx > box:
            mx = box
        if my > box:
            my = box
        pygame.draw.line(screen, [0,0,0], (mx,my), (px,py), 6)
    elif mouseHold and (mx < box and my < box) and (px > box or py > box):
        if px > box:
            px = box
        if py > box:
            py = box
        pygame.draw.line(screen, [0,0,0], (mx,my), (px,py), 6)
    px, py = mx, my

    #Green
    if mouseClick and my > 150 and my < 280 and mx > 10 and mx < 40:
        num["{0}".format(w_char)] += 1
        pygame.draw.rect(screen, [20,150,20], (10, 150, 30, 30))
        for y in range(box-1):
            for x in range(box-1):
                if screen.get_at((x+1,y+1)) == (0,0,0):
                    bit["{0}".format(w_char)][y*(box-1)+x] += 1

        with open(dir_path + "/heatmaps/{0}bit".format(w_char), 'w') as f:
            for s in bit["{0}".format(w_char)]:
                f.write(str(s) + '\n')
                
        with open(dir_path + "/heatmaps/{0}bit_num".format(w_char), 'w') as f:
            f.write(str(num["{0}".format(w_char)]) + '\n')
        
        setup()
        high = max(bit["{0}".format(w_char)])
        if high == 0:
            high = 1
            
        for y in range(box-1):
            for x in range(box-1):
                screen.set_at((x+box+1,y+1),[255*bit["{0}".format(w_char)][y*(box-1)+x]/high,0,0])
                    
        pygame.draw.rect(screen, [20,150,20], (10, 150, 30, 30))
    else:
        pygame.draw.rect(screen, [20,200,20], (10, 150, 30, 30))

    #Blue
    if (mouseClick and my > 150 and my < 280 and mx > 50 and mx < 80):# or (mouseUp and mx < box and my < box):
        pygame.draw.rect(screen, [20,20,150], (50, 150, 30, 30))
        tryNum = 0
        for item in learnt:
            trySum["{0}".format(item)] = 0
        
        for y in range(box-1):
            for x in range(box-1):
                if screen.get_at((x+1,y+1)) == (0,0,0):
                    tryNum += 1
                    for item in learnt:
                        trySum["{0}".format(item)] += bit["{0}".format(item)][y*(box-1)+x]/num["{0}".format(item)]

        avgNum = {}
        for item in learnt:
            avgNum["{0}".format(item)] = sum(i for i in bit["{0}".format(item)])/num["{0}".format(item)] #Average number of pixels coloured
            acc["{0}".format(item)] = 50*trySum["{0}".format(item)]/tryNum + 50*max(0,(avgNum["{0}".format(item)] - abs(tryNum - avgNum["{0}".format(item)]))/avgNum["{0}".format(item)])

        perM = max(acc, key=lambda i: acc[i])
        print(perM)#,tryNum,avgNum["{0}".format(perM)],int(100*trySum["{0}".format(perM)]/tryNum), int(100*max(0,(avgNum["{0}".format(perM)] - abs(tryNum - avgNum["{0}".format(perM)]))/avgNum["{0}".format(perM)])), int(acc["{0}".format(perM)]))
                    
        pygame.draw.rect(screen, [20,20,150], (50, 150, 30, 30))
    else:
        pygame.draw.rect(screen, [20,20,200], (50, 150, 30, 30))

    #Red
    if mouseClick and my > 150 and my < 280 and mx > 90 and mx < 120:
        pygame.draw.rect(screen, [255,255,255], (1, 1, box-1, box-1))
        pygame.draw.rect(screen, [150,20,20], (90, 150, 30, 30))
    else:
        pygame.draw.rect(screen, [200,20,20], (90, 150, 30, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
