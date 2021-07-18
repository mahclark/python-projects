import csv
import parse
import pygame
import time
from dataclasses import dataclass, replace
from math import radians, sin, cos, pi, sqrt, log10
from typing import NamedTuple

@dataclass
class Vec3:
    x : float = 0
    y : float = 0
    z : float = 0

    def __add__(self, vec):
        return Vec3(
            self.x + vec.x,
            self.y + vec.y,
            self.z + vec.z
        )

    def __sub__(self, vec):
        return self + -vec

    def __neg__(self):
        return Vec3(
            -self.x,
            -self.y,
            -self.z
        )

    def __mul__(self, x):
        return Vec3(
            self.x*x,
            self.y*x,
            self.z*x
        )

    def abs(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def xy(self):
        return (
            int(self.x),
            int(self.y)
        )

    def xyz(self):
        return (
            int(self.x),
            int(self.y),
            int(self.z)
        )


class Star(Vec3):

    def __init__(self, ra, dec, dist, abs_mag):
        """
        Takes the right ascension, declination and distance from Earth
        and calculates the 3D coordinates of the star
        """
        hth = -ra*pi/12
        vth = dec*pi/180

        super().__init__(
            dist*cos(vth)*sin(hth),
            dist*sin(vth),
            dist*cos(vth)*cos(hth)
        )

        self.dist = dist
        self.abs_mag = abs_mag

    def get_app_mag(self, camera):
        rel_dist = (self - camera).abs()

        return self.abs_mag + 5*log10(rel_dist) - 5

    def get_color(self, camera):

        if self.dist == 10_000_000*3.262:
            return (255,255,255)

        mag_hi = 7
        mag_lo = mag_hi+15

        return (Vec3(255,255,255)*(1 - min(1, max(0, (self.get_app_mag(camera) - mag_hi)/(mag_lo - mag_hi))))).xyz()

    def get_draw_rad(self, camera):
        rel_dist = (self - camera).abs()

        app_mag = self.abs_mag + 5*log10(rel_dist) - 5

        return max(0, int(16 - self.get_app_mag(camera)*2))


if __name__ == "__main__":

    pygame.init()

    x_size, y_size = 1600, 800
    screen = pygame.display.set_mode((x_size, y_size))
    surf = pygame.Surface((x_size, y_size), pygame.SRCALPHA, 32)
    pygame.display.set_caption("Stars")

    depth = 500 # fov controller (higher decreases fov)

    rx = -pi # rotation about x axis
    ry = pi/3 # rotation about y axis

    camera = Vec3()
    earth = Vec3()

    speed = 1

    def draw(surface, color, pos, camera, rx, ry, rad=0):
        """
        Converts 3D coordinates to 2D coordinates
        Renders as dot on the surface provided
        """

        # convert world coordinates to camera coordinates
        pos -= camera

        # rotate coordinates around camera
        original = replace(pos) # deep copies dataclass
        
        pos.x = pos.x*cos(rx) - pos.z*sin(rx)
        pos.z = pos.z*cos(rx) + original.x*sin(rx)

        pos.y = pos.y*cos(ry) - pos.z*sin(ry)
        pos.z = pos.z*cos(ry) + original.y*sin(ry)

        # don't draw anything behind us
        if pos.z <= 1: # choose 1 not zero so the next part doesn't explode
            return

        # this part is the 3D to 2D magic
        pos.x *= depth/pos.z
        pos.y *= depth/pos.z

        # adjust so (0,0) is in the middle, not the corner
        pos.x += x_size/2
        pos.y = y_size/2 - pos.y

        if rad == 0:
            surface.set_at(pos.xy(), color)
        else:

            for r in range(rad, rad//3 - 1, -1):

                if rad == 0 or r == 1:
                    scale = 1
                else:
                    scale = min(1, max(0, .8*(r - rad)**2/(2*rad/3)**2 + .2))

                try:
                    pygame.draw.circle(surface, (*color, 255*scale), pos.xy(), r)
                except TypeError:
                    print(pos.xy())
                    raise TypeError

    # Read and parse the star data
    stars = []

    with open("data/hygfull.csv") as data_csv:
        reader = csv.reader(data_csv)
        header = next(reader, None)

        ra_i = header.index("RA")
        dec_i = header.index("Dec")
        dist_i = header.index("Distance")
        abs_mag_i = header.index("AbsMag")

        for line in reader:
            ra = float(line[ra_i])
            dec = float(line[dec_i])
            dist = float(line[dist_i])*3.262
            abs_mag = float(line[abs_mag_i])

            star = Star(ra, dec, dist, abs_mag)

            if star.get_app_mag(earth) < 7 or abs_mag < -7:
                stars.append(star)

    stars = sorted(stars, key=lambda s: -s.get_app_mag(earth))

    print(f"loaded {len(stars)} stars")

    # with open("Stars.txt", "rb") as stars_txt:

    #     for line in stars_txt.read().decode(encoding='UTF-8').split("\n"):
    #         _, _, ra_splt, dec_splt, dist_splt = line.split(",")
            
    #         h, m, s = parse.parse("{:d}h {:d}m {:f}s", ra_splt)
    #         ra = h + m/60 + s/3600

    #         sign, h, m, s = parse.parse("{}{:d}° {:d}′ {:f}″", dec_splt)
    #         dec = float(sign + "1")*(h + m/60 + s/3600)

    #         dist = float(dist_splt)

    #         stars.append(Star(ra, dec, dist))

    #----------------------Main Loop----------------------#
    clock = pygame.time.Clock()
    done = False
    while not done:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    speed *= 1.1
                elif event.button == 5:
                    speed /= 1.1
                # print(f"{speed:.2f}")

        if keys[pygame.K_ESCAPE]:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
        else:
            delta_x, delta_y = pygame.mouse.get_rel()
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

            rx += radians(delta_x/30)
            ry -= radians(delta_y/30)

            ry = min(ry, pi/2)
            ry = max(ry, -pi/2)

        if keys[pygame.K_w]:
            camera.x += sin(rx)*speed
            camera.z += cos(rx)*speed

        if keys[pygame.K_a]:
            camera.x += sin(3*pi/2 - rx)*speed
            camera.z -= cos(3*pi/2 - rx)*speed

        if keys[pygame.K_s]:
            camera.x -= sin(pi - rx)*speed
            camera.z += cos(pi - rx)*speed

        if keys[pygame.K_d]:
            camera.x += sin(pi/2 - rx)*speed
            camera.z -= cos(pi/2 - rx)*speed

        if keys[pygame.K_SPACE]:
            camera.y += 1*speed

        if keys[pygame.K_LCTRL]:
            camera.y -= 1*speed

        if keys[pygame.K_h]:
            camera.x = 0
            camera.z = 0
            camera.y = 0

        if keys[pygame.K_q]:
            done = True

        screen.fill([0,0,0])
        surf.fill([0,0,0])

        for star in stars:
            draw(surf, star.get_color(camera), star, camera, rx, ry, star.get_draw_rad(camera))

        draw(surf, [0,255,0], earth, camera, rx, ry, 2)

        screen.blit(surf, (0,0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
