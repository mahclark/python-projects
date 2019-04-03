import pygame
import time
from math import radians, sin, cos, tan, sqrt

pygame.init()

xSize, ySize = 1600, 800
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("3D Graphics")

depth = 1000 #distance between thoertical screen and eye (changes fov)

ry = -30 #rotation about y axis
rx = 0 #rotation about x axis

class c: x, y, z = 50,80,-50 #camera coordinates

px, pz = 0,0
vv = 0
centre = 0

def get_2d(x, y, z): #Algorithm to convert 3D coordinates into 2D screen coordinates
    x -= c.x
    y -= c.y
    z -= c.z

    oldx = x
    oldy = y
    
    #turning camera
    x = x*cos(radians(rx)) - z*sin(radians(rx))
    z = z*cos(radians(rx)) + oldx*sin(radians(rx))

    y = y*cos(radians(ry)) - z*sin(radians(ry))
    z = z*cos(radians(ry)) + oldy*sin(radians(ry))

    z -= depth

    class e: x, y, z = 0,0,-depth #eye coordinates
    
    try: x = x + (0 - z)*(x - e.x)/(z - e.z)
    except: x = c.x
    try: y = y + (0 - z)*(y - e.y)/(z - e.z)
    except: y = c.y

    x += xSize/2
    y = ySize/2 - y

    if z <= e.z: return "error"
    return int(x), int(y)

landscape = [] #generating flat landscape
for x in range(0,100,2):
    for z in range(0,100,2):
        landscape.append((x,0,z))

#----------------------Main Loop----------------------#

clock = pygame.time.Clock()
fc = 0
done = False
while not done:
    fc += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if keys[pygame.K_ESCAPE]:
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
    else:
        delta_x, delta_y = pygame.mouse.get_rel()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        rx += delta_x/30
        ry -= delta_y/30
        if ry > 90: ry = 90
        if ry < -90: ry = -90
    if keys[pygame.K_w]:
        c.x += sin(radians(rx))
        c.z += cos(radians(rx))
    if keys[pygame.K_a]:
        c.x += sin(radians(270 - rx))
        c.z += -cos(radians(270 - rx))
    if keys[pygame.K_s]:
        c.x += -sin(radians(180 - rx))
        c.z += cos(radians(180 - rx))
    if keys[pygame.K_d]:
        c.x += sin(radians(90 - rx))
        c.z += -cos(radians(90 - rx))
    if keys[pygame.K_i]:
        px += 1
    if keys[pygame.K_j]:
        pz -= 1
    if keys[pygame.K_k]:
        px -= 1
    if keys[pygame.K_l]:
        pz += 1
    if keys[pygame.K_SPACE]:
        c.y += 1
    if keys[pygame.K_LCTRL]:
        c.y -= 1

    screen.fill([255,255,255])

    for i in range(len(landscape)): #creating landscape
        d = sqrt(pow(landscape[i][2]-px,2) + pow(landscape[i][0]-pz,2))
        if d < 10:
            landscape[i] = (landscape[i][0], centre + sqrt(100 - d*d), landscape[i][2])
        else:
            landscape[i] = (landscape[i][0], 0, landscape[i][2])
            

    render = []
    for i in range(len(landscape)): #rendering landscape
        render.append(get_2d(landscape[i][0],landscape[i][1],landscape[i][2]))
    
    for i in range(0,len(landscape),2):
        if int(i/50)%2 != 0: i += 1
        
        #drawing landscape polygons
        if (i+1) % 50 != 0 and i < len(landscape) - 50:
            #try: outline = pygame.draw.polygon(screen, [0,0,0], ((get_2d(landscape[i][0],landscape[i][1],landscape[i][2])),(get_2d(landscape[i+1][0],landscape[i+1][1],landscape[i+1][2])),(get_2d(landscape[i+51][0],landscape[i+51][1],landscape[i+51][2])),(get_2d(landscape[i+50][0],landscape[i+50][1],landscape[i+50][2]))),1)
            try: outline = pygame.draw.polygon(screen, [0,0,0], (render[i],render[i+1],render[i+51],render[i+50]),1)
                    #outline = pygame.draw.polygon(screen, [100,255,100], (render[i],render[i+1],render[i+51],render[i+50]))
            except: pass

    fps = int(10*clock.get_fps())/10
    fpsLabel = pygame.font.SysFont("monospace", 15).render(str(fps), 1, (0,0,0))
    screen.blit(fpsLabel, (0,0)) #displays fps

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
