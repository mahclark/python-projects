from math import sqrt, inf
import time

class Size():
    def __init__(self, size):
        self.x = size[0]
        self.y = size[1]

class Node():
    def __init__(self, pos):
        self.pos = pos
    f = 0
    g = 0
    h = 0
    direction = -1

def minF(a):
    minNode = a[0]
    for item in a:
        if item.f < minNode.f:
            minNode = item
    return minNode

def getByPos(a, pos):
    for item in a:
        if item.pos == pos:
            return item
    return None

def checkValid(pos, mapSize, heights, heightRange):
    mapSize = Size(mapSize)

    if pos[0] < 0 or pos[0] >= mapSize.x or pos[1] < 0 or pos[1] >= mapSize.y:
        return False
    if heights[pos] < heightRange[0] or heights[pos] >= heightRange[1]:
        return False
    else: return True

def findPath(start, end, mapSize, normals, heights, heightRange, path):
    print("finding path...")
    mapSize = Size(mapSize)
    
    start = Node(start)
    openList = [start]
    closedList = []

    startTime = time.time()
    timeOut = 10
    heightWeight = 300

    bestBridge = (None, inf)
    
    while len(openList) > 0:        
        q = minF(openList)
        openList.remove(q)

        successors = [
            (q.pos[0] - 1, q.pos[1] - 1),
            (q.pos[0]    , q.pos[1] - 1),
            (q.pos[0] + 1, q.pos[1] - 1),
            (q.pos[0] - 1, q.pos[1]    ),
            (q.pos[0] + 1, q.pos[1]    ),
            (q.pos[0] - 1, q.pos[1] + 1),
            (q.pos[0]    , q.pos[1] + 1),
            (q.pos[0] + 1, q.pos[1] + 1),
            ]
        for n, succPos in enumerate(successors):
            if checkValid(succPos, (mapSize.x, mapSize.y), heights, heightRange):
                
                successor = Node(succPos)
                successor.parent = q
                successor.direction = n
                if successor.pos == end:# or successor.pos in (path if path != None else []):
                    print("path found")
                    path = []
                    current = successor
                    while current != start:
                        path.append(current.pos)
                        current = current.parent
                    path.append(start.pos)
                    
                    return (path[::-1], None)

                heightDiff = heights[successor.pos] - heights[q.pos]
                
                successor.g = q.g + heightWeight*abs(heightDiff)
                successor.h = sqrt((successor.pos[0] - end[0])**2 + (successor.pos[1] - end[1])**2)#max(abs(successor.pos[0] - end[0]), abs(successor.pos[1] - end[1]))
                successor.f = successor.g + successor.h

                closedPosItem = getByPos(closedList, succPos)
                if closedPosItem != None and closedPosItem.f < successor.f:
                    continue

                openPosItem = getByPos(openList, successor.pos)
                if openPosItem != None:
                    if openPosItem.f < successor.f:
                        continue
                    else:
                        openList.remove(openPosItem)

                if closedPosItem != None: closedList.remove(closedPosItem)

                openList.append(successor)

            elif not (succPos[0] < 0 or succPos[0] >= mapSize.x or succPos[1] < 0 or succPos[1] >= mapSize.y) and heights[succPos] < 0.5:
                dot = normals[succPos][0]*(end[0] - succPos[0]) + normals[succPos][1]*(end[1] - succPos[1])
                mod1 = max(sqrt(normals[succPos][0]**2 + normals[succPos][1]**2), 0.0001)
                mod2 = max(sqrt((end[0] - succPos[0])**2 + (end[1] - succPos[1])**2), 0.0001)

                dot /= mod1*mod2

                if q.f < bestBridge[1] and dot > 0.1:
                    coastPoint = Node(succPos)
                    coastPoint.parent = q
                    bestBridge = (coastPoint, q.f)


        if time.time() - startTime > timeOut:
            if bestBridge[0] != None:
                break
            else:
                if timeOut == 10:
                    print("timeOut 1 - trying again")
                    timeOut = 20
                    heightWeight = 100
                else:
                    break

        closedList.append(q)
        
    if bestBridge[0] != None:
        print("try a bridge")
        path = []
        current = bestBridge[0]
        while current != start:
            path.append(current.pos)
            current = current.parent
        path.append(start.pos)

        return (path[::-1], bestBridge[0].pos)
    else:
        print("no path found")
        return (None, None)