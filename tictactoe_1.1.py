################################################################################
## Yi Guo                                                                     ##
## CS 4397 Computer Game Design                                               ##
## Project 01 Tic Tac Toe (Python 3.3.2)                                      ##
################################################################################

################################################################################
##             This project is a fully completed tic-tac-toe game.            ##
##                Run the module to play against the computer!                ##
################################################################################

################################# INTRODUCTION #################################
## This tic-tac-toe game is deisgned on a graphics window sized to 600 pixels ##
## in width and 500 pixels in height. The window is represented by the        ##
## coordinate system with (0,0) located in the lower left corner. In such     ##
## design, x-coordinate increases to the right, and y increases upward.       ##
################################################################################
##   The game board in the PNG file is strictly scaled to 600 x 500 pixels!   ## 
################################################################################

#################################### LAYOUT ####################################
## The explicit layout of the game, which is attached as a PNG file, contains ##
################################################################################
## 1) Grid - sized to 360 x 360 pixels with the lower left corner located at  ##
##           (40,40). The grid is 3 by 3 containing 9 cells with each one     ##
##           occupying 120 x 120 pixels within the grid.                      ##
################################################################################
## 2) Button - two buttons, Play Again and Exit, of the same size of 120 x 40 ##
##             pixels are located to the right of the grid. To be explicit,   ##
##             Play Again: {(x,y) | 440 <= x <= 560, 120 <= y <= 160}         ##
##             Exit:       {(x,y) | 440 <= x <= 560,  60 <= y <= 100}         ##
################################################################################
## 3) Title - the title of "Tic Tac Toe" is bold and centered in the area     ##
##            above the grid where 0 <= x <= 600 and 400 <= y <= 500.         ##
################################################################################
## 4) Record board - displaying game record above the Play Again button. The  ##
##                   location is only given loosely in the attached layout    ##
##                   since it is not a major component.                       ##
################################################################################
## 5) Player board - displaying current players above the record board. The   ##
##                   location is only given loosely in the attached layout    ##
##                   since it is not a major component.                       ##
################################################################################

################################## DATA MODEL ##################################
## A *Point* is a pair (x,y) of floats where 0 <= x <= 600 and 0 <= y <= 500. ##
## Points are interpreted as points in the graphics window introduced above.  ##
################################################################################
## A *Cell* is an integer in the interval [0,8]. Cells represent   0 | 1 | 2  ##
## squares on the tic-tac-toe board as pictured. Given the grid   ----------- ##
## layout introduced above, for example, a legal click at point    3 | 4 | 5  ##
## (x,y) has to satisfy 40 < x < 160 and 280 < y < 400 to be in   ----------- ##   
## cell 0. A detailed cell/button reference table is given below.  6 | 7 | 8  ##
################################################################################
## A *GameState* is a list of nine strings, each of whose members  x |   |    ##
## is either 'x', 'o', or 'e'. The game state S is visualized as  ----------- ##
## a board configuration in which the content of cell i denotes      | o |    ##
## S[i] for 0 <= i <= 8. For example, the game state of           ----------- ##   
## ['x','e','e','e','o','e','e','e','x'] is as pictured.             |   | x  ##
################################################################################

######################### Cell/Button Reference Table ##########################
##      x = 160, x = 280, y = 160, and y = 280 lay the tic-tac-toe grid.      ##
## Please note the difference between an open interval and a closed interval  ##
## used below because CLICKS ON THE GRID ARE INVALID!                         ##
################################################################################
##  Cell/Button |     x     |     y     | Cell/Button |     x     |     y     ##
## -------------------------------------|------------------------------------ ##
##       0      | [ 40,160) | (280,400] |      6      | [ 40,160) | [ 40,160) ## 
##       1      | (160,280) | (280,400] |      7      | (160,280) | [ 40,160) ##
##       2      | (280,400] | (280,400] |      8      | (280,400] | [ 40,160) ##
##       3      | [ 40,160) | (160,280) |      9      | [440,560] | [120,160] ##
##       4      | (160,280) | (160,280) |     10      | [440,560] | [ 60,100] ##
##       5      | (280,400] | (160,280) |             |           |           ##
################################################################################

import random

# winningStates is a list of 8 lists of 3 cells representing the total of 8 different winning combinations
winningStates = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

# initialState: N/A -> GameState
# initialState() is the game state corresponding to an empty board.
def initialState():
    return ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']

# successor: GameState * Point -> GameState
# If S is a game state and P is a point, then successor(S, P) is the game state resulting from
# clicking Point P in GameState S.
# If Point P is illegal, either because the cell that P points at is occupied or because P points at
# somewhere else beyond the grid and the buttons, then successor(S, P) is the game state resulting
# from applying player's next click, which is prompted, to GameState S.
# If Point P points at the Exit button, then successor(S, P) displays the message that says "Exiting"
# and terminates the program.
def successor(S, P):
    click = getClick(P)
    # Point P does not fall into legal area
    if click == -1:
        print("Invalid click! Let's try again.\n")
        return playerMove(S)
    # Point P points at the Play Again button
    elif click == 9:
        print("New Game! Good Luck!\n")
        display(initialState())
        return playerMove(initialState())
    # Point P points at the Exit button
    elif click == 10:
        print("Exiting...\n")
        quit()
    else:
        # Point P points at a cell that is occupied
        if S[click] != 'e':
            print("Invalid click: the cell has been occupied! Let's try again.\n")
            return playerMove(S)
        # Otherwise, update the game state
        else:
            S[click] = 'x'
            return S

