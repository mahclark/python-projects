from math import sqrt
import random
from random import randint

class Size():
    def __init__(self, size):
        self.x = size[0]
        self.y = size[1]

def fade(x): return 6*x**5 - 15*x**4 + 10*x**3


def makeNoise(cellSize, mapSize):
    print("generating landscape...")
    cellSize = Size(cellSize)
    mapSize = Size(mapSize)
    overSize = Size((mapSize.x % cellSize.x, mapSize.y % cellSize.y))
    mapSize.x += overSize.x
    mapSize.y += overSize.y

    vectorChoice = [
        ( 1, 1),
        ( 1,-1),
        (-1,-1),
        (-1, 1)
        ]
    vectors = []

    for yCorner in range(int(mapSize.y/cellSize.y) + 1):
        vectors.append([])
        for xCorner in range(int(mapSize.x/cellSize.x) + 1):
            vectors[yCorner].append(vectorChoice[randint(0, len(vectorChoice) - 1)])

    #     vectors[yCorner].append(vectors[yCorner][0])
    # vectors.append(vectors[0])

    values = []
    for y in range(mapSize.y - overSize.y):
        values.append([])

    for yCell in range(int(mapSize.y/cellSize.y)):
        for xCell in range(int(mapSize.x/cellSize.x)):

            randVec0 = vectors[yCell    ][xCell    ]
            randVec1 = vectors[yCell    ][xCell + 1]
            randVec2 = vectors[yCell + 1][xCell + 1]
            randVec3 = vectors[yCell + 1][xCell    ]

            for yPixel in range(cellSize.y):
                for xPixel in range(cellSize.x):

                    distVec0 = (xPixel/cellSize.x    , yPixel/cellSize.y    )
                    distVec1 = (xPixel/cellSize.x - 1, yPixel/cellSize.y    )
                    distVec2 = (xPixel/cellSize.x - 1, yPixel/cellSize.y - 1)
                    distVec3 = (xPixel/cellSize.x    , yPixel/cellSize.y - 1)

                    dot0 = randVec0[0]*distVec0[0] + randVec0[1]*distVec0[1]
                    dot1 = randVec1[0]*distVec1[0] + randVec1[1]*distVec1[1]
                    dot2 = randVec2[0]*distVec2[0] + randVec2[1]*distVec2[1]
                    dot3 = randVec3[0]*distVec3[0] + randVec3[1]*distVec3[1]

                    topInterpolated = dot0 + fade(xPixel/cellSize.x)*(dot1 - dot0)
                    botInterpolated = dot3 + fade(xPixel/cellSize.x)*(dot2 - dot3)

                    finalValue = topInterpolated + fade(yPixel/cellSize.y)*(botInterpolated - topInterpolated)

                    if yCell*cellSize.y + yPixel < mapSize.y - overSize.y and len(values[yCell*cellSize.y + yPixel]) < mapSize.x - overSize.x:
                        values[yCell*cellSize.y + yPixel].append(finalValue)

    normals = []
    heightWeight = 100
    for y in range(mapSize.y - overSize.y):
        normals.append([])
        for x in range(mapSize.x - overSize.y):
            if y == 0:
                Ty = (0, 1, heightWeight*(values[y + 1][x] - values[y][x]))
            elif y == mapSize.y - 1:
                Ty = (0, 1, heightWeight*(values[y][x] - values[y - 1][x]))
            else:
                Ty = (0, 2, heightWeight*(values[y + 1][x] - values[y - 1][x]))

            if x == 0:
                Tx = (1, 0, heightWeight*(values[y][x + 1] - values[y][x]))
            elif x == mapSize.x - 1:
                Tx = (1, 0, heightWeight*(values[y][x] - values[y][x - 1]))
            else:
                Tx = (2, 0, heightWeight*(values[y][x + 1] - values[y][x - 1]))

            xProduct = (Ty[1]*Tx[2] - Ty[2]*Tx[1], Ty[2]*Tx[0] - Ty[0]*Tx[2], Ty[0]*Tx[1] - Ty[1]*Tx[0])
            modulus = sqrt(xProduct[0]**2 + xProduct[1]**2 + xProduct[2]**2)

            normal = (-xProduct[0]/modulus, -xProduct[1]/modulus, -xProduct[2]/modulus)

            normals[y].append(normal)

    return (values, normals)