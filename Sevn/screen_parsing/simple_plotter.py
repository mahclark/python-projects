import pygame
import time
import colorsys
import pin_pointer
from math import sqrt

# xSize, ySize = 500, 500
cell = 50
xSize, ySize = cell*7, cell*7

cols = pin_pointer.hsv_cols
rgbs = pin_pointer.rgb_cols

def dist(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def next_group(groups):
    for i in range(100):
        if i not in groups:
            return i

    print(groups)
    raise Exception("group error")

threshes = [0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 1]
grouped = []
groups = {0:[0]}
assign = {0:0}

failed = False
try:
    while len(grouped) < 49:

        for i in range(len(cols)):
            if i in grouped: continue
            for j in range(i + 1, len(cols)):
                if j in grouped: continue
                if dist(cols[i], cols[j]) <= threshes[0] and abs(cols[i][2] - cols[j][2]) < 0.5*255:

                    for a, b in [(i, j), (j, i)] if i < j else [(j, i), (i, j)]:
                        if a in assign:
                            if b in assign:
                                if assign[a] != assign[b]:
                                    if len(groups[assign[a]]) + len(groups[assign[b]]) <= 7:
                                        group_to_grow = assign[a]
                                        group_to_delete = assign[b]
                                        for k in groups[group_to_delete]:
                                            assign[k] = group_to_grow
                                        groups[group_to_grow] += groups[group_to_delete].copy()
                                        del groups[group_to_delete]
                                        if len(groups[group_to_grow]) == 7:
                                            grouped += groups[group_to_grow]
                                        break
                                    else:
                                        print(a, b)
                                        print(groups)
                                        print(assign)
                                        raise Exception("group error")
                            elif len(groups[assign[a]]) < 7:
                                assign[b] = assign[a]
                                groups[assign[a]] += [b]
                                if len(groups[assign[a]]) == 7:
                                    grouped += groups[assign[a]]
                                break

                    if i not in assign and j not in assign:
                        group = next_group(groups)
                        assign[i] = group
                        assign[j] = group
                        groups[group] = [i, j]

        del threshes[0]

except Exception as e:
    failed = True
    print(e)

print([rgbs[g[0]] for g in groups.values()])

if __name__ == "__main__":
    screen = pygame.display.set_mode((xSize, ySize))
    pygame.display.set_caption("Pygame Template")

    clock = pygame.time.Clock()
    frameCount = 0
    done = False
    mouseHold = False
    while not done:
        frameCount += 1
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseHold = True
                print((int(1000*mx/xSize)/1000, int(1000*my/ySize)/1000))

            if event.type == pygame.MOUSEBUTTONUP:
                mouseHold = False
                
        screen.fill([255,255,255])

        flash = int((frameCount % 100) / 10)

        if failed:
            for i in range(len(cols)):
                if i in assign and assign[i] == flash: continue
                col = cols[i]
                pygame.draw.circle(screen, colorsys.hsv_to_rgb(col[0], col[1], col[2]), (int(col[0]*xSize), int(col[1]*ySize)), 3)
                # screen.set_at((int(col[0]*xSize), int(col[1]*ySize)), (255,0,0))

        else:
            for y in range(7):
                for x in range(7):
                    rep = groups[assign[y*7 + x]][0]
                    pygame.draw.rect(screen, rgbs[rep], (x*cell, y*cell, cell, cell))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()