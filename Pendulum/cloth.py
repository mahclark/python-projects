import pygame
import time
import os
from math import sqrt, sin, cos, atan2, exp, degrees, pi


class Vec2:
  
    def __init__(self, x=0, y=0): 
        self.x = x
        self.y = y

    def __add__(self, vec):
        return Vec2(
            self.x + vec.x,
            self.y + vec.y
        )

    def __sub__(self, vec):
        return self + -vec

    def __neg__(self):
        return Vec2(
            -self.x,
            -self.y
        )

    def __mul__(self, x):
        return Vec2(
            self.x*x,
            self.y*x
        )

    def abs(self):
        return sqrt(self.x**2 + self.y**2)

    def norm(self):
        if self.abs() == 0:
            return Vec2(1, 1)
        return self * (1 / self.abs())

    def dot(self, vec):
        return Vec2(
            self.x * vec.x,
            self.y * vec.y
        )

    def xy(self):
        return (
            int(self.x),
            int(self.y)
        )

    def set(self, vec):
        self.x = vec.x
        self.y = vec.y


class FixedPoint(Vec2):

    color = (142, 12, 84)
    radius = 10


class DynamicPoint(Vec2):

    color = (98, 147, 210)
    radius = 10

    def __init__(self, x, y):
        super().__init__(x, y)

        self.vel = Vec2()

    def apply_gravity(self, g=1):
        self.vel.y += g
        self.x += self.vel.x
        self.y += self.vel.y

class Link:

    color = (109, 113, 105)
    thickness = 2

    def __init__(self, p1, p2, length=None):
        self.p1 = p1
        self.p2 = p2

        if length == None:
            self.length = (self.p1 - self.p2).abs()
        else:
            self.length = length

    def fix_points(self):
        dist = (self.p1 - self.p2).abs()

        if isinstance(self.p1, DynamicPoint):
            diff = (self.p1 - self.p2).norm() * (dist - self.length)
            self.p1.set(
                self.p1 - diff * 0.1
            )

        if isinstance(self.p2, DynamicPoint):
            diff = (self.p2 - self.p1).norm() * (dist - self.length)
            self.p2.set(
                self.p2 - diff * 0.1
            )

        # stretching the true length
        self.length = max(self.length, dist * 0.6)

    def reset_vels(self):
        dist = (self.p1 - self.p2).abs()

        if isinstance(self.p1, DynamicPoint):
            diff = (self.p1 - self.p2).norm() * (dist - self.length)
            self.p1.vel -= diff.norm() * diff.norm().dot(self.p1.vel).abs()
            # if isinstance(self.p2, DynamicPoint):
            #     self.p1.vel += diff.norm() * diff.norm().dot(self.p2.vel).abs()

        if isinstance(self.p2, DynamicPoint):
            diff = (self.p2 - self.p1).norm() * (dist - self.length)
            self.p2.vel -= diff.norm() * diff.norm().dot(self.p2.vel).abs()
            # if isinstance(self.p1, DynamicPoint):
            #     self.p2.vel += diff.norm() * diff.norm().dot(self.p1.vel).abs()


    def collide(self, p):
        link_vec = self.p2 - self.p1
        cut_vec = p - self.p1

        if link_vec.abs() < cut_vec.abs():
            return False

        link_norm = link_vec.norm()
        cut_norm = cut_vec.norm()

        margin = 0.2
        return link_norm.x - margin < cut_norm.x < link_norm.x + margin \
            and link_norm.y - margin < cut_norm.y < link_norm.y + margin


pygame.init()

xSize, ySize = 600, 600
screen = pygame.display.set_mode((xSize, ySize))
pygame.display.set_caption("Cloth")

fixed = []
dynamic = []
links = []

x, y = 11, 7
space = 50

for i in range(y):
    for j in range(x):
        if i == 0:
            fixed.append(FixedPoint(50 + j * space, 50 + i * space))
        else:
            dynamic.append(DynamicPoint(50 + j * space, 50 + i * space))

            if i == 1:
                links.append(Link(fixed[j], dynamic[-1]))
            else:
                links.append(Link(dynamic[-x - 1], dynamic[-1]))

            if j > 0:
                links.append(Link(dynamic[-2], dynamic[-1]))


mouse_hold = False
clock = pygame.time.Clock()
frameCount = 0
done = False
while not done:
    mx, my = pygame.mouse.get_pos()
    frameCount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_hold = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_hold = False
            
    screen.fill([52, 36, 68])

    for p in dynamic:
        p.apply_gravity()

    for _ in range(5):
        for link in links:
            link.fix_points()

    for link in links:
        link.reset_vels()

    if mouse_hold:
        for i, link in enumerate(links):
            if link.collide(Vec2(*pygame.mouse.get_pos())):
                del links[i]

    for link in links:
        pygame.draw.line(screen, link.color, link.p1.xy(), link.p2.xy(), link.thickness)

    for p in fixed + dynamic:
        pygame.draw.circle(screen, p.color, p.xy(), p.radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()