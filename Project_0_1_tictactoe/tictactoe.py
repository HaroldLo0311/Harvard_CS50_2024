"""
Tic Tac Toe Player
"""
import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    m , n = 0,0
    for i in board:
        for j in i:
            if j == 'X':
                m += 1
            elif j == 'O':
                n += 1
    if m > n:
        return 'O'
    else:
        return 'X'

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_action = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                possible_action.add((i,j))
    return possible_action

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception('Invalid action!')

    copy_of_board = copy.deepcopy(board)
    copy_of_board[action[0]][action[1]] = player(board)
    return copy_of_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # 1.check winner of row line:
    for i in board:
        if "X" in i and "O" not in i and EMPTY not in i:
            return 'X'
        elif "O" in i and "X" not in i and EMPTY not in i:
            return 'O'

    # 2.check winner of column line:

    m, n = len(board), len(board[0])
    for y in range(m):
        check = []
        for x in range(n):
            check.append(board[x][y])
        if "X" in check and "O" not in check and EMPTY not in check:
            return 'X'
        elif "O" in check and "X" not in check and EMPTY not in check:
            return 'O'

    # 3.check winner of axis diagonal:
    check = []
    x = len(board)
    j, k = 0,0
    for j in range(x):
        check.append(board[j][j])
    if "X" in check and "O" not in check and EMPTY not in check:
        return 'X'
    elif "O" in check and "X" not in check and EMPTY not in check:
        return 'O'
    check = []
    for k in range(x):
        check.append(board[k][x - k - 1])
    if ("X" in check and "O" not in check and EMPTY not in check):
        return 'X'
    elif "O" in check and "X" not in check and EMPTY not in check:
        return 'O'

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == 'X' or winner(board) == 'O':
        return True
    else:
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #if the game already end, return None
    if terminal(board) == True:
        return None
    else:
        #if AI plays X
        #p_action: first move from AI
        p_actions = list(actions(board))
        max_node = 0
        if player(board) == 'X':
            for i in range(len(p_actions)):
                new_board_1 = result(board, p_actions[i])
                #n_action: second move from player
                n_actions = list(actions(new_board_1))
                #find the max score of the current move
                if utility(new_board_1) == 1:
                    return p_actions[i]
                else:
                    min_score = 1
                    #find the min score of the second layer
                    for j in range(len(n_actions)):
                        new_board_2 = result(new_board_1, n_actions[j])
                        # A* algorithm, if there is a -1 then don't have to keep search
                        if utility(new_board_2) == -1:
                            min_score = -1
                            break
                        else:
                            min_score = min(utility(new_board_2), min_score)
                if min_score == 0:
                    max_node = i
            return p_actions[max_node]

        #if AI plays O
        else:
            # p_action: first move from player
            min_node = 0
            for i in range(len(p_actions)):
                new_board_1 = result(board, p_actions[i])
                # n_action: second move from player
                n_actions = list(actions(new_board_1))
                # find the max score of the current move
                if utility(new_board_1) == -1:
                    return p_actions[i]
                else:
                    max_score = -1
                    # find the min score of the second layer
                    for j in range(len(n_actions)):
                        new_board_2 = result(new_board_1, n_actions[j])
                        #A* algorithm, if there is a 1 then don't have to keep search
                        if utility(new_board_2) == 1:
                            max_score = 1
                            break
                        else:
                            max_score = max(utility(new_board_2), max_score)
                if max_score == 0:
                    min_node = i
            return p_actions[min_node]


