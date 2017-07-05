from itertools import repeat
from timeit import default_timer as timer
from multiprocessing import Pool


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


def minimax_prep(state):
    v = minimax(state, 12, 0, -1, 1, False)
    return v

# use minimax to find best move and update board
def computer_turn(board_state):
    comp_player = 0
    # game_print(board_state)
    # print("Player " + str(comp_player + 1) + "s Turn")
    best = -1
    alpha = -1
    beta = 1
    # check move in each location
    states = []
    for i in range(0, 9):
        child_state = make_move(board_state, comp_player, i)
        # if move is valid perform minimax with alpha-beta pruning
        if child_state is not None:
            states.append(child_state)
    pool = Pool()
    pool.map(minimax_prep, states)
    pool.close()
    pool.join()
    # if v >= best:
    #     best = v
    #     best_state = child_state
    # return best_state
    return


# use minimax to find best move and update board
def computer_turn_original(board_state):
    comp_player = 0
    best = -1
    alpha = -1
    beta = 1
    # check move in each location
    for i in range(0, 9):
        child_state = make_move(board_state, comp_player, i)
        # if move is valid perform minimax with alpha-beta pruning
        if child_state is not None:
            v = minimax(child_state, 12, comp_player, alpha, beta, False)
            if v >= best:
                best = v
                best_state = child_state
            alpha = max(alpha, best)
            if beta <= alpha:
                return child_state
    return best_state


# all arrangements of three-in-a-row
winning_states = [0b100100100,
                  0b010010010,
                  0b001001001,
                  0b111000000,
                  0b000111000,
                  0b000000111,
                  0b100010001,
                  0b001010100]


if __name__ == "__main__":
    # states = []
    # player = []
    # for i in range(0, 100):
    #     states.append(0)
    #     player.append(0)
    #
    # start = timer()
    # for i in range(0, 100):
    #     computer_turn(0)
    # end = timer()
    # print(end - start)
    #
    # start = timer()
    # pool = Pool()
    # pool.map(computer_turn, states)
    # pool.close()
    # pool.join()
    # end = timer()
    # print(end - start)

    start = timer()
    computer_turn(0)
    end = timer()
    print(end - start)

    start = timer()
    computer_turn_original(0)
    end = timer()
    print(end - start)