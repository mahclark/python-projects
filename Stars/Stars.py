import csv
import parse
import pygame
import time
import os
from dataclasses import dataclass, replace
from math import radians, sin, cos, tan, sqrt, pi
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

    def xy(self):
        return (
            int(self.x),
            int(self.y)
        )


class Star(Vec3):

    def __init__(self, ra, dec, dist):
        """
        Takes the right ascension, declination and distance from Earth
        and calculates the 3D coordinates of the star
        """
        hth = ra*pi/12
        vth = dec*pi/180

        super().__init__(
            dist*cos(vth)*sin(hth),
            dist*sin(vth),
            dist*cos(vth)*cos(hth)
        )


if __name__ == "__main__":

    pygame.init()

    x_size, y_size = 1600, 800
    screen = pygame.display.set_mode((x_size, y_size))
    pygame.display.set_caption("Stars")

    depth = 500 # fov controller (higher decreases fov)

    rx = -pi # rotation about x axis
    ry = pi/3 # rotation about y axis

    camera = Vec3()

    def draw(surface, color, pos, camera, rx, ry):
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

        pygame.draw.circle(surface, color, pos.xy(), 1)

    # Read and parse the star data
    stars = []

    with open("Stars.txt", "rb") as stars_txt:

        for line in stars_txt.read().decode(encoding='UTF-8').split("\n"):
            _, _, ra_splt, dec_splt, dist_splt = line.split(",")
            
            h, m, s = parse.parse("{:d}h {:d}m {:f}s", ra_splt)
            ra = h + m/60 + s/3600

            sign, h, m, s = parse.parse("{}{:d}° {:d}′ {:f}″", dec_splt)
            dec = float(sign + "1")*(h + m/60 + s/3600)

            dist = float(dist_splt)

            stars.append(Star(ra, dec, dist))

    #----------------------Main Loop----------------------#
    clock = pygame.time.Clock()
    done = False
    while not done:
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

            rx += radians(delta_x/30)
            ry -= radians(delta_y/30)

            ry = min(ry, pi/2)
            ry = max(ry, -pi/2)

        if keys[pygame.K_w]:
            camera.x += sin(rx)
            camera.z += cos(rx)

        if keys[pygame.K_a]:
            camera.x += sin(3*pi/2 - rx)
            camera.z -= cos(3*pi/2 - rx)

        if keys[pygame.K_s]:
            camera.x -= sin(pi - rx)
            camera.z += cos(pi - rx)

        if keys[pygame.K_d]:
            camera.x += sin(pi/2 - rx)
            camera.z -= cos(pi/2 - rx)

        if keys[pygame.K_SPACE]:
            camera.y += 1

        if keys[pygame.K_LCTRL]:
            camera.y -= 1

        if keys[pygame.K_h]:
            camera.x = 0
            camera.z = 0
            camera.y = 0

        if keys[pygame.K_q]:
            done = True

        screen.fill([0,0,0])

        earth = Vec3()

        draw(screen, [0,255,0], earth, camera, rx, ry)

        for star in stars:
            draw(screen, [255,255,255], star, camera, rx, ry)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
