import pygame
import time
import os
from random import randint
from math import sqrt, atan, atan2, sin as sine, cos as cosine, radians, degrees

def sin(deg): return sine(radians(deg))
def cos(deg): return cosine(radians(deg))

def pythag(a,b): return sqrt(a*a + b*b)

def apply_force(magnitude,angle,hf,vf):
    hf += magnitude*sin(angle)
    vf += -magnitude*cos(angle)
    return hf, vf

def add_body(name,col,mass,pos,hv,vv):
    bodies["name{0}".format(bodies["num"])] = name
    bodies["mass{0}".format(bodies["num"])] = mass
    bodies["color{0}".format(bodies["num"])] = col
    bodies["pos{0}".format(bodies["num"])] = pos
    bodies["hv{0}".format(bodies["num"])] = hv
    bodies["vv{0}".format(bodies["num"])] = vv
    bodies["num"] += 1

def conv_z(pos,panx,pany,zoom):
    return (int((pos[0] + panx - xSize/2)*zoom + xSize/2),int((pos[1] + pany - ySize/2)*zoom + ySize/2))

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
infoObject = pygame.display.Info()
xSize, ySize = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Gravity")

#----------------------Main Loop----------------------#

zoom_d = 3*sqrt(xSize)/5 #zoom
focus = 0
view_mode = 0
fov = 90 #NEW#
offset = 0 #NEW#

G = pow(10,-21)

bodies = {}
bodies["num"] = 0

#add_body(NAME, COLOUR, MASS, POSITION, HV, VV)
add_body("Spaceship",[255,255,255],100,[0,40],sqrt(G*pow(10,25)/40),0)
add_body("The Sun",[254,229,117],pow(10,25),[0,0],0,0)
add_body("Earth",[92,135,45],pow(10,22),[0,500],sqrt(G*bodies["mass1"]/500),0)
add_body("The Moon",[155,155,155],pow(10,20),[0,520],-sqrt(G*bodies["mass2"]/20) + bodies["hv2"],0)
add_body("Mercury",[189,122,33],pow(10,19),[0,50],sqrt(G*bodies["mass1"]/50),0)

bodies["dist0"] = [0.0,0] #NEW#

