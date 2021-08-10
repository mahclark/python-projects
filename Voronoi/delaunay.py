from math import sqrt

def midpoint(a, b, c): #finds the point equidistant to a, b and c
    x0, y0 = a
    x1, y1 = b
    x2, y2 = c

    n = (y1**2 - y0**2 - x0**2 + x1**2)*(x0 - x2) + (x2**2 - x0**2 - y0**2 + y2**2)*(x1 - x0)
    d = 2*(y2 - y0)*(x1 - x0) - 2*(y0 - y1)*(x0 - x2)
    y = n/d

    x = (2*y*(y0 - y1) + y1**2 - y0**2 - x0**2 + x1**2)/(2*(x1 - x0))

    return (x,y)

def dist(a, b): #finds the distance between two points
    x0, y0 = a
    x1, y1 = b

    return sqrt((x0 - x1)**2 + (y0 - y1)**2)


def isTriangle(a, b, c, points): #tests if (a,b,c) is in the triangulation
    try:
        mid = midpoint(a, b, c)
    except:
        return #this happens a, b and c are in a line (there can't be a midpoint or triangle)

    d = dist(mid, a)

    for p in points:
        if dist(mid, p) < d:
            return False

    return True

def delaunay(points):
    delaunay = [] #will contain all triangles in the triangulation

    #first, we find one triangle and add it to the set
    a = points[0]
    #loop:
    for i in range(1, len(points) - 1):
        b = points[i]
        for j in range(i + 1, len(points)):
            c = points[j]
            if isTriangle(a, b, c, points):
                break# loop

    delaunay.append(set([a,b,c]))

    #each edge in the triangulation is part of one or two triangles
    #so every time we find a new triangle, we add the new edges to toCheck
    toCheck = []
    toCheck.append((a,b))
    toCheck.append((a,c))
    toCheck.append((b,c))
    while len(toCheck) > 0:
        (x,y) = toCheck.pop()
        for z in points:
            if set([x,y,z]) not in delaunay and isTriangle(x, y, z, points):
                delaunay.append(set([x,y,z]))
                toCheck.append((x,z))
                toCheck.append((y,z))
                break

    return delaunay

print(delaunay([(300,300),(300,100),(500,200),(500,400),(100,400),(100,200)]))