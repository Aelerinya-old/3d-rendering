from graphics import *
import numpy as np
import math
import time

class p3 :

    focalLength = 0
    width = 0
    height = 0
    unit = 0
    win = 0

    def __init__ (self, matrix) :
        self.matrix = matrix

    def render (self) :
        flatCoordinates = self.matrix.getA1()
        x = flatCoordinates[0]
        y = flatCoordinates[1]
        z = flatCoordinates[2]

        dx = self.width/2 - x
        dy = self.height/2 - y
        dz = self.focalLength + z

        X = self.width/2 - (self.focalLength * dx)/dz
        Y = self.height/2 - (self.focalLength * dy)/dz

        #ren = Rectangle(Point(X * self.unit, Y * self.unit), Point((X + 1) * self.unit, (Y + 1) * self.unit))
        #ren.setFill("white")
        #ren.draw(self.win)

        return Point(X * self.unit, Y * self.unit)

    def rotate (self, origin, rotation) :
        self.matrix = origin + rotation * (self.matrix - origin)



def main () :
    quit = False;

    p3.unit = unit =  10
    p3.width  = width = 64
    p3.height = height = 48
    p3.focalLength = focalLength = 20

    p3.win = win = GraphWin("Moteur 3D", width*unit, height*unit)

    #Put black background
    background = Rectangle(Point(0, 0), Point(width*unit, height*unit))
    background.setFill('black')
    background.draw(win)

    cubeCoord = [[[22],[14],[2]], [[42],[14],[2]], [[42],[34],[2]], [[22],[34],[2]], [[22],[14],[22]], [[42],[14],[22]], [[42],[34],[22]], [[22],[34],[22]]]
    cubeNet = [[0,1], [1,2], [2,3], [3,0], [4,5], [5,6], [6,7], [7,4], [0,4], [1,5], [2,6], [3,7]]
    cube = []
    lines = []

    angle = math.pi / 120.0
    center = np.matrix([[32], [24], [12]])
    rotation = np.matrix([[math.cos(angle), 0, math.sin(angle)],
                          [0, 1, 0],
                          [-math.sin(angle), 0, math.cos(angle)]])

    for coord in cubeCoord :
        cube.append(p3(np.matrix(coord)))

    while quit == False :
        for line in lines :
            line.undraw()

        for link in cubeNet :
            line = Line(cube[link[0]].render(), cube[link[1]].render())
            line.setFill("white")
            line.draw(win)
            lines.append(line)

        for point in cube :
            point.rotate(center, rotation)

        input = win.checkKey()

        if input == "Escape" :
            quit = True


        time.sleep(1.0/60)

main()
