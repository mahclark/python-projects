import pygame
import time
from math import radians, sin, cos, sqrt

pygame.init()

xSize, ySize = 1600, 800
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("3D Graphics")

depth = 1000

ry = 0
rx = 0

def get_2d(x, y, z): #Algorithm to convert 3D coordinates into 2D screen coordinates
    x -= cx
    y -= cy
    z -= cz

    oldx = x
    oldy = y
    
    #turning camera
    x = x*cos(radians(rx)) - z*sin(radians(rx))
    z = z*cos(radians(rx)) + oldx*sin(radians(rx))

    y = y*cos(radians(ry)) - z*sin(radians(ry))
    z = z*cos(radians(ry)) + oldy*sin(radians(ry))

    z -= depth

    class c: x, y, z = 0,0,-depth
    
    try: x = x + (0 - z)*(x - c.x)/(z - c.z)
    except: x = c.x
    try: y = y + (0 - z)*(y - c.y)/(z - c.z)
    except: y = 0

    x += xSize/2
    y = ySize/2 - y

    if z <= c.z: return "error"
    return int(x), int(y)

cx, cy, cz = 0,0,-50
lx, ly, lz = 50,50,50


l = []
for x in range(0,100,2):
    for z in range(0,100,2):
        l.append((x,30,z))

#----------------------Main Loop----------------------#

started = False
clock = pygame.time.Clock()
fc = 0
done = False
while not done:
    if started: fc += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP:
            if keys[pygame.K_p]:
                started = not started
                
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
        cx += sin(radians(rx))
        cz += cos(radians(rx))
    if keys[pygame.K_a]:
        cx += sin(radians(270 - rx))
        cz += -cos(radians(270 - rx))
    if keys[pygame.K_s]:
        cx += -sin(radians(180 - rx))
        cz += cos(radians(180 - rx))
    if keys[pygame.K_d]:
        cx += sin(radians(90 - rx))
        cz += -cos(radians(90 - rx))
    if keys[pygame.K_SPACE]:
        cy += 1
    if keys[pygame.K_LCTRL]:
        cy -= 1
    if keys[pygame.K_y]:
        cx = 0
        cz = 0
        cy = 200
        rx = 0
        ry = -90
    if keys[pygame.K_x]:
        cx = 200
        cz = 0
        cy = 0
        rx = -90
        ry = 0

    screen.fill([255,255,255])

    px, py, pz = 20 + 25*sin(radians(fc)), 10 + 20*cos(radians(fc)), 50

    try: outline = pygame.draw.polygon(screen, [0,0,255], ((get_2d(20,10,0)),(get_2d(-20,10,0)),(get_2d(-20,-10,0)),(get_2d(20,-10,0))),1)
    except: pass
    for i in range(-50,51,5): 
        try: x = pygame.draw.line(screen, [0,0,0], (get_2d(i,0,0)),(get_2d(i+5,0,0)))
        except: pass
    for i in range(-50,51,5): 
        try: y = pygame.draw.line(screen, [0,0,0], (get_2d(0,i,0)),(get_2d(0,i+5,0)))
        except: pass
    for i in range(-50,51,5): 
        try:pygame.draw.line(screen, [0,0,0], (get_2d(0,0,i)),(get_2d(0,0,i+5)))
        except: pass
    try: c = pygame.draw.circle(screen, [255,0,0], (get_2d(0,0,-20)),5)
    except: pass
    try: p = pygame.draw.circle(screen, [0,255,0], (get_2d(px,py,pz)),5)
    except: pass
    g = 100
    for i in range(0,g,2):
        #try: l = pygame.draw.line(screen, [0,0,0], (get_2d(0,0,-20)),(get_2d(px,py,pz)))
        try: l = pygame.draw.line(screen, [0,0,0], (get_2d(i*px/g,i*py/g,-20 + i*(pz+20)/g)),(get_2d((i+1)*px/g,(i+1)*py/g,-20 + (i+1)*(pz+20)/g)))
        except: pass
    try: b = pygame.draw.circle(screen, [0,0,255], (get_2d(px*20/(20 + pz),py*20/(20 + pz),0)),5)
    except: pass

    fps = int(10*clock.get_fps())/10
    fpsLabel = pygame.font.SysFont("monospace", 15).render(str(fps), 1, (0,0,0))
    screen.blit(fpsLabel, (0,0))

    bLabel = pygame.font.SysFont("monospace", 15).render("("+str(int(px*200/(20 + pz))/10)+","+str(int(py*200/(20 + pz))/10)+")", 1, (0,0,0))
    try: screen.blit(bLabel, (get_2d(px*20/(20 + pz),py*20/(20 + pz) - 1,0)))
    except: pass

    pLabel = pygame.font.SysFont("monospace", 15).render("("+str(int(10*px)/10)+","+str(int(10*py)/10)+","+str(int(10*pz)/10)+")", 1, (0,0,0))
    try: screen.blit(pLabel, (get_2d(px,py - 1,pz)))
    except: pass

    cLabel = pygame.font.SysFont("monospace", 15).render("(0,0,-20)", 1, (0,0,0))
    try: screen.blit(cLabel, (get_2d(0,-1,-20)))
    except: pass

    xLabel = pygame.font.SysFont("monospace", 15).render("x", 1, (0,0,0))
    try: screen.blit(xLabel, (get_2d(50,-1,0)))
    except: pass

    yLabel = pygame.font.SysFont("monospace", 15).render("y", 1, (0,0,0))
    try: screen.blit(yLabel, (get_2d(1,50,0)))
    except: pass

    zLabel = pygame.font.SysFont("monospace", 15).render("z", 1, (0,0,0))
    try: screen.blit(zLabel, (get_2d(0,-1,50)))
    except: pass

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
