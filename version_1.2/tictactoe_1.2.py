################################################################################
## Yi Guo                                                                     ##
## CS 4397 Computer Game Design                                               ##
## Project 1.2 Tic Tac Toe (Python 3.3.2)                                      ##
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
        print("Invalid click! Let's try again.")
        return playerMove(S)
    # Point P points at the Play Again button
    elif click == 9:
        print("New Game! Good Luck!")
        return initialState()
    # Point P points at the Exit button
    elif click == 10:
        print("Exiting...")
        quit()
    else:
        # Point P points at a cell that is occupied
        if S[click] != 'e':
            print("Invalid click! The cell has been occupied! Let's try again.")
            return playerMove(S)
        # Otherwise, update the game state
        else:
            S[click] = 'x'
            return S

# playerMove: GameState -> GameState
# If S is a non-winning game state, then playerMove(S), which prompts for a pair (x,y) of floats
# as a point first, is the game state resulting from clicking the point (x,y) in GameState S.
# If S is a winning game state, then playerMove(S) is GameState S.
def playerMove(S):
    if isWinning(S)[0]:
        return S
    else:
        c = display.getMouse()
        P = (c.getX(), displaySize()[1] - c.getY())
        return successor(S, P)

# computerMove: GameState -> GameState
# If S is a non-winning game state and is not full, then computerMove(S) is the game state
# resulting from applying a computer move, depending on GameState S, to GameState S.
# If S is the initial state, a winning game state, or a game state corresponding to a full game board,
# then computerMove(S) is GameState S.
def computerMove(S):
    if isWinning(S)[0] or isFull(S) or S == initialState():
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


# getClick: Point -> integer
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

# isWinning: GameState -> Pair
# If S is a game state, then isWinning(S) is a pair P with P[0] being a boolean value indicating whether
# GameState S is a winning game state and P[1] being a string of either "YOU WIN!" or "You lose!".
# If S is not a winning game state, P[0] is False, and P[1] is an empty string.
def isWinning(S):
    for state in winningStates:
        if S[state[0]] == S[state[1]] and S[state[1]] == S[state[2]]:
            if S[state[0]] == 'x':
                return (True, "Congratulations! YOU WIN!")
            elif S[state[0]] == 'o':
                return (True, 'Unfortunately, you lose!')
    return (False, "")

# displayImages: GameState -> imageList
# If S is a game state, then displayImages(S) is a list containing the images to be displayed on the screen in
# GameState S. Images occurring later in the list overwrites images that occur earlier if they overlap.
def displayImages(S):
    grid = [(160,40,160,400),(280,40,280,400),(40,160,400,160),(40,280,400,280)]
    title = [("Tic Tac Toe", 300, 450, 30)]
    playAgain = [("Play Again", 500, 140, 10),(440,120,440,160),(440,120,560,120),(440,160,560,160),(560,120,560,160)]
    Exit = [("Exit", 500, 80, 10),(440,60,440,100),(440,60,560,60),(440,100,560,100),(560,60,560,100)]
    playerBoard = [("X - Player 1: Human", 500, 360, 12), ("O - Player 2: AI", 482.5, 330, 12)]
    recordBoard = [("Win: ", 490, 275, 10), ("Lose: ", 488.5, 255, 10), ("Draw: ", 487.5, 235, 10)]
    cells = []
    for i in range(len(S)):
        cells = cells + draw(S[i], i)
    return grid + title + playAgain + Exit + playerBoard + recordBoard + cells

