

def game_print(state):
    # prints out the game board somewhat nicely
    output = [".", ".", ".", ".", ".", ".", ".", ".", "."]
    print("#####")
    for i in range(0, 9):
        x_mask = 1 << i
        o_mask = x_mask << 9
        if state & x_mask:
            output[i] = "X"
        elif state & o_mask:
            output[i] = "O"
        else:
            output[i] = "."
    for i in range(0, 3):
        print(output[3 * i] + " " + output[3 * i + 1] + " " + output[3 * i + 2])
    print("#####")


def make_move(state, player, position):
    # check if location is full
    filled_mask = 1 << (position + 18)
    if not state & filled_mask:
        # mark location as filled
        state += filled_mask
        # mark corresponding player array as full
        if player:  # O
            state += 1 << (position + 9)
            return state
        else:  # X
            state += 1 << position
            return state
    return


def evaluate(state, player):
    # iterate through all 3-in-a-row positions
    for i in range(0, 8):
        # if current state matches a position for X
        x_win_state = winning_states[i]
        if (state & x_win_state) == x_win_state:
            if player:
                return -1
            else:
                return 1
        # if current state matches a position for O
        o_win_state = winning_states[i] << 9
        if (state & o_win_state) == o_win_state:
            if player:
                return 1
            else:
                return -1
    # otherwise check if the board is full
    filled_check = 0b111111111 << 18
    if (state & filled_check) == filled_check:
        return 0
    # return 'None' if game is not over
    return


def minimax(board_state, depth, player, alpha, beta, maximizing_player):
    evaluation = evaluate(board_state, player)
    # if depth is exhausted or leaf node (evaluation exists)
    if depth == 0 or evaluation is not None:
        return evaluation
    if maximizing_player:
        v = -1
        # check all positions
        for i in range(0, 9):
            child_state = make_move(board_state, not player ^ maximizing_player, i)
            # if position is valid (not taken)
            if child_state is not None:
                # recursively call minimax with alpha-beta pruning
                v = max(v, minimax(child_state, depth - 1, player, alpha, beta, False))
                alpha = max(alpha, v)
                if beta <= alpha:
                    return 1
        return v
    else:  # minimizing player
        v = 1
        # check all positions
        for i in range(0, 9):
            child_state = make_move(board_state, not player ^ maximizing_player, i)
            # if position is valid (not taken)
            if child_state is not None:
                # recursively call minimax with alpha-beta pruning
                v = min(v, minimax(child_state, depth - 1, player, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    return -1
        return v


# use minimax to find best move and update board
def computer_turn(board_state, comp_player):
    best = -1
    alpha = -1
    beta = 1
    # check move in each location
    for i in range(0, 9):
        child_state = make_move(board_state, comp_player, i)
        # if move is valid perform minimax with alpha-beta pruning
        if child_state is not None:
            v = minimax(child_state, 12, comp_player, alpha, beta, False)
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
        input_temp = input("Location to play (1-9)\n")
        if input_temp.isnumeric():
            if 1 <= int(input_temp) <= 9:
                new_state = make_move(board_state, player, int(input_temp) - 1)
                # check that make_move returned a valid board (not already taken)
                if new_state is not None:
                    return new_state
                else:
                    print("location taken")
            else:
                print("invalid input")
        else:
            print("invalid input")


# all arrangements of three-in-a-row
winning_states = [0b100100100,
                  0b010010010,
                  0b001001001,
                  0b111000000,
                  0b000111000,
                  0b000000111,
                  0b100010001,
                  0b001010100]

# left-most 9 bits filled
# middle 9 bits O
# right-most 9 bits X
# least significant bit of 9 is top-left of board
initial_state = 0b000000000000000000000000000
state = 0b000000000000000000000000000

# main code
if __name__ == "__main__":
    finished = False

    while not finished:

        state = initial_state
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
                state = computer_turn(state, not player)

            # check for game over
            evaluation = evaluate(state, player)
            if evaluation is not None:
                if evaluation == 1:
                    game_print(state)
                    print("Human won")
                elif evaluation == -1:
                    game_print(state)
                    print("Human lost")
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