fps = 60
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if keys[pygame.K_0]: focus = 0
    if keys[pygame.K_1]: focus = 1
    if keys[pygame.K_2]: focus = 2
    if keys[pygame.K_3]: focus = 3
    if keys[pygame.K_4]: focus = 4
    if keys[pygame.K_5]: focus = 5
    if keys[pygame.K_6]: focus = 6
    if keys[pygame.K_7]: focus = 7
    if keys[pygame.K_8]: focus = 8
    if keys[pygame.K_9]: focus = 9
    focus = min(bodies["num"] - 1,focus)

    if keys[pygame.K_v]: #NEW
        if view_mode == 0: view_mode = 1
        else: view_mode = 0

    if keys[pygame.K_PAGEUP]: zoom_d -= 1
    if keys[pygame.K_PAGEDOWN]: zoom_d += 1
    zoom_d = max(zoom_d,1)
    zoom = xSize/(zoom_d*zoom_d)
        
    screen.fill([0,0,0])

    phf, pvf = 0, 0 #player horizontal/vertical velocity

    collect = [] #NEW#

    for a in range(bodies["num"] - 1):
        for b in range(bodies["num"] - 1):
            if b != a:
                
                px1, py1 = bodies["pos{0}".format(b)]
                px2, py2 = bodies["pos{0}".format(a)]
                th = degrees(atan2((py2 - py1),(px2 - px1))) - 90 #theta, in degrees
                
                d = pythag(py1 - py2,px1 - px2) + 0.00000001 #true distance

                f = G*bodies["mass{0}".format(a)]*bodies["mass{0}".format(b)]/(d*d) #gravitational force
    
                hf = 0 #horizontal force
                vf = 0 #vertical force

                if a == 0:
                    if view_mode == 1: foffset = offset #NEW#
                    else: foffset = 0 #NEW#
                    if keys[pygame.K_LSHIFT]: thrust = 2
                    elif keys[pygame.K_SPACE]: thrust = 0.3
                    else: thrust = 1
                    if b == 1:
                        if keys[pygame.K_w]:
                            hf, vf = apply_force(15*pow(10,thrust),0 - foffset,hf,vf) #NEW#
                        if keys[pygame.K_a]:
                            hf, vf = apply_force(15*pow(10,thrust),270,hf,vf)
                        if keys[pygame.K_s]:
                            hf, vf = apply_force(15*pow(10,thrust),180,hf,vf)
                        if keys[pygame.K_d]:
                            hf, vf = apply_force(15*pow(10,thrust),90,hf,vf)

                    bodies["dist{0}".format(b)] = [d,b] #NEW#
                    collect.append(bodies["dist{0}".format(b)]) #NEW#

                    if d < int(pow(bodies["mass{0}".format(b)]/pow(10,22),1/3.5)) + 2:
                        print("You crashed into",bodies["name{0}".format(b)]+".")
                        done = True
                        site = bodies["name{0}".format(b)]
                
                hf, vf = apply_force(f,th,hf,vf)

                if a == 0:
                    phf += hf
                    pvf += vf

                ha = hf/bodies["mass{0}".format(a)] #horizontal acceleration
                va = vf/bodies["mass{0}".format(a)]

                bodies["hv{0}".format(a)] += ha*5/fps #horizontal velocity
                bodies["vv{0}".format(a)] += va*5/fps
    
    collect.sort(reverse=True) #NEW#
    
    #Move
    for a in range(bodies["num"]):
        bodies["pos{0}".format(a)][0] += bodies["hv{0}".format(a)]*5/fps
        bodies["pos{0}".format(a)][1] += bodies["vv{0}".format(a)]*5/fps
        px = bodies["pos{0}".format(a)][0]
        py = bodies["pos{0}".format(a)][1]

    #Projection
    collect.sort(reverse=True)
    
    future = []
    fcrash = False
    fx, fy = bodies["pos0"][0], bodies["pos0"][1]
    fhv, fvv = bodies["hv0"], bodies["vv0"]
    fm = bodies["mass0"]
    escape = True
    d = pythag(fy - bodies["pos1"][1],fx - bodies["pos1"][0])
    for _ in range(400):
        for b in range(1,bodies["num"] - 1):
                px1, py1 = bodies["pos{0}".format(b)]
                px2, py2 = fx, fy
                th = degrees(atan2((py2 - py1),(px2 - px1))) - 90
                if abs(fx - bodies["pos0"][0]) < 0.5 and abs(fy - bodies["pos0"][1]) < 0.5 and _ > 50:
                    fcrash = True
                
                d = pythag(py1 - py2,px1 - px2) + 0.00000001
                if pythag(fhv,fvv) < sqrt(2*G*bodies["mass{0}".format(b)]/d):
                    escape = False

                if d < int(pow(bodies["mass{0}".format(b)]/pow(10,22),1/3.5)) + 2:
                    fcrash = True

                f = G*fm*bodies["mass{0}".format(b)]/(d*d)
    
                hf = 0
                vf = 0
                
                hf, vf = apply_force(f,th,hf,vf)
                
                ha = hf/fm
                va = vf/fm

                fhv += ha*5/fps
                fvv += va*5/fps

                fx += fhv*5/fps/3
                fy += fvv*5/fps/3
                
                if _ % 5 == 0: future.append([fx,fy])
                
        if escape: break
        if fcrash: break

    #Draw
    if view_mode == 0:
        px, py = bodies["pos0"][0], bodies["pos0"][1]
        panx = xSize/2 - bodies["pos{0}".format(focus)][0]
        pany = ySize/2 - bodies["pos{0}".format(focus)][1]
        
        for a in range(1,bodies["num"]):
            rad = int(pow(bodies["mass{0}".format(a)]/pow(10,22),1/3.5)) + 2
            pygame.draw.circle(screen, [255,255,255], conv_z((bodies["pos{0}".format(a)][0],bodies["pos{0}".format(a)][1]),panx,pany,zoom), int(rad*zoom))
            
        pygame.draw.circle(screen, [255,255,255], conv_z((px,py),panx,pany,zoom), 1)
        pygame.draw.line(screen, [255,0,0], conv_z((px + phf*pow(10,-1),py),panx,pany,zoom),conv_z((px,py),panx,pany,zoom),1)
        pygame.draw.line(screen, [255,0,0], conv_z((px,py + pvf*pow(10,-1)),panx,pany,zoom),conv_z((px,py),panx,pany,zoom),1)

    elif view_mode == 1: #NEW#
        px, py = bodies["pos0"][0], bodies["pos0"][1]

        if keys[pygame.K_RIGHT]:
            offset -= 0.1
        if keys[pygame.K_LEFT]:
            offset += 0.1
        while offset <= -180:
            offset += 360
        while offset > 180:
            offset -= 360

        delta_x, delta_y = pygame.mouse.get_rel()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        offset -= delta_x/15
        
        for c in collect:
            a = c[1]
            
            r = pow(bodies["mass{0}".format(a)]/pow(10,22),1/2) + 1
                
            mx, my = bodies["pos{0}".format(a)][0], bodies["pos{0}".format(a)][1]
            angle = degrees(atan2((my - py),(mx - px)))
            
            if -135 <= offset and offset < 45:
                if mx < px and my >= py: angle -= 270 - offset
                else: angle += 90 + offset
            else:
                if mx <= px and my < py: angle += 90 + offset
                else: angle -= 270 - offset
            
            d = pythag(py - bodies["pos{0}".format(a)][1],px - bodies["pos{0}".format(a)][0])
            
            if d >= 11: rad = int(pythag(ySize,xSize)*degrees(atan(r/(d - 8)))/150)
            else: rad = int(pythag(ySize,xSize)*degrees(atan(r/(d*d*d*3/1331)))/150)
            pygame.draw.circle(screen, bodies["color{0}".format(a)], (int(xSize/2 + angle/fov*xSize),int(ySize/2)),rad)
            pygame.draw.circle(screen, bodies["color{0}".format(a)], (int(xSize/2 + (angle + 360)/fov*xSize),int(ySize/2)),rad)
            pygame.draw.circle(screen, bodies["color{0}".format(a)], (int(xSize/2 + (angle - 360)/fov*xSize),int(ySize/2)),rad)

    prev = bodies["pos0"]
    for point in future:
        pygame.draw.line(screen, [255,255,255], conv_z(prev,panx,pany,zoom), conv_z(point,panx,pany,zoom),1)
        prev = point
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
