import pygame
import time
import os
from random import randint, gauss
from math import sqrt, atan, atan2, sin as sine, cos as cosine, tan, radians, degrees
from functions import read

old_method = pygame.draw.circle

def circle(a, b, c, r):
    if r == 1:
        pygame.draw.rect(a,b,(c[0] - 1, c[1] - 1,2,2))
    else:
        old_method(a,b,c,r)

def sin(deg): return sine(radians(deg))
def cos(deg): return cosine(radians(deg))

def pythag(a,b):
    return sqrt(a*a + b*b)

def apply_force(magnitude,angle,hf,vf):
    hf += magnitude*sin(angle)
    vf += -magnitude*cos(angle)
    return hf, vf

def add_body(name,col1,col2,path,mass,pos,hv,vv):
    bodies["name{0}".format(bodies["num"])] = name
    bodies["mass{0}".format(bodies["num"])] = mass
    bodies["color{0}".format(bodies["num"])] = col1
    bodies["text{0}".format(bodies["num"])] = {}
    bodies["pos{0}".format(bodies["num"])] = pos
    bodies["hv{0}".format(bodies["num"])] = hv
    bodies["vv{0}".format(bodies["num"])] = vv

    bodies["rot{0}".format(bodies["num"])] = 0
    if path != "":
        text = read("\Textures" + path).split("\n")
        for i in range(len(text)):
            bodies["text{0}".format(bodies["num"])][i] = []
            for j in text[i]:
                if j == "q": bodies["text{0}".format(bodies["num"])][i].append(col2)
                elif j == "w": bodies["text{0}".format(bodies["num"])][i].append(col1)
    
    bodies["num"] += 1


def label(txt,pos,font):
    lbl = font.render(txt, 1, [205,205,205])
    try: screen.blit(lbl,pos)
    except: pass

def conv_z(pos,panx,pany,zoom):
    return (int((pos[0] + panx - xSize/2)*zoom + xSize/2),int((pos[1] + pany - ySize/2)*zoom + ySize/2))

def rotate(a,th,rot_n):
    n = len(bodies["text{0}".format(a)][0])
    limit = 360/n

    while rot_n < int(th/limit):
        rot_n += 1
        if rot_n == n: rot_n = 0
        for i in range(len(bodies["text{0}".format(a)])):
            bodies["text{0}".format(a)][i].insert(0,bodies["text{0}".format(a)][i][len(bodies["text{0}".format(a)][i]) - 1])
            bodies["text{0}".format(a)][i].pop(len(bodies["text{0}".format(a)][i]) - 1)

    while rot_n > int(th/limit):
        rot_n -= 1
        if rot_n == int(th/limit) - 1: rot_n = n
        for i in range(len(bodies["text{0}".format(a)])):
            bodies["text{0}".format(a)][i].append(bodies["text{0}".format(a)][i][0])
            bodies["text{0}".format(a)][i].pop(0)
            
    return rot_n

def make_planet(ox,oy,r,texture):
    if ox + rad > 0 and ox - rad < xSize:
        for y in range(oy - r + 1, oy + r):
            ncol = int((y - oy + r)/(r/len(texture))/2)
            
            r2 = sqrt(r**2 - (y - oy)**2)
            c = 2*3.141*r2
            n = len(texture[ncol])

            n/=2
            for i in range(int(n)):
                icol = i
                while icol >= 2*n:
                    icol = int(i - 2*n)
                if r2 == 0: r2 = 0.000001
                x = r2*cosine(i*c/(2*n)/r2) - r2*cosine(i*c/(2*n)/r2 + c/(2*n)/r2)
                x1 = r2 - r2*cosine(i*c/(2*n)/r2)
                pygame.draw.line(screen, texture[ncol][icol], (ox - r2 + x1, y), (ox - r2 + x1 + x, y))

