from graphics import *
import numpy as np
import math
import time

class p3 :

    focalLength = 0
    width = 0
    height = 0
    unit = 0

    focalPoint = 0
    plane = 0
    origin = 0
    vI = 0
    vJ = 0

    def setup (self) :
        f = self.focalPoint.getA1()
        p = self.plane

        k = -(p[0]*f[0] + p[1]*f[1] + p[2]*f[2] + p[3]) / (p[0]**2 + p[1]**2 + p[2]**2)

        self.origin = np.matrix([[k*p[0]+f[0]],
                                 [k*p[1]+f[1]],
                                 [k*p[2]+f[2]],])
        o = self.origin.getA1()

        self.focalLength = math.sqrt((f[0]-o[0])**2 + (f[1]-o[1])**2 + (f[2]-o[2])**2)

        print('Origin : ' + str(o))

    def __init__ (self, matrix) :
        self.matrix = matrix

    def render (self) :
        flatCoordinates = self.matrix.getA1()
        x = flatCoordinates[0]
        y = flatCoordinates[1]
        z = flatCoordinates[2]

        f = self.focalPoint.getA1()
        p = self.plane

        k = -(p[0]*f[0] + p[1]*f[1] + p[2]*f[2] + p[3]) / (p[0]*x - p[0]*f[0] + p[1]*y - p[1]*f[1] + p[2]*z - p[2]*f[2])

        projectionX = k * (x - f[0]) + f[0]
        projectionY = k * (y - f[1]) + f[1]
        projectionZ = k * (z - f[2]) + f[2]

        pI = self.vI.getA1()
        pJ = self.vJ.getA1()
        pO = self.origin.getA1()

        a = np.matrix([[projectionX - pO[0]],
                       [projectionY - pO[1]]])

        b = np.matrix([[pI[0], pJ[0]],
                       [pI[1], pJ[1]]])
        c = np.linalg.inv(b)

        coords = c * a
        flatCoords = coords.getA1()

        X = flatCoords[0]
        Y = flatCoords[1]

        return Point((X + self.width / 2)*self.unit, (Y + self.height / 2)*self.unit)

    def rotate (self, origin, rotation) :
        self.matrix = origin + rotation * (self.matrix - origin)

    def distance (self, otherPoint) :
        p1 = self.matrix.getA1()
        p2 = otherPoint.matrix.getA1()
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def main ():
    p3.unit = unit = 10
    p3.width  = width = 64
    p3.height = height = 48

    p3.focalPoint = focalPoint = np.matrix([[32], [24], [-30]])
    p3.plane = plane = [0,0,1,0]
    p3.vI = vI = np.matrix([[1.], [0.], [0.]])
    p3.vJ = vJ = np.matrix([[0.], [1.], [0.]])

    p3.setup(p3)

    win = GraphWin("Moteur 3D", width*unit, height*unit)

    #Put black background
    background = Rectangle(Point(0, 0), Point(width*unit, height*unit))
    background.setFill('black')
    background.draw(win)

    cubeCoord = [[[22],[14],[2]], [[42],[14],[2]], [[42],[34],[2]], [[22],[34],[2]], [[22],[14],[22]], [[42],[14],[22]], [[42],[34],[22]], [[22],[34],[22]]]
    cubeNet = [[0,1], [1,2], [2,3], [3,0], [4,5], [5,6], [6,7], [7,4], [0,4], [1,5], [2,6], [3,7]]
    cube = []
    lines = []

    for coord in cubeCoord :
        cube.append(p3(np.matrix(coord)))

    for link in cubeNet :
        line = Line(cube[link[0]].render(), cube[link[1]].render())
        line.setFill("white")
        line.draw(win)
        lines.append(line)

    win.getMouse()


main()
