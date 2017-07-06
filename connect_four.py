import random
from timeit import default_timer as timer


def game_print(state):
    # prints out the game board somewhat nicely
    print("\n")
    for row in range(0, 6):
        for col in range(0, 7):
            x_mask = 1 << (7 * (5 - row) + col)
            o_mask = x_mask << 42
            if state & x_mask:
                print('X', end=' ')
            elif state & o_mask:
                print('O', end=' ')
            else:
                print('.', end=' ')
        print()
    print("#############")


def make_move(state, player, col):
    # check if column is full
    column_location = 3 * col + 84
    filled_mask = 0b111 << column_location
    row = (state & filled_mask) >> column_location
    if row < 6:
        # mark corresponding player array as full
        if player:  # O
            state += 1 << (7 * row + col + 42)
        else:  # X
            state += 1 << (7 * row + col)
        # increment column state
        state += 1 << column_location
        return state
    return


def evaluate(state, player, depth):
    hori = 0b1111
    vert = 0b1000000100000010000001
    forw = 0b1000000010000000100000001
    back = 0b1000001000001000001
    loss = -1100 - depth
    win = 1100 + depth
    for row in range(0, 6):
        for col in range(0, 7):
            if col <= 3:
                # horizontal
                hori_x = hori << (7 * row + col)
                hori_o = hori << (7 * row + col + 42)
                if (state & hori_x) == hori_x:
                    if player:
                        return loss
                    else:
                        return win
                if (state & hori_o) == hori_o:
                    if player:
                        return win
                    else:
                        return loss
            if row <= 2:
                # vertical
                vert_x = vert << (7 * row + col)
                vert_o = vert << (7 * row + col + 42)
                if (state & vert_x) == vert_x:
                    if player:
                        return loss
                    else:
                        return win
                if (state & vert_o) == vert_o:
                    if player:
                        return win
                    else:
                        return loss
            if row <= 2 and col <= 3:
                # forward diagonal
                forw_x = forw << (7 * row + col)
                forw_o = forw << (7 * row + col + 42)
                if (state & forw_x) == forw_x:
                    if player:
                        return loss
                    else:
                        return win
                if (state & forw_o) == forw_o:
                    if player:
                        return win
                    else:
                        return loss
            if row <= 2 and col >= 3:
                # backward diagonal
                back_x = back << (7 * row + col)
                back_o = back << (7 * row + col + 42)
                if (state & back_x) == back_x:
                    if player:
                        return loss
                    else:
                        return win
                if (state & back_o) == back_o:
                    if player:
                        return win
                    else:
                        return loss
    # otherwise check if the board is full
    filled_check = 0b110110110110110110110 << 84
    if (state & filled_check) == filled_check:
        return 0
    # return 'None' if game is not over
    return


def heuristic_evaluate(state, player):
    return random.randint(-100, 100)


def minimax(board_state, depth, player, alpha, beta, maximizing_player):
    evaluation = evaluate(board_state, player, depth)
    # if depth is exhausted or leaf node (evaluation exists)
    if evaluation is not None:
        return evaluation
    if depth == 0:
        return heuristic_evaluate(board_state, player)
    if maximizing_player:
        v = float('-inf')
        # check all positions
        for i in range(0, 7):
            child_state = make_move(board_state, not player ^ maximizing_player, i)
            # if position is valid (not taken)
            if child_state is not None:
                # recursively call minimax with alpha-beta pruning
                v = max(v, minimax(child_state, depth - 1, player, alpha, beta, False))
                alpha = max(alpha, v)
                if beta <= alpha:
                    return float('inf')
        return v
    else:  # minimizing player
        v = float('inf')
        # check all positions
        for i in range(0, 7):
            child_state = make_move(board_state, not player ^ maximizing_player, i)
            # if position is valid (not taken)
            if child_state is not None:
                # recursively call minimax with alpha-beta pruning
                v = min(v, minimax(child_state, depth - 1, player, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    return float('-inf')
        return v


# use minimax to find best move and update board
def computer_turn(board_state, comp_player):
    best = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    # check move in each location
    for i in range(0, 7):
        child_state = make_move(board_state, comp_player, i)
        # if move is valid perform minimax with alpha-beta pruning
        if child_state is not None:
            v = minimax(child_state, 7, comp_player, alpha, beta, False)
            print(v)
            if v >= best:
                best = v
                best_state = child_state
            alpha = max(alpha, best)
            if beta <= alpha:
                return child_state
    return best_state


# take user input and update board accordingly
def human_turn(board_state, player):
    while True:
        input_temp = input("Location to play (1-7)\n")
        if input_temp.isnumeric():
            if 1 <= int(input_temp) <= 7:
                new_state = make_move(board_state, player, int(input_temp) - 1)
                # check that make_move returned a valid board (not already taken)
                if new_state is not None:
                    return new_state
                else:
                    print("column full")
            else:
                print("invalid input")
        else:
            print("invalid input")


# main code
if __name__ == "__main__":

    finished = False

    while not finished:

        state = 0
        turn = 0
        player = 0

        # pregame
        while True:
            input_temp = input("Play first or second? (1/2)\n")
            if input_temp == "1":
                player = 0
                print("You are player one using Xs")
                break
            elif input_temp == "2":
                player = 1
                print("You are player two using Os")
                break
            else:
                print("invalid input")

        # during game
        while True:
            if turn % 2 == player:
                game_print(state)
                print("Player " + str(player + 1) + "s Turn")
                state = human_turn(state, player)
            else:
                game_print(state)
                print("Player " + str((not player) + 1) + "s Turn")
                start = timer()
                state = computer_turn(state, not player)
                end = timer()
                print('Turn Length ' + str(end - start))

            # check for game over
            evaluation = evaluate(state, player, 0)
            if evaluation is not None:
                if evaluation >= 1000:
                    game_print(state)
                    print("Player 1 (Xs) Wins")
                elif evaluation <= -1000:
                    game_print(state)
                    print("Player 2 (Os) Wins")
                else:
                    game_print(state)
                    print("Draw")
                break
            turn += 1

        # post game
        while True:
            input_temp = input("Play Again? (Y/N)\n")
            if input_temp == "Y" or input_temp == "y":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n#####")
                break
            elif input_temp == "N" or input_temp == "n":
                finished = True
                break
            else:
                print("invalid input")
