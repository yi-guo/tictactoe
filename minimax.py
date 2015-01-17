################################################################################
## Yi Guo (Partnered with Wesley Saunders)                                    ##
## CS 4397 Computer Game Design                                               ##
## Project 1.3 Minimax Implementation (Python 3.3.2)                          ##
################################################################################

################################################################################
##  To use the following minimax implementation in Wesley Saunders' project,  ##
##  simply replace the whole adversary_turn(S) function in his project with   ##
##                       ALL the content in this file!                        ##
################################################################################

import random

# adversary_turn: GameState -> GameState
# If S is a game state, then adversary_turn(S) is the game state resulting from applying the adversary's one
# of the best moves to S, where the best moves are defined and approached by the minimax algorithm.
def adversary_turn(S):
    if not game_is_over(S):
        S[move(S)] = 'o'
    return S


# The above is to modify Wesley's code that invokes a computer move
# Please make sure the adversary_turn(S) function is his project is replaced by the whole content in this file!

# ================================= Splitter ================================= #

# The following is the implementation of the minimax algorithm


# turn(S): GameState -> string
# If S is a valid game state, regardless of whether S is already a winning game state or whether the board is
# full in S, turn(S) is either 'x' or 'o' corresponding to the play's or the computer's turn respectively.
def turn(S):
    if S.count('x') == S.count('o'):
        return 'x'
    else:
        return 'o'

# minimax(S): GameState -> integer
# If S is a valid game state, minimax(S) is an integer evaluation of S defined by the minimax algorithm below.
#   o If S is a game state in which the player already wins, minimax(S) is 0
#   o If S is a game state in which the computer already wins, minimax(S) is 2
#   o If S is a game state in which the board is full but neither side wins, minimax(S) is 1
#   o If S is a game state beyond the above and it is the player's turn to move, minimax(S) is the minimum of 
#     minimax(C) where C is every possible child game state resulted from applying a legal player move to S.
#   o If S is a game state beyond the above and it is the computer's turn to move, minimax(S) is the maximum of
#     minimax(C) where C is every possible child game state resulted from applying a legal computer move to S.
def minimax(S):
    T = turn(S)
    
    # Return the heuristic directly when S is a leaf node
    if side_won(S, 'o'):
        return 2
    elif side_won(S, 'x'):
        return 0
    elif board_full(S):
        return 1

    # Get all possible moves from S
    moves = []
    for i in range(len(S)):
        if S[i] == 'e':
            moves.append(i)

    # Get all heuristics of the child states of S
    heuristics = []
    # Return the minimum heuristic if it is the play's turn
    if T == 'x':
        for move in moves:
            temp = S[:]
            temp[move] = 'x'
            heuristics.append(minimax(temp))
        return min(heuristics)
    # Otherwise, return the maximum heuristic
    else:
        for move in moves:
            temp = S[:]
            temp[move] = 'o'
            heuristics.append(minimax(temp))
        return max(heuristics)

# move(S): GameState -> integer
# If S is a legal game state and it is the computer's turn to move, then move(S) is a cell representing one of the
# best moves from the current state S for the computer.
def move(S):
    heuristic = minimax(S)
    moves = []
    for i in range(len(S)):
        if S[i] == 'e':
            temp = S[:]
            temp[i] = 'o'
            # If the computer can win in one move, it does
            if side_won(S, 'x') or side_won(S, 'o'):
                return i
            # Otherwise, create a list of the best moves
            if minimax(temp) >= heuristic:
                moves.append(i)
    # Randomly choose one best move
    return random.choice(moves)