# draw: character, integer -> imageList
# If cell is an integer in [0,8] as introduced in the data model and symbol is either 'x' or 'o', then
# draw(symbol, cell) is the image list to draw X/O resectively in the corresponding cell on the game board.
# If symbol is neither 'x' nor 'o', draw(symbol, cell) is an empty image list.
def draw(symbol, cell):
    if symbol == 'x':
        if (cell == 0):
            return [(60,300,140,380),(60,380,140,300)]
        elif (cell == 1):
            return [(180,300,260,380),(180,380,260,300)]
        elif (cell == 2):
            return [(300,300,380,380),(300,380,380,300)]
        elif (cell == 3):
            return [(60,180,140,260),(60,260,140,180)]
        elif (cell == 4):
            return [(180,180,260,260),(180,260,260,180)]
        elif (cell == 5):
            return [(300,180,380,260),(300,260,380,180)]
        elif (cell == 6):
            return [(60,60,140,140),(60,140,140,60)]
        elif (cell == 7):
            return [(180,60,260,140),(180,140,260,60)]
        else:
            return [(300,60,380,140),(300,140,380,60)]
    elif symbol == 'o':
        if (cell == 0):
            return [(100,340,40)]
        elif (cell == 1):
            return [(220,340,40)]
        elif (cell == 2):
            return [(340,340,40)]
        elif (cell == 3):
            return [(100,220,40)]
        elif (cell == 4):
            return [(220,220,40)]
        elif (cell == 5):
            return [(340,220,40)]
        elif (cell == 6):
            return [(100,100,40)]
        elif (cell == 7):
            return [(220,100,40)]
        elif (cell == 8):
            return [(340,100,40)]
        else:
            return [(340,340,40)]
    else:
        return []

# displayConsole: GameState -> N/A
# If S is a game state, then displayConsole(S) prints the game board in GameState S to the console.
def displayConsole(S):
    cell = {'x': 'x', 'o': 'o', 'e': ' '}
    print(" %s | %s | %s" % (cell[S[0]], cell[S[1]], cell[S[2]]))
    print("-----------")
    print(" %s | %s | %s" % (cell[S[3]], cell[S[4]], cell[S[5]]))
    print("-----------")
    print(" %s | %s | %s" % (cell[S[6]], cell[S[7]], cell[S[8]]))
    print()    

######################################################################
######################################################################
# TPGE GAME ENGINE
#
# Student code is linked with this code to create a game.

# displaySize() is the size of the display window, (width, height)

from graphics import *

def displaySize() : return (600,500)

# If x is an image, imageKind(x) is the type of image x is:
# 'circle', 'text', or 'lineSegment'

def imageKind(x):
    if len(x)==3 : return 'circle'
    elif type(x[0])== str :return 'text'
    else : return 'lineSegment'

    
# If x is an image, convert(x) is the corresponding image in the
# graphics.py library. We turn the screen upside down so that the origin
# is in the lower left corner, so it matches what they learn in algebra
# class.

def convert(x):
    if imageKind(x)=='circle': return convertCircle(x)
    elif imageKind(x)=='lineSegment': return convertLine(x)
    elif imageKind(x)=='text' : return convertText(x)


def convertLine(x):
    (W,H) = displaySize()
    P1 = Point(x[0],H - x[1])
    P2 = Point(x[2],H - x[3])
    return Line(P1,P2)

def convertText(x):
    (W,H) = displaySize()
    center = Point(x[1],H-x[2])
    string = x[0]
    size = x[3]
    T = Text(center,string)
    T.setSize(size)
    return T

def convertCircle(x):
    (W,H) = displaySize()
    center = Point(x[0],H-x[1])
    radius = x[2]
    return Circle(center,radius)

# Create a window to play in
display = GraphWin("My game", displaySize()[0], displaySize()[1])

# The main loop
#
# Set the state, draw the display, get a mouse click, set the new state,
# and repeat until the user closes the window.
def main():

    try:
        print("Game start! GOOD LUCK!")
        S = initialState()
        images = [convert(x) for x in displayImages(S)]

        # Main game engine
        while (True):
            for x in images: x.draw(display)
            S = playerMove(S)
            S = computerMove(S)
            for I in images: I.undraw()
            images = [convert(x) for x in displayImages(S)]

            # Determine if winning
            W = isWinning(S)
            if W[0]:
                print(W[1])
            elif isFull(S):
                print("Draw!")

            # If winning or the board is full, wait on player's selection to continue/exit
            while W[0] or isFull(S):
                for I in images: I.undraw()
                for x in images: x.draw(display)
                c = display.getMouse()
                P = (c.getX(), displaySize()[1] - c.getY())
                click = getClick(P)
                if click == 9:
                    S = initialState()
                    for I in images: I.undraw()
                    images = [convert(x) for x in displayImages(S)]
                    print("New Game! Good Luck!")
                    break
                elif click == 10:
                    quit()

    # Capture exceptions by quit()
    except:
        print("Hope you had fun!")
        
main()

