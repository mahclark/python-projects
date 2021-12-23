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

    class SpaceElevator:

        def __init__(self, parent):
            self.parent = parent
            self.length = 2 * Space.calculate_geostationary_radius(self.parent)
            self.end_point = Vec2()

        def step(self):
            self.end_point = self.parent.position + Vec2(self.length).rotate(self.parent.rotation)

        def draw(self, surface):
            pygame.draw.line(
                surface,
                (255,255,255),
                self.parent.position.xy(),
                self.end_point.xy(),
                2
            )

    name: str
    mass: float
    radius: float
    position: Vec2 = Vec2()
    velocity: Vec2 = Vec2()
    rotation_freq: float = 1/500
    rotation: float = 0
    space_elevator: SpaceElevator = None

    def step(self, time_speed=1):
        self.position += self.velocity * time_speed
        self.rotation += 2 * pi * time_speed * self.rotation_freq % (2 * pi)

        if self.space_elevator is not None:
            self.space_elevator.step()

    def draw(self, surface):
        pygame.draw.circle(surface, (255,255,255), (self.position).xy(), int(self.radius))

        if self.space_elevator is not None:
            self.space_elevator.draw(surface)

    def make_circular_satellite(self, name, mass, radius, relative_position, clockwise=True):
        velocity = Space.calculate_circular_orbit_velocity(self, relative_position, clockwise)
        return Body(name, mass, radius, relative_position + self.position, velocity)

    def add_space_elevator(self):
        self.space_elevator = self.SpaceElevator(self)

    # def attach_to(self, elevator):


    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Space:

    G = 1e-4
    
    def __init__(self):
        self.bodies = set()

    def add_body(self, body):
        self.bodies.add(body)

    @staticmethod
    def calculate_force(from_body, to_body):
        dist = (from_body.position - to_body.position).abs()
        dist = max(dist, from_body.radius + to_body.radius)

        magnitude = (Space.G
            * from_body.mass
            * to_body.mass / dist ** 2)
        return (to_body.position - from_body.position).norm() * magnitude

    @staticmethod
    def calculate_circular_orbit_velocity(main_body, relative_position, clockwise=True):
        speed = sqrt(main_body.mass / relative_position.abs() * Space.G)

        rotation = pi/2 if clockwise else -pi/2
        
        return relative_position.norm().rotate(rotation) * speed + main_body.velocity

    @staticmethod
    def calculate_geostationary_radius(body):
        return (body.rotation_period**2 * Space.G * body.mass / (4 * pi**2)) ** (1/3)

    def step(self, time_speed=1):

        for body in self.bodies:
            resultant_force = Vec2()

            for other_body in self.bodies - {body}:
                resultant_force += Space.calculate_force(body, other_body)

            # F = ma
            acceleration = resultant_force / body.mass

            body.velocity += acceleration * time_speed

            body.step(time_speed)

        # collision check
        collisions = {}

        bodies_by_mass = sorted(self.bodies, key=lambda b: b.mass)
        for i, body in enumerate(bodies_by_mass):
            for larger_body in bodies_by_mass[i+1:]:
                if (body.position - larger_body.position).abs() < body.radius + larger_body.radius:
                    collisions[body] = larger_body
                    break

        for body, larger_body in collisions.items():

            self.bodies.remove(body)

            if body.mass == 1:
                larger_body.mass += 1

            else:
                direction = (larger_body.position - body.position).norm()
                velocity_diff = body.velocity - larger_body.velocity

                mass_ratio = body.mass / larger_body.mass

                reflection_velocity = -velocity_diff.project(direction) * 0.7

                base_velocity = body.velocity + reflection_velocity
                larger_body.velocity -= reflection_velocity * mass_ratio

                if body.mass > 0:
                    for _ in range(int(5*log10(body.mass))):
                        self.add_body(
                            Body(
                                name=f"Fragment{randint(10_000, 99_999)}",
                                mass=1,
                                radius=1,
                                position=body.position + Vec2.random(3),
                                velocity=base_velocity + Vec2.random(0.01)
                            )
                        )

    def reset_momentum(self):
        total_mass = sum([
            body.mass
            for body in self.bodies
        ])
        total_momentum = sum([
            body.velocity * body.mass
            for body in self.bodies
        ], start=Vec2())
        resultant_velocity = total_momentum / total_mass

        for body in self.bodies:
            body.velocity -= resultant_velocity

    def draw(self, surface):
        for body in self.bodies:
            body.draw(surface)

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Space Elevator")

space = Space()

earth = Body(
    "Earth",
    mass=1e6,
    radius=10,
    position=Vec2(*screen.get_size()) / 2
)
# earth.add_space_elevator()
# earth.space_elevator.do_something()
moon = earth.make_circular_satellite(
    "Moon",
    mass=1e4,
    radius=5,
    relative_position=Vec2(400, 0)
)
rock = moon.make_circular_satellite(
    "Rock",
    mass=1e1,
    radius=1,
    relative_position=Vec2(-20,0),
    clockwise=False
)
meteor = Body(
    "Hehehe",
    mass=1e2,
    radius=3,
    position=earth.position + Vec2(12, -500),
    velocity=earth.velocity + Vec2(0.08, 0.1)
)
moon_meteor = Body(
    "test",
    mass=1e2,
    radius=3,
    position=Vec2(x=245, y=-726) + Vec2(*screen.get_size()) / 2,
    velocity=Vec2(x=0.1, y=1)
)
anti_moon = earth.make_circular_satellite(
    "Anti Moon",
    mass=moon.mass,
    radius=moon.radius,
    relative_position=Vec2(-400, 0),
    clockwise=False
)

space.add_body(earth)
space.add_body(moon)

# for i in range(40):
#     space.add_body(
#         earth.make_circular_satellite(
#             f"Moon{i}",
#             mass=0,
#             radius=1,
#             relative_position=Vec2(100 * (i + 1) / 20, 0)
#         ))

space.add_body(rock)
# space.add_body(anti_moon)
space.add_body(meteor)
space.add_body(moon_meteor)

space.reset_momentum()

time_speed = 1

frame = 0
pygame.init()
clock = pygame.time.Clock()
done = False
while not done:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP:
            if keys[pygame.K_COMMA]:
                time_speed *= 0.5
                print(f"x{time_speed}")
            elif keys[pygame.K_PERIOD]:
                time_speed *= 2
                print(f"x{time_speed}")

    screen.fill((0,0,0))

    space.step(time_speed)
    space.draw(screen)

    pygame.display.flip()
    clock.tick(60)
    frame += 1

pygame.quit()