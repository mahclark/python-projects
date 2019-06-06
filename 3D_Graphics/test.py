import numpy as np
from math import cos, sin, tan, pi

xSize, ySize = 1600, 800
xFov = pi/1.1
yFov = pi/4

class ScreenCoordinate():
    def __init__(self, x=0, y=0, behind=False):
    	self.x = x
    	self.y = y
    	self.behind = behind;
a = ScreenCoordinate(1,4)

f = lambda x : x - np.array([5, 50, 500])

rx = 0#pi/4

rotateX = lambda coordinate: np.array([	coordinate[0]*cos(rx) - coordinate[2]*sin(rx),
										coordinate[1],
										coordinate[0]*sin(rx) + coordinate[2]*cos(rx)
										])

makeScreen = lambda coordinate : ScreenCoordinate(behind=True) if coordinate[2] >= 0 else ScreenCoordinate(xSize*(0.5 + coordinate[0]/(coordinate[2]*tan(xFov))), ySize*(0.5 - coordinate[1]/(coordinate[2]*tan(yFov))))


arr = np.apply_along_axis(rotateX, 1, np.zeros((5,3)) + [0,0,-30])

print(arr)

arr = np.apply_along_axis(makeScreen, 1, arr)

for item in arr:
	print(item.x, item.y, item.behind)
# print(yy)

