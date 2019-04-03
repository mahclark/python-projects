import pygame
import time
import os
from functions import read
from math import radians, sin, cos, tan, sqrt, pi

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()

xSize, ySize = 1600, 800
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Pygame Template")

depth = 1000 #distance between thoertical screen and eye (changes fov)

ry = -30 #rotation about y axis
rx = 0 #rotation about x axis

class c: x, y, z = 50,80,-50 #camera coordinates

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

stars_txt = read("\Stars.txt").split("\n")

stars = {}
stars["num"] = 0

for txt in stars_txt:
    stars["name{0}".format(stars["num"])] = txt[:12]
    stars["mag{0}".format(stars["num"])] = float(txt[35:39])
    stars["ra{0}".format(stars["num"])] = int(txt[40:42]) + int(txt[43:46])/60 + float(txt[49:54])/3600
    stars["dec{0}".format(stars["num"])] = float(txt[56:59]) + float(txt[56] + txt[61:63])/60 + float(txt[56] + txt[65:69])/3600
    stars["dist{0}".format(stars["num"])] = float(txt[71:])
    stars["num"] += 1
    

#print(stars["name0"],stars["mag0"],stars["ra0"],stars["dec0"],stars["dist0"])
#print(stars["name4"],stars["mag4"],stars["ra4"],stars["dec4"],stars["dist4"])

#----------------------Main Loop----------------------#

clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 1
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
    if keys[pygame.K_SPACE]:
        c.y += 1
    if keys[pygame.K_LCTRL]:
        c.y -= 1
    if keys[pygame.K_p]:
        c.x = 0
        c.z = 0
        c.y = 0

    screen.fill([0,0,0])

    try: pygame.draw.circle(screen, [0,255,0], (get_2d(0,0,0)),1)
    except: pass

    for star in range(stars["num"]):
        hth = stars["ra{0}".format(star)]*pi/12
        vth = stars["dec{0}".format(star)]*pi/180
        d = stars["dist{0}".format(star)]
        try: pygame.draw.circle(screen, [255,255,255], (get_2d(d*cos(vth)*sin(hth),d*sin(vth),d*cos(vth)*cos(hth))),0)#int(10/stars["mag{0}".format(star)]))
        except: pass
        #label = pygame.font.SysFont("monospace", 8).render(stars["name{0}".format(star)], 1, [255,255,255])
        #try: screen.blit(label, (get_2d(d*sin(hth),d*tan(vth)-1,d*cos(hth))))
        #except: pass

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
