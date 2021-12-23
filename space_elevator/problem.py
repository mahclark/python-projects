import pygame
import time
from math import sqrt, sin, cos, pi, log10
from dataclasses import dataclass
from typing import NamedTuple
from random import random, randint, seed

seed(42)


@dataclass
class Vec2:
  
    x: float = 0
    y: float = 0

    @staticmethod
    def random(magnitude=1):
        return Vec2(
            random() - 0.5,
            random() - 0.5
        ).norm() * magnitude

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

    def __mul__(self, k):
        return Vec2(
            self.x * k,
            self.y * k
        )

    def __truediv__(self, k):
        return self * (1/k)

    def abs(self):
        return sqrt(self.x**2 + self.y**2)

    def norm(self):
        if self.abs() == 0:
            return Vec2(1, 1)
        return self * (1 / self.abs())

    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y

    def project(self, direction):
        normalised = direction.norm()
        return normalised * self.dot(normalised)

    def xy(self):
        return (
            int(self.x),
            int(self.y)
        )

    def rotate(self, angle):
        return Vec2(
            self.x * cos(angle) - self.y * sin(angle),
            self.x * sin(angle) + self.y * cos(angle)
        )


@dataclass
class Body:
    name: str
    mass: float

    def __hash__(self):
        return hash(self.name) ^ hash(self.mass)

    def __eq__(self, other):
        return self.name == other.name and self.mass == other.mass


class Space:

    G = 1e-4
    
    def __init__(self):
        self.bodies = set()

    def add_body(self, body):
        self.bodies.add(body)

    def step(self):
        collisions = {}

        bodies_by_mass = list(self.bodies)
        for i, body in enumerate(bodies_by_mass):
            for larger_body in bodies_by_mass[i+1:]:
                # if (body.position - larger_body.position).abs() < body.radius + larger_body.radius:
                collisions[body] = larger_body
                break

        for body, larger_body in collisions.items():

            # if body not in self.bodies:
            #     print({b.name: id(b) for b in self.bodies if b.name == body.name})
            #     print({body.name: id(body)})

            tmp = self.bodies

            self.bodies = {b for b in self.bodies}

            print(body in tmp)
            print(body in self.bodies)

            self.bodies.remove(body)
            tmp.remove(body)

            if body.mass == 1:
                larger_body.mass += 1
                # pass

            else:
                for _ in range(2):
                    self.add_body(
                        Body(
                            name=f"Fragment{randint(10_000, 99_999)}",
                            mass=1
                        )
                    )


space = Space()

earth = Body(
    "Earth",
    mass=1e6
)
body2 = Body(
    "body2",
    mass=5
)

space.add_body(earth)
space.add_body(body2)

while True:
    space.step()
