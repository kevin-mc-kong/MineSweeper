import random


def get_neighbors(mx, my, x, y):
    temp_neighbors = list()

    temp_neighbors.append((mx - 1, my - 1))
    temp_neighbors.append((mx - 1, my))
    temp_neighbors.append((mx - 1, my + 1))

    temp_neighbors.append((mx, my - 1))
    temp_neighbors.append((mx, my + 1))

    temp_neighbors.append((mx + 1, my - 1))
    temp_neighbors.append((mx + 1, my))
    temp_neighbors.append((mx + 1, my + 1))

    neighbors = list()

    for n in temp_neighbors:
        if n[0] >= 0 and n[0] < x and n[1] >= 0 and n[1] < y:
            neighbors.append(n)

    return neighbors


def flag_neighbors(board, mx, my, x, y):
    neighbors = get_neighbors(mx, my, x, y)

    for n in neighbors:
        board[n[0]][n[1]] += 1


def init_mines(board, x, y, num_mines):
    mine_loc = set()

    while len(mine_loc) < num_mines:
        mine_loc.add((random.randint(0, x - 1), random.randint(0, y - 1)))

    for m in mine_loc:
        mx = m[0]
        my = m[1]

        board[mx][my] = -999
        flag_neighbors(board, mx, my, x, y)


def init_board(x, y, num_mines):
    board = []
    for i in xrange(x):
        row = []
        for j in xrange(y):
            row.append(0)

        board.append(row)

    init_mines(board, x, y, num_mines)

    for i in xrange(x):
        for j in xrange(y):
            if board[i][j] < 0:
                board[i][j] = -1

    return board


def reveal_square(board, player_checked, cx, cy, x, y, original_click):
    if board[cx][cy] < 0 and original_click:
        print("Boom!")
        exit(0)

    elif board[cx][cy] == 0:
        player_checked[cx][cy] = 1

        neighbors = get_neighbors(cx, cy, x, y)
        any_numbers = False
        for n in neighbors:
            if board[n[0]][n[1]] < 0:
                any_numbers = True
            elif board[n[0]][n[1]] > 0:
                any_numbers = True
                player_checked[n[0]][n[1]] = 1

        if not any_numbers:
            for n in neighbors:
                if not player_checked[n[0]][n[1]]:
                    reveal_square(board, player_checked, n[0], n[1], x, y, False)


    else:
        player_checked[cx][cy] = 1
        return player_checked
        

def main():
    x = int(input("Insert x dim"))
    y = int(input("Insert y dim"))
    num_m = int(input("How many mines?"))

    assert num_m < x * y

    board = init_board(x, y, num_m)
    player_checked = []
    for i in range(x):
        row = []
        for j in range(y):
            row.append(0)
        player_checked.append(row)

    while(True):
        flag_mode = raw_input("F for flag, any keys for mark")

        if flag_mode == 'F':
            cx = int(input("Insert x coordinate"))
            cy = int(input("Insert y coordinate"))

            if player_checked[cx][cy] == 2:
                player_checked[cx][cy] = 0

            else:
                player_checked[cx][cy] = 2

        else:
            cx = int(input("Insert x coordinate"))
            cy = int(input("Insert y coordinate"))

            reveal_square(board, player_checked, cx, cy, x, y, True)

        for i in range(x):
            row_str = ""
            for j in range(y):
                if player_checked[i][j] == 1:
                    row_str += str(board[i][j]) + " "
                elif player_checked[i][j] == 2:
                    row_str += "F "
                else:
                    row_str += "X "

            print(row_str)


main()