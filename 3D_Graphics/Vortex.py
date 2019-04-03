import pygame
import time
from math import radians, sin, cos, tan, sqrt, atan2, acos
from random import randint

pygame.init()

xSize, ySize = 1600, 800
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("3D Graphics")

depth = 1000 #distance between thoertical screen and eye (changes fov)

ry = -45 #rotation about y axis
rx = -20 #rotation about x axis

class c: x, y, z = 150,100,-150 #camera coordinates

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
for x in range(-100,100,10):
    for z in range(-100,100,10):
        landscape.append((x,0,z))

#----------------------Main Loop----------------------#
        
h = 20
R = 15
r = 10
th = radians(45)

#ball
vx, vy, vz = 5, -100, 9 #velocity
bx, by, bz = -100, 15, -100

g = -9.8

clock = pygame.time.Clock()
fc = 0
done = False
while not done:
    fc += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            vx += randint(-5,5)
            vy += randint(0,10)
            vz += randint(-5,5)

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

    screen.fill([255,255,255])

    if fc > 260:
        vy += g/30
        if by <= 0:
            vx -= vx/50
            vz -= vz/50

        bx += vx/30
        if bx < 100 and bx > -100 and bz < 90 and bz > -100:
            by = max(0, by + vy/30)
            if by <= 0: vy = -vy/2
        else: by += vy/30
        bz += vz/30

    th = 3.14/2*sin(fc/50)
    #R = 16+15*sin(fc/10)

    #for i in range(len(landscape)): #creating landscape
        #landscape[i] = (landscape[i][0], 30 + 4*cos(5*radians(landscape[i][2] + landscape[i][0] - fc)), landscape[i][2])

    render = []
    for i in range(len(landscape)): #rendering landscape
        render.append(get_2d(landscape[i][0],landscape[i][1],landscape[i][2]))
    
    for i in range(0,len(landscape)):
        
        #drawing landscape polygons
        if (i+1) % 20 != 0:# and i < len(landscape) - 20:
            try: outline = pygame.draw.polygon(screen, [150,150,150], (render[i],render[i+1],render[i+201],render[i+200]),1)
            except: pass

    phi = atan2(0 - c.z, c.x - R*sin(th))
        
    try: shaft = pygame.draw.line(screen, [0,0,0], (get_2d(0,h,0)),(get_2d(R*sin(th),h - R*cos(th),0)))
    except: pass
    try: pygame.draw.line(screen, [0,0,0], (get_2d(R*sin(th) + r*cos(th), h - R*cos(th) + r*sin(th), 0)),(get_2d(R*sin(th) - r*cos(th), h - R*cos(th) - r*sin(th), 0)))
    except: pass
    try: pygame.draw.line(screen, [0,0,0], (get_2d(R*sin(th), h - R*cos(th), r)),(get_2d(R*sin(th), h - R*cos(th), -r)))
    except: pass
    try: leg = pygame.draw.line(screen, [0,0,0], (get_2d(0,h,0)),(get_2d(0,0,h*r/R)))
    except: pass
    try: leg = pygame.draw.line(screen, [0,0,0], (get_2d(0,h,0)),(get_2d(0,0,-h*r/R)))
    except: pass
    a,b,cc,d =   [get_2d(R*sin(th) + r*cos(th), h - R*cos(th) + r*sin(th), 0),
                get_2d(R*sin(th), h - R*cos(th), r),
                get_2d(R*sin(th) - r*cos(th), h - R*cos(th) - r*sin(th), 0),
                get_2d(R*sin(th), h - R*cos(th), -r)]
    try: board = pygame.draw.polygon(screen, [205,205,255], (a,b,cc,d),0)
    except: pass

    a1,a2,a3 = [-R*sin(th), R*cos(th), 0]
    b1,b2,b3 = [c.x - R*sin(th), c.y - h + R*cos(th), c.z]

    if acos((a1*b1 + a2*b2 + a3*b3)/(sqrt(a1*a1 + a2*a2 + a3*a3)*sqrt(b1*b1 + b2*b2 + b3*b3)))*180/3.141 < 90:
        try: board = pygame.draw.polygon(screen, [205,255,205], (a,b,cc,d),0)
        except: pass
        try: shaft = pygame.draw.line(screen, [0,0,0], (get_2d(0,h,0)),(get_2d(R*sin(th),h - R*cos(th),0)))
        except: pass
        try: leg = pygame.draw.line(screen, [0,0,0], (get_2d(0,h,0)),(get_2d(0,0,h*r/R)))
        except: pass
        try: leg = pygame.draw.line(screen, [0,0,0], (get_2d(0,h,0)),(get_2d(0,0,-h*r/R)))
        except: pass

    try: ball = pygame.draw.circle(screen, [0,0,0], (get_2d(bx,by,bz)), 5)
    except: pass

    fps = int(10*clock.get_fps())/10
    fpsLabel = pygame.font.SysFont("monospace", 15).render(str(fps), 1, (0,0,0))
    screen.blit(fpsLabel, (0,0)) #displays fps

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