# playerMove: GameState -> GameState
# If S is a non-winning game state, then playerMove(S), which prompts for a pair (x,y) of floats
# as a point first, is the game state resulting from clicking the point (x,y) in GameState S.
# If S is a winning game state, then playerMove(S) prints out the message that says "you lose"
# and terminates the program.
def playerMove(S):
    if isWinning(S):
        print("Unfortunately, you lose!\n")
        quit()
    else:
        x = float(input("Enter X: "))
        y = float(input("Enter Y: "))
        print()
        return successor(S, (x, y))

# computerMove: GameState -> GameState
# If S is a non-winning game state and is not full, then computerMove(S) is the game state
# resulting from applying a computer move, depending on GameState S, to GameState S.
# If S is a non-winning game state and is full, then computerMove(S) is GameState S.
# If S is a winning game state, then computerMove(S) prints out the message that says "you win"
# and terminates the program.
def computerMove(S):
    if isWinning(S):
        print("Congratulations! YOU WIN!\n")
        quit()
    elif isFull(S):
        return S
    else:
        # If the computer wins in one move, it does;
        for state in winningStates:
            if S[state[0]] == S[state[1]] and S[state[0]] == 'o' and S[state[2]] == 'e':
                S[state[2]] = 'o'
                return S
            elif S[state[0]] == S[state[2]] and S[state[0]] == 'o' and S[state[1]] == 'e':
                S[state[1]] = 'o'
                return S
            elif S[state[1]] == S[state[2]] and S[state[1]] == 'o' and S[state[0]] == 'e':
                S[state[0]] = 'o'
                return S
        # If the computer has to block, it does;
        for state in winningStates:
            if S[state[0]] == S[state[1]] and S[state[0]] == 'x' and S[state[2]] == 'e':
                S[state[2]] = 'o'
                return S
            elif S[state[0]] == S[state[2]] and S[state[0]] == 'x' and S[state[1]] == 'e':
                S[state[1]] = 'o'
                return S
            elif S[state[1]] == S[state[2]] and S[state[1]] == 'x' and S[state[0]] == 'e':
                S[state[0]] = 'o'
                return S
        # The computer moves in the center if it is empty
        if S[4] == 'e':
            S[4] = 'o'
        # The computer moves in a randomly corner cell if one or more are empty
        elif S[0] == 'e' or S[2] == 'e' or S[6] == 'e' or S[8] == 'e':
            cornerCells = []
            for cell in [0,2,6,8]:
                if S[cell] == 'e':
                    cornerCells.append(cell)
            S[cornerCells[random.randrange(len(cornerCells))]] = 'o'
        # The computer moves in a random empty cell
        else:
            sideCells = []
            for cell in [1,3,5,7]:
                if S[cell] == 'e':
                    sideCells.append(cell)
            S[sideCells[random.randrange(len(sideCells))]] = 'o'
        return S

# getClick: Point -> int
# If P is a point, then getClick(P) is the integer in the interval [-1,10] representing the area on the board
# that P points at, where integers 0-8 correspond to the 8 cells, 9 represents the Play Again button, 10
# represents the Exit button, and -1 indicates that the click is invalid.
def getClick(P):
    click = -1
    if P[0] >= 40 and P[0] < 160:
        if P[1] >= 40 and P[1] < 160:
            click = 6
        elif P[1] > 160 and P[1] < 280:
            click = 3
        elif P[1] > 280 and P[1] <= 400:
            click = 0
    elif P[0] > 160 and P[0] < 280:
        if P[1] >= 40 and P[1] < 160:
            click = 7
        elif P[1] > 160 and P[1] < 280:
            click = 4
        elif P[1] > 280 and P[1] <= 400:
            click = 1
    elif P[0] > 280 and P[0] <= 400:
        if P[1] >= 40 and P[1] < 160:
            click = 8
        elif P[1] > 160 and P[1] < 280:
            click = 5
        elif P[1] > 280 and P[1] <= 400:
            click = 2
    elif P[0] >= 440 and P[0] <= 560:
        if P[1] >= 60 and P[1] <= 100:
            click = 10
        elif P[1] >= 120 and P[1] <= 160:
            click = 9
    return click

# isFull: GameState -> boolean
# If S is a game state, then isFull(S) returns true if the game board in GameState S is full; false otherwise.
def isFull(S):
    for cell in S:
        if cell == 'e':
            return False
    return True

# isWinning: GameSttae -> boolean
# If S is a game state, then isWinning(S) returns true if either the player or the computer wins in GameState S;
# false otherwise.
def isWinning(S):
    for state in winningStates:
        if S[state[0]] == S[state[1]] and S[state[1]] == S[state[2]] and S[state[0]] != 'e':
               return True
    return False

# display: GameState -> N/A
# If S is a game state, then display(S) prints the game board in GameState S to the console.
def display(S):
    cell = {'x': 'x', 'o': 'o', 'e': ' '}
    print(" %s | %s | %s" % (cell[S[0]], cell[S[1]], cell[S[2]]))
    print("-----------")
    print(" %s | %s | %s" % (cell[S[3]], cell[S[4]], cell[S[5]]))
    print("-----------")
    print(" %s | %s | %s" % (cell[S[6]], cell[S[7]], cell[S[8]]))
    print()

# main() starts and drives the game until the game is over, the board is full, or the player exits.
def main():
    try:
        # Starts the game with the initial state
        S = initialState()
        # Continue the game until either wins or the board is full
        while not(isFull(S)):
            display(S)
            S = playerMove(S)
            S = computerMove(S)
        display(S)
        if isWinning(S):
            print("Unfortunately, you lose!\n")
        else:
            print("Draw!\n")
    except:
        print("Hope you had fun. Bye!\n")

main()
