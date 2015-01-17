######################################################################
 ######################################################################
 # TPGE GAME ENGINE
 #
 # Student code is linked with this code to create a game.

 # displaySize() is the size of the display window, (width, height)

 def displaySize() : return (600,500)
 from graphics import *

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

 S = initialState()
 images = [convert(x) for x in displayImages(S)]

 while(True):
     for x in images: x.draw(display)
     c = display.getMouse()
     click = (c.getX(),displaySize()[1] - c.getY())
     S = successor(S,click)
     for I in images: I.undraw()
     images = [convert(x) for x in displayImages(S)]