def terminator(ox, oy, rad, angle, col):
    if ox + rad > 0 and ox - rad < xSize:
        if rad < 2:
            angle = 180 - abs(180 - angle)/1
            circle(screen,[col[0]*angle/180,col[1]*angle/180,col[2]*angle/180],(ox,oy),rad)
        else:
            angle -= int(angle/360)*360
            for y in range(oy - rad, oy + rad):
                if angle <= 90:
                    inter = (rad*rad - (y - oy)*(y - oy))/(tan(radians(angle) + 0.000001) + 1)
                    x = ox + sqrt(abs(inter))*inter/abs(inter + 0.00001)
                elif angle >= 270:
                    inter = (rad*rad - (y - oy)*(y - oy))/(tan(radians(-angle) + 0.000001) + 1)
                    x = ox - sqrt(abs(inter))*inter/abs(inter + 0.00001)
                elif angle < 180:
                    inter = (rad*rad - (y - oy)*(y - oy))/(tan(radians(-angle) + 0.000001) + 1)
                    x = ox - sqrt(abs(inter))*inter/abs(inter + 0.00001)
                else:
                    inter = (rad*rad - (y - oy)*(y - oy))/(tan(radians(angle) + 0.000001) + 1)
                    x = ox + sqrt(abs(inter))*inter/abs(inter + 0.00001)
                
                try:
                    if angle >= 180:
                        xs = x
                        xe = ox + sqrt(rad*rad - pow(y - oy,2)) + 2
                    else:
                        xs = ox - sqrt(rad*rad - pow(y - oy,2))
                        xe = x
                    
                    horizontal_line = pygame.Surface((abs(xe - xs), 1), pygame.SRCALPHA)
                    horizontal_line.fill((0, 0, 0, 249))
                    screen.blit(horizontal_line, (xs,y))
                except: pass

