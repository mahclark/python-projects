import csv

def make_board(inp):
    board = [[],[],[],[],[],[],[]]
    for row in range(7):
        for col in range(7):
            for i in range(8):
                if inp[row*56 + col*8 + i] == 1:
                    board[row].append(i - 1)
                    break

    return board

def pos_moves(board):
    exposed = [0, 0, 0, 0, 0, 0, 0]
    for row in range(7):
        for col in range(7):
            p = get(board, col, row)
            if p != -1:
                up = get(board, col, row - 1) == -1
                dn = get(board, col, row + 1) == -1
                lf = get(board, col - 1, row) == -1
                rt = get(board, col + 1, row) == -1

                if up + dn + lf + rt > 2:
                    exposed[p] += 1
                elif up + dn + lf + rt == 2:
                    if not (up and dn) and not (lf and rt):
                        exposed[p] += 1

    return sum([2**n - 1 for n in exposed])

def get(board, x, y):
    if x < 0 or y < 0 or x > 6 or y > 6:
        return -1
    else:
        return board[y][x]

def undo_first(board):
    count = 0
    s = [0,0,0,0,0,0,0,0]
    for row in range(7):
        for col in range(7):
            s[board[row][col] + 1] += 1
            if board[row][col] == -1 and not (row in [0, 6] and col in [0, 6]):
                return None

    if s[0] > 4:
        return None

    col = None
    for i, n in enumerate(s[1:]):
        if n < 7:
            if col != None:
                return None
            col = i

    if col == None:
        return None

    board2 = board.copy()
    for y, x in [(0,0),(0,6),(6,0),(6,6)]:
        if board2[y][x] == -1:
            board2[y][x] = col

    return board2

if __name__ == "__main__":
    spread = []
    for folder in [399, 402, 403, 410]:
        for num in range(93):
            try:
                one_count = 0
                with open('data/{0}/trainging_set_{1}_x.csv'.format(folder, num)) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')

                    for row in csv_reader:
                        board = make_board([float(i) for i in row])
                        n = pos_moves(board)

                        if len(spread) <= n:
                            for _ in range(n - len(spread) + 1):
                                spread.append(0)
                        spread[n] += 1

                        board2 = undo_first(board)
                        if board2:
                            if one_count == 0:
                                n = pos_moves(board2)
                                if len(spread) <= n:
                                    for _ in range(n - len(spread) + 1):
                                        spread.append(0)
                                spread[n] += 1               
                            one_count += 1
                            if one_count > 4:
                                one_count = 0
                print(str(folder) + " no. " + str(num))
            except FileNotFoundError:
                break

    print("Results:")
    for s in spread:
        print(s)
