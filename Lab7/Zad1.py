from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import random
import numpy as np
# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0
# klasa pomocnicza, pozwalająca na odwoływanie się do słowników przez notację kropkową
class dd(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
part1 = {}
part1 = dd(part1)
part1.v = [0, -1, 0]
part1.p = [-5, 2, 3]
part1.m = 10
part1.r = 1
part1.col = [0, 0.5, 0]
part1.quad = None
s = 1
pos = [-5.0, 5.0, 10.0]
g = 0
o = 0
# rysowanie sfery
def drawSphere(part):
    glLoadIdentity()
    glTranslatef(part.p[0], part.p[1], part.p[2])
    glColor3fv(part.col)
    gluSphere(part.quad, part.r, 16, 16)

# rysowanie podłogi
def drawFloor():
    glLoadIdentity()
    glColor3fv([0.3, 0.3, 0.3])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, -10])
    glVertex3fv([-10, 0, 10])
    glVertex3fv([10, 0, 10])
    glVertex3fv([10, 0, -10])
    glEnd()

# rysowanie podłogi
def drawOther():
    glLoadIdentity()
    glColor3fv([0, 1, 0])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 10, -10])
    glVertex3fv([-10, 0, -10])
    glVertex3fv([10, 0, -10])
    glVertex3fv([10, 10, -10])
    glEnd()

    glLoadIdentity()
    glColor3fv([0, 1, 0])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 10, 10])
    glVertex3fv([-10, 0, 10])
    glVertex3fv([10, 0, 10])
    glVertex3fv([10, 10, 10])
    glEnd()

    glLoadIdentity()
    glColor3fv([1, 0, 0])
    glBegin(GL_POLYGON)
    glVertex3fv([10, 10, -10])
    glVertex3fv([10, 0, -10])
    glVertex3fv([10, 0, 10])
    glVertex3fv([10, 10, 10])
    glEnd()

    glLoadIdentity()
    glColor3fv([1, 0, 0])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 10, -10])
    glVertex3fv([-10, 0, -10])
    glVertex3fv([-10, 0, 10])
    glVertex3fv([-10, 10, 10])
    glEnd()

    glLoadIdentity()
    glColor3fv([0, 0, 1])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 10, -10])
    glVertex3fv([-10, 10, 10])
    glVertex3fv([10, 10, 10])
    glVertex3fv([10, 10, -10])
    glEnd()

# ruch sfery
def updateSphere(part, dt):
    # tutaj trzeba dodać obsługę sił, w tym grawitacji
    part.p[0] += dt * part.v[0]
    part.p[1] += dt * part.v[1]
    part.p[2] += dt * part.v[2]

    print(part.v)
    if part.v[1] > 0:
        part.v[1] -= g
    else:
        part.v[1] -= g
    if abs(part.v[0]) > o:
        if part.v[0] >0:
            part.v[0] -= o
        else:
            part.v[0] += o
    if abs(part.v[1]) > o:
        if part.v[1] >0:
            part.v[1] -= o
        else:
            part.v[1] += o
    if abs(part.v[2]) > o:
        if part.v[2] >0:
            part.v[2] -= o
        else:
            part.v[2] += o

# sprawdzenie czy doszło do kolizji
def checkSphereToFloorCollision(part):
    if part.p[1] - part.r < 0:
        return True
    if part.p[1] + part.r > 10:
        return True

def checkSphereTozCollision(part):
    if part.p[2] - part.r < -10:
        return True
    if part.p[2] + part.r > 10:
        return True

def checkSphereToxCollision(part):
    if part.p[0] - part.r < -10:
        return True
    if part.p[0] + part.r > 10:
        return True

# obsługa kolizji
def updateSphereCollision(part):
    if checkSphereToxCollision(part1):
        if part.p[0] - part.r < 0:
            part.p[0] = -9
        if part.p[0] + part.r > 10:
            part.p[0] = 9
        part.v[0] = - part.v[0] * s
    if checkSphereTozCollision(part1):
        if part.p[2] - part.r < 0:
            part.p[2] = -9
        if part.p[2] + part.r > 10:
            part.p[2] = 9
        part.v[2] = - part.v[2] * s
    if checkSphereToFloorCollision(part1):
        # jeśli sfera zachodzi pod podłogę, to podnieś ją
        if part.p[1] - part.r < 0:
            part.p[1] = part.r
        if part.p[1] + part.r > 10:
            part.p[1] = 9
        # u = -part.v[1] + s / part.m
        part.v[1] = - part.v[1] * s

# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1: # max 10 ramek / s
        return False
    tick = ltime
    return True
# pętla wyświetlająca
def display():
    if not cupdate():
        return
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 100)
    gluLookAt(pos[2], pos[1], pos[0], 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    global part1
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    drawFloor()
    drawOther()
    updateSphere(part1, 0.1)
    updateSphereCollision(part1)

    drawSphere(part1)
    glFlush()

def keypress(k, x, y):
    global s, pos, g, o
    key = k.decode("utf-8")
    if key == "i":
        s += 0.1
    elif key == "j":
        s -= 0.1
    elif key == "w":
        pos[1] += 1
    elif key == "s":
        pos[1] -= 1
    elif key == "a":
        pos[2] += 1
    elif key == "d":
        pos[2] -= 1
    elif key == "e":
        pos[0] += 1
    elif key == "q":
        pos[0] -= 1
    elif key == "z":
        r = random.randint(0,2)
        if part1.v[r] > 0:
            part1.v[r] += 50
        else:
            part1.v[r] -= 50
    elif key == "x":
        g += 0.001
    elif key == "c":
        g -= 0.001
    elif key == "n":
        o += 0.001
    elif key == "m":
        o -= 0.001


glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 05")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glutKeyboardFunc(keypress)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
# przygotowanie oświetlenia
glEnable(GL_LIGHT0)
glLight(GL_LIGHT0, GL_POSITION, [0., 5., 5., 0.])
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
# przygotowanie sfery
part1.quad = gluNewQuadric()
gluQuadricNormals(part1.quad, GLU_SMOOTH)
glutMainLoop()