dir_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
infoObject = pygame.display.Info()
xSize, ySize = infoObject.current_w, infoObject.current_h#1440, 900
screen = pygame.display.set_mode((xSize, ySize), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.display.set_caption("Gravity")

#----------------------Main Loop----------------------#

texturing = True
zoom_d = 3*sqrt(xSize)/10
view_mode = 1
focus = 0
landed = False
fov = 90
offset = 0
orbit_time = 0
pdist = 0
focus_target = 0

G = pow(10,-22)

bodies = {}
bodies["num"] = 0

#add_body(NAME, COLOUR1, COLOUR2, PATH, MASS, POSITION, HORIZONTAL_VELOCITY, VERTICAL_VELOCITY)
add_body("Spaceship",[255,255,255],[255,255,255],"",200,[0,600],0,0)
add_body("The Sun",[254,229,117],[254,229,117],"",pow(10,25),[0,0],0,0)
add_body("Earth",[37,78,124],[92,135,45],"\Text_Earth.txt",pow(10,22),[0,500],sqrt(G*bodies["mass1"]/500),0)
add_body("The Moon",[105,105,105],[65,65,65],"\Text_Moon.txt",pow(10,20),[0,520],-sqrt(G*bodies["mass2"]/20) + bodies["hv2"],0)
add_body("Mercury",[189,122,33],[189,122,33],"",pow(10,19),[0,50],sqrt(G*bodies["mass1"]/50),0)
add_body("Halley's Comet",[186,229,213],[186,229,213],"",pow(10,17),[-1000,0],0,sqrt(G*bodies["mass1"]/50000))
add_body("Jupiter",[250,230,220],[220,151,97],"\Text_Jupiter.txt",pow(10,23),[1200,0],0,-sqrt(G*bodies["mass1"]/1200))
add_body("Europa",[105,71,66],[105,71,66],"",pow(10,19),[1180,0],0,-sqrt(G*bodies["mass6"]/20) + bodies["vv6"])
add_body("Io",[223,218,57],[223,218,57],"",pow(10,19),[1130,0],0,-sqrt(G*bodies["mass6"]/70) + bodies["vv6"])
add_body("Callisto",[170,158,90],[170,158,90],"",pow(10,18),[1150,0],0,-sqrt(G*bodies["mass6"]/50) + bodies["vv6"])
add_body("Neptune",[30,45,175],[200,200,200],"\Text_Neptune.txt",5*pow(10,22),[-1700,0],0,sqrt(G*bodies["mass1"]/1700))
add_body("Pluto",[195,195,195],[170,158,90],"",pow(10,21),[0,2000],sqrt(G*bodies["mass1"]/2000),0)
add_body("Planet X",[100,65,204],[20,20,20],"\Text_Planet_X.txt",pow(10,22),[0,-10000],sqrt(G*bodies["mass1"]/10000),0)
add_body("Alpha Centauri A",[254,159,67],[170,158,90],"",pow(10,25),[100000,20000],-sqrt(G*2*pow(10,25)/400),0)
add_body("Alpha Centauri B",[94,109,247],[170,158,90],"",2*pow(10,25),[100000,20200],sqrt(G*pow(10,25)/400),0)
add_body("Proxima Centauri",[255,59,37],[170,158,90],"",pow(10,23),[100000,22000],sqrt(G*3*pow(10,25)/2000),0)
add_body("Black Hole",[0,0,0],[0,0,0],"",pow(10,24),[500,600],0,0)
#add_body("Ok",[255,255,255],[255,0,0],"\Text_Ok.txt",pow(10,25),[500,0],0,0)
    

bodies["rv0"] = 0.0
bodies["dist0"] = [0.0,0]


##rot_n = 0
##q = [92,135,45]
##w = [37,78,124]
##text = read("\Earth_Texture.txt").split("\n")
##texture = {}
##for i in range(len(text)):
##    texture[i] = []
##    for j in text[i]:
##        if j == "q": texture[i].append(q)
##        elif j == "w": texture[i].append(w)

#Stars
stars = []
for i in range(1000):
    stars.append([randint(-179,180), randint(0,ySize), randint(50,255)])
for i in range(1001,2000):
    x = gauss(180,60)
    y = -1
    while y > ySize or y < 0:
        y = gauss(3*x,50)
    stars.append([x - 180, y, randint(50,255)])

fps = 60
mouseHold = True
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    frameCount += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if keys[pygame.K_q]: done = True
    
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
    
    if keys[pygame.K_v]:
        if view_mode == 0: view_mode = 1
        else: view_mode = 0

    if keys[pygame.K_PAGEUP]: zoom_d -= 1
    if keys[pygame.K_PAGEDOWN]: zoom_d += 1
    zoom_d = max(zoom_d,1)
    zoom = xSize/(zoom_d*zoom_d)
        
    screen.fill([0,0,0])

    if frameCount % 50 == 0:
        for i in range(len(bodies["text2"])):
            bodies["text2"][i].append(bodies["text2"][i][0])
            bodies["text2"][i].pop(0)


    phf, pvf = 0, 0

    collect = []
    gr = False
    orbit_n = 0
    focus_deviation = 0
    for a in range(bodies["num"]):
        for b in range(bodies["num"]):
            if b != a:
                
                px1, py1 = bodies["pos{0}".format(b)]
                px2, py2 = bodies["pos{0}".format(a)]
                th = degrees(atan2((py2 - py1),(px2 - px1))) - 90 #theta, in degrees

                try:
                    if b == 0: bodies["rot{0}".format(a)] = rotate(a, th, bodies["rot{0}".format(a)])
                except: pass
                
                d = pythag(py1 - py2,px1 - px2) + 0.00000001 #true distance

                f = G*bodies["mass{0}".format(a)]*bodies["mass{0}".format(b)]/(d*d) #gravitational force
    
                hf = 0 #horizontal force
                vf = 0 #vertical force

                if a == 0:
                    if view_mode == 1: foffset = offset
                    else: foffset = 0
                    if keys[pygame.K_LSHIFT]: thrust = 2
                    elif keys[pygame.K_SPACE]: thrust = 0.3
                    else: thrust = 1
                    if b == 1:
                        if keys[pygame.K_w]:
                            hf, vf = apply_force(15*pow(10,thrust),0 - foffset,hf,vf)
                        if keys[pygame.K_a]:
                            hf, vf = apply_force(15*pow(10,thrust),270 - foffset,hf,vf)
                        if keys[pygame.K_s]:
                            hf, vf = apply_force(15*pow(10,thrust),180 - foffset,hf,vf)
                        if keys[pygame.K_d]:
                            hf, vf = apply_force(15*pow(10,thrust),90 - foffset,hf,vf)

                    
                    bodies["dist{0}".format(b)] = [d,b]
                    collect.append(bodies["dist{0}".format(b)])
                    pv = pythag(bodies["hv{0}".format(a)],bodies["vv{0}".format(a)])
                    rv = pythag(bodies["hv{0}".format(a)] - bodies["hv{0}".format(b)], bodies["vv{0}".format(a)] - bodies["vv{0}".format(b)]) #relative velocity
                    bodies["rv{0}".format(b)] = rv

                    if d < int(pow(bodies["mass{0}".format(b)]/pow(10,22),1/3.5)) + 2:
                        print("You crashed into",bodies["name{0}".format(b)]+".")
                        done = True
                        site = bodies["name{0}".format(b)]

                    
                    #if b == 2: print(rv < sqrt(2*G*bodies["mass{0}".format(b)]/d), d < int(pow(bodies["mass{0}".format(b)]/pow(10,22),1/3.5)) + 6)
                    if rv < sqrt(2*G*bodies["mass{0}".format(b)]/d) and d < int(pow(bodies["mass{0}".format(b)]/pow(10,22),1/3.5)) + 7:
                        gr = True
                        orbit_time += 1
                        if keys[pygame.K_RETURN] and orbit_time > 100:
                            print("You landed on",bodies["name{0}".format(b)]+".")
                            done = True
                            site = bodies["name{0}".format(b)]
                            landed = True
                        orbit_n += 1
                
                hf, vf = apply_force(f,th,hf,vf)

                if a == 0:
                    phf += hf
                    pvf += vf

                ha = hf/bodies["mass{0}".format(a)] #horizontal acceleration
                va = vf/bodies["mass{0}".format(a)]

                bodies["hv{0}".format(a)] += ha*5/fps #horizontal velocity
                bodies["vv{0}".format(a)] += va*5/fps
                
    if orbit_n < 1:
        orbit_time = 0
    collect.sort(reverse=True)
    
    #Move
    for a in range(bodies["num"]):
        bodies["pos{0}".format(a)][0] += bodies["hv{0}".format(a)]*5/fps
        bodies["pos{0}".format(a)][1] += bodies["vv{0}".format(a)]*5/fps
    
    #Draw
    if view_mode == 0:
        px, py = bodies["pos0"][0], bodies["pos0"][1]
        panx = xSize/2 - bodies["pos{0}".format(focus)][0]
        pany = ySize/2 - bodies["pos{0}".format(focus)][1]
        
        for a in range(1,bodies["num"]):
            rad = int(pow(bodies["mass{0}".format(a)]/pow(10,22),1/3.5)) + 2
            circle(screen, [255,255,255], conv_z((bodies["pos{0}".format(a)][0],bodies["pos{0}".format(a)][1]),panx,pany,zoom), int(rad*zoom))
            
        if gr == True: circle(screen, [0,255,0], conv_z((px,py),panx,pany,zoom),1)
        else: circle(screen, [255,255,255], conv_z((px,py),panx,pany,zoom), 1)
        pygame.draw.line(screen, [255,0,0], conv_z((px + phf*pow(10,-1),py),panx,pany,zoom),conv_z((px,py),panx,pany,zoom),1)
        pygame.draw.line(screen, [255,0,0], conv_z((px,py + pvf*pow(10,-1)),panx,pany,zoom),conv_z((px,py),panx,pany,zoom),1)
        
    elif view_mode == 1:
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

        #Lensing Preparation
        mx, my = bodies["pos16"][0], bodies["pos16"][1]
        angle = degrees(atan2((my - py),(mx - px)))
        r = pow(bodies["mass16"]/pow(10,22),1/2) + 1
        d = pythag(py - bodies["pos16"][1],px - bodies["pos16"][0])
        if d >= 11: rad = int(pythag(ySize,xSize)*degrees(atan(r/(d - 8)))/150)
        else: rad = int(pythag(ySize,xSize)*degrees(atan(r/(d*d*d*3/1331)))/150)
        
        #Stars
        for star in stars:
            origx = star[0]
            origy = star[1]
            star[0] += 90
            star[1] -= ySize/2
            col = [star[2],star[2],star[2]]
            odist = sqrt(pow(star[1]*fov/xSize,2) + pow(star[0] - 90 - angle,2))
            if odist < 2*rad*fov/xSize:
                #col = [255,0,0]
                arg = atan2(star[1]*fov/xSize, star[0] - 90 - angle)
                dist = pow(odist,2)/(4*rad*fov/xSize) + rad*fov/xSize
                star[0] = angle + 90 + dist*cosine(arg)
                star[1] = dist*sine(arg)*xSize/fov
                #if star[0] - 90 > angle: star[0] = angle + 90 + pow(star[0] - 90 - angle,2)/(4*rad*fov/xSize) + rad*fov/xSize
                #elif star[0] - 90 < angle: star[0] = angle + 90 - pow(star[0] - 90 - angle,2)/(4*rad*fov/xSize) - rad*fov/xSize
                #print(angle, rad*fov/xSize, arg, odist, dist, origx, origy, star[0], star[1])
                
            for n in range(-1,2):
                screen.set_at((int(xSize/2 + (star[0] + offset + 360*n)/fov*xSize), int(star[1] + ySize/2)), col)
            star[0] = origx
            star[1] = origy
        
        for c in collect:
            a = c[1]
            
            mx, my = bodies["pos{0}".format(a)][0], bodies["pos{0}".format(a)][1]
            angle = degrees(atan2((my - py),(mx - px)))
            
            if -135 <= offset and offset < 45:
                if mx < px and my >= py: angle -= 270 - offset
                else: angle += 90 + offset
            else:
                if mx <= px and my < py: angle += 90 + offset
                else: angle -= 270 - offset

            if a == focus:
                if True or [pygame.K_f]:
                    offset -= angle
            
            r = pow(bodies["mass{0}".format(a)]/pow(10,22),1/2) + 1
            d = pythag(py - bodies["pos{0}".format(a)][1],px - bodies["pos{0}".format(a)][0])
            
            if d >= 11: rad = int(pythag(ySize,xSize)*degrees(atan(r/(d - 8)))/150)
            else: rad = int(pythag(ySize,xSize)*degrees(atan(r/(d*d*d*3/1331)))/150)

            if a != 1:
                px1, py1 = bodies["pos{0}".format(a)]
                px2, py2 = bodies["pos0"]
                th = degrees(atan2((py2 - py1),(px2 - px1)))
                px2, py2 = bodies["pos1"]
                th = degrees(atan2((py2 - py1),(px2 - px1))) - th

                if th < 180:
                    th += 180
                else:
                    th -= 180

                while th < 0: th += 360
                while th > 360: th -= 360

                
                if texturing and len(bodies["text{0}".format(a)]) > 0:
                    make_planet(int(xSize/2 + angle/fov*xSize), int(ySize/2), rad, bodies["text{0}".format(a)])
                    make_planet(int(xSize/2 + (angle + 360)/fov*xSize), int(ySize/2), rad, bodies["text{0}".format(a)])
                    make_planet(int(xSize/2 + (angle - 360)/fov*xSize), int(ySize/2), rad, bodies["text{0}".format(a)])
                else:
                    circle(screen,bodies["color{0}".format(a)],(int(xSize/2 + angle/fov*xSize),int(ySize/2)),rad)
                    circle(screen,bodies["color{0}".format(a)],(int(xSize/2 + (angle + 360)/fov*xSize),int(ySize/2)),rad)
                    circle(screen,bodies["color{0}".format(a)],(int(xSize/2 + (angle - 360)/fov*xSize),int(ySize/2)),rad)
                terminator(int(xSize/2 + angle/fov*xSize),int(ySize/2), rad, th, bodies["color{0}".format(a)])
                terminator(int(xSize/2 + (angle + 360)/fov*xSize),int(ySize/2), rad, th, bodies["color{0}".format(a)])
                terminator(int(xSize/2 + (angle - 360)/fov*xSize),int(ySize/2), rad, th, bodies["color{0}".format(a)])
            else:
##                make_planet(int(xSize/2 + angle/fov*xSize), int(ySize/2), rad, bodies["text{0}".format(a)])
##                make_planet(int(xSize/2 + (angle + 360)/fov*xSize), int(ySize/2), rad, bodies["text{0}".format(a)])
##                make_planet(int(xSize/2 + (angle - 360)/fov*xSize), int(ySize/2), rad, bodies["text{0}".format(a)])
                circle(screen, bodies["color{0}".format(a)], (int(xSize/2 + angle/fov*xSize),int(ySize/2)),rad)
                circle(screen, bodies["color{0}".format(a)], (int(xSize/2 + (angle + 360)/fov*xSize),int(ySize/2)),rad)
                circle(screen, bodies["color{0}".format(a)], (int(xSize/2 + (angle - 360)/fov*xSize),int(ySize/2)),rad)

            if focus_deviation > abs(int(xSize/2 + angle/fov*xSize) - xSize/2) or focus_deviation == 0:
                focus_deviation = abs(int(xSize/2 + angle/fov*xSize) - xSize/2)
                focus_target = a

        if keys[pygame.K_r]:
            focus = focus_target
        
        pygame.draw.line(screen,[15,15,20],(0,ySize/10),(xSize/3 + 5,ySize*3/5 + 7),15)
        pygame.draw.line(screen,[15,15,20],(xSize,ySize/10),(xSize*2/3 - 5,ySize*3/5 + 9),15)
        pygame.draw.line(screen,[15,15,20],(xSize*9/24,ySize),(xSize/3,ySize*3/5),10)
        pygame.draw.line(screen,[15,15,20],(xSize*15/24,ySize),(xSize*2/3,ySize*3/5),10)
            
        font1 = pygame.font.SysFont("agency fb", 20)

        dist = int(bodies["dist{0}".format(focus)][0]*1000)/100

        label("Focus: " + str(bodies["name{0}".format(focus)]),(10,ySize-75),font1)
        label("Distance: "+ str(dist),(10,ySize-25),font1)
        if dist <= pdist: label("Relative Velocity: " + str(int(bodies["rv{0}".format(focus)]*5000)/1000),(10,ySize-50),font1)
        else: label("Relative Velocity: " + str(-int(bodies["rv{0}".format(focus)]*5000)/1000),(10,ySize-50),font1)
        label(str(int(pv*5000)/1000),(xSize - 25 - 8*len(str(int(pv*5000)/1000)),ySize-25),font1)
        label("pps",(xSize - 25,ySize-25),font1)

        if not keys[pygame.K_r]:
            focus = 0

        pdist = dist
        
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

##if landed == True:
##    if site == "Earth":
##        print("Mission Success")
##    elif site == "The Sun":
##        print("Mission Failed (though that's quite an achievement...)")
##    else:
##        print("Mission Failed")
##else:
##    print("Mission Failed")
##input()
