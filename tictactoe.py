def check(arg):
    global game
    count_x = 0
    count_o = 0
    count_ = 0
    x = False
    y = False

    # Counter
    for t in arg:
        for i in t:
            if i == "X":
                count_x += 1
            elif i == "O":
                count_o += 1
            elif i == "_":
                count_ += 1

    # Check X in row
    if arg[0][0] == "X" and arg[0][1] == "X" and arg[0][2] == "X":
        x = True
    elif arg[1][0] == "X" and arg[1][1] == "X" and arg[1][2] == "X":
        x = True
    elif arg[2][0] == "X" and arg[2][1] == "X" and arg[2][2] == "X":
        x = True
    elif arg[0][0] == "X" and arg[1][0] == "X" and arg[2][0] == "X":
        x = True
    elif arg[0][1] == "X" and arg[1][1] == "X" and arg[2][1] == "X":
        x = True
    elif arg[0][2] == "X" and arg[1][2] == "X" and arg[2][2] == "X":
        x = True
    elif arg[0][0] == "X" and arg[1][1] == "X" and arg[2][2] == "X":
        x = True
    elif arg[0][2] == "X" and arg[1][1] == "X" and arg[2][0] == "X":
        x = True

    # Check O in row
    if arg[0][0] == "O" and arg[0][1] == "O" and arg[0][2] == "O":
        y = True
    elif arg[1][0] == "O" and arg[1][1] == "O" and arg[1][2] == "O":
        y = True
    elif arg[2][0] == "O" and arg[2][1] == "O" and arg[2][2] == "O":
        y = True
    elif arg[0][0] == "O" and arg[1][0] == "O" and arg[2][0] == "O":
        y = True
    elif arg[0][1] == "O" and arg[1][1] == "O" and arg[2][1] == "O":
        y = True
    elif arg[0][2] == "O" and arg[1][2] == "O" and arg[2][2] == "O":
        y = True
    elif arg[0][0] == "O" and arg[1][1] == "O" and arg[2][2] == "O":
        y = True
    elif arg[0][2] == "O" and arg[1][1] == "O" and arg[2][0] == "O":
        y = True

    # Check for impossibility
    if count_x - count_o >= 2:
        print("Impossible")
    elif count_o - count_x >= 2:
        print("Impossible")
    elif x and y:
        print("Impossible")

    # Winner check
    if count_ == 0 and x is False and y is False:
        print("Draw")
        game = False
    elif x:
        print("X wins")
        game = False
    elif y:
        print("O wins")
        game = False
    elif count_ != 0:
        game = True


def x_x():
    global t_t_t_l
    global start_
    while True:
        try:
            start_ = list(map(int, input("X turn: ").split()))
            if start_[0] > 3 or start_[0] < 1:
                print("Coordinates should be from 1 to 3!")
                continue
            elif start_[1] > 3 or start_[1] < 1:
                print("Coordinates should be from 1 to 3!")
                continue
            elif start_[2] >= 0 or start_[2] <= 0:
                print("You should enter 2 numbers!")
                continue
        except ValueError:
            print("You should enter numbers!")
            continue
        except IndexError:
            pass
        if t_t_t_l[start_[0] - 1][start_[1] - 1] == "X" or t_t_t_l[start_[0] - 1][start_[1] - 1] == "O":
            print("This cell is occupied! Choose another one!")
        elif t_t_t_l[start_[0] - 1][start_[1] - 1] == "_":
            t_t_t_l[start_[0] - 1][start_[1] - 1] = "X"
            break


def o_o():
    global t_t_t_l
    global start_
    while True:
        try:
            start_ = list(map(int, input("O turn: ").split()))
            if start_[0] > 3 or start_[0] < 1:
                print("Coordinates should be from 1 to 3!")
                continue
            elif start_[1] > 3 or start_[1] < 1:
                print("Coordinates should be from 1 to 3!")
                continue
            elif start_[2] >= 0 or start_[2] <= 0:
                print("You should enter 2 numbers!")
                continue
        except ValueError:
            print("You should enter numbers!")
            continue
        except IndexError:
            pass
        if t_t_t_l[start_[0] - 1][start_[1] - 1] == "X" or t_t_t_l[start_[0] - 1][start_[1] - 1] == "O":
            print("This cell is occupied! Choose another one!")
        elif t_t_t_l[start_[0] - 1][start_[1] - 1] == "_":
            t_t_t_l[start_[0] - 1][start_[1] - 1] = "O"
            break


def print_board():
    global t_t_t_l
    print("---------")
    print("|", t_t_t_l[0][0], t_t_t_l[0][1], t_t_t_l[0][2], "|")
    print("|", t_t_t_l[1][0], t_t_t_l[1][1], t_t_t_l[1][2], "|")
    print("|", t_t_t_l[2][0], t_t_t_l[2][1], t_t_t_l[2][2], "|")
    print("---------")


if __name__ == "__main__":
    game = True
    start_ = list()
    t_t_t_l = [["_________"[i + n] for n in range(3)] for i in range(0, 9, 3)]
    print_board()
    while game:
        x_x()
        print_board()
        check(t_t_t_l)
        if not game:
            break
        o_o()
        print_board()
        check(t_t_t_l)
        if not game:
            break
    input("Press Enter to exit...")
