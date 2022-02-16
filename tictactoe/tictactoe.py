"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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

    # Count how many X and O are in the game
    X_counter = 0
    O_counter = 0

    for i in range(len(board)):
        X_counter = X_counter + int(board[i].count(X))
        O_counter = O_counter + int(board[i].count(O))

    if X_counter > O_counter:
        return O

    else:
        return X

def actions(board):

    possibilities = set()

    # A loop that goes through the matrix and find EMPTY spaces
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                possibilities.add((i,j))
    
    return possibilities

def result(board, action):
    
    board_copy = deepcopy(board)

    if board_copy[action[0]][action[1]] is not EMPTY:
        raise Exception
    else:
        board_copy[action[0]][action[1]] = player(board_copy)
    
    return board_copy

def winner(board):
    X_moves = []
    O_moves = []
    
    # Take the all moves of each player
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                X_moves.append((i, j))
            elif board[i][j] == O:
                O_moves.append((i, j))
    
    # Create a dic to store each play of the players
    players = { 'X': {'vertical': [],
                    'horizontal': []},
                'O': {'vertical': [],
                    'horizontal': []}
            }
    
    # Two lists with the possiblities to diagonal
    diagonal1 = [(0, 0), (1, 1), (2, 2)] 
    diagonal2 = [(0, 2), (1, 1), (2, 0)]
    
    # Check if the X won at any diagonal
    if set(diagonal1).issubset(set(X_moves)) or set(diagonal2).issubset(set(X_moves)):
        return X
    
    # Check if the O won at any diagonal
    if set(diagonal1).issubset(set(O_moves)) or set(diagonal2).issubset(set(O_moves)):
        return O
    
    # Separate horizontal and vertifcal moves X player
    for move in X_moves:
        players['X']['horizontal'].append(move[0])
        players['X']['vertical'].append(move[1])
        
    # Separate horizontal and vertifcal moves O player
    for move in O_moves:
        players['O']['horizontal'].append(move[0])
        players['O']['vertical'].append(move[1])
    
    # Check if any player won at vertical or horizontal
    for player in players:
        for i in range(3):
            if players[player]['horizontal'].count(i) == 3:
                return player
            if players[player]['vertical'].count(i) ==  3:
                return player
    
    return None

def terminal(board):

    if winner(board) is not None:
        return True
    
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False

    return True

def utility(board):

    # Get the winner in a variable
    champion = winner(board)

    if champion == X:
        return 1
            
    elif champion == O:
        return -1

    return 0

def min_value(board):
    
    v = float('+inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v

def max_value(board):

    v = float('-inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v

def minimax(board):
    
    if terminal(board):
        return None
    
    actual_player = player(board)

    possibilities = actions(board)

    if actual_player == X:
        # Get the max value
        max_v = float('-inf')

        for action in possibilities:
            # Makes the X next move
            temp_board = result(board, action)

            # See what the enemy is going to do
            v = min_value(temp_board)

            if v > max_v:
                # Take the best play
                max_v = v
                final_action = action   

    else:
        # Get the minimum value 
                # Get the max value
        min_v = float('+inf')

        for action in possibilities:
            # Makes the O next move
            temp_board = result(board, action)

            # See what the enemy is going to do
            v = max_value(temp_board)

            if v < min_v:
                # Take the best play
                min_v = v
                final_action = action   

    return final_action
