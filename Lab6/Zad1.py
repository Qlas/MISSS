from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time
# licznik czasu - do wymuszenia czestotliwosci odswiezania
tick = 0
# klasa pomocnicza, pozwalajaca na odwoływanie sie do słowników przez notacje kropkowa
class dd(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# dwa obszary ograniczajace o punktach skrajnych p1 i p3
aabb1 = {"p1":[-2.0, -4.0], "p3":[2.0, 4.0]}; aabb1 = dd(aabb1)
aabb2 = {"p1":[-6.0, -1.0], "p3":[-4.0, 1.0]}; aabb2 = dd(aabb2)
aabbster = {"p1":[-6.0, -1.0], "p3":[-4.0, 1.0]}; aabbster = dd(aabbster)
# funkcja rysujaca jeden obszar ograniczajacy AABB w 2d
def dAABB2f(p1, p3, col):
    p2 = p1[:]; p2[0] = p3[0]
    p4 = p1[:]; p4[1] = p3[1]
    glColor3fv(col)
    glBegin(GL_POLYGON)
    glVertex2fv(p1); glVertex2fv(p2); glVertex2fv(p3); glVertex2fv(p4)
    glEnd()
# funkcja sprawdzajaca warunki zachodzenia na siebie dwóch AABB
def ccAABBtoAABB(p1, p3, q1, q3):
    if (p3[0] < q1[0] or p1[0] > q3[0]): return 0
    if (p3[1] < q1[1] or p1[1] > q3[1]): return 0
    return 1
# wymuszenie czestotliwosci odswiezania
def cupdate():
    global tick
    ltime = time.clock()
    if (ltime < tick + 0.1): # max 10 ramek / s
        return False
    tick = ltime
    return True
# petla wyswietlajaca
def display():
    if not cupdate():
        return
    global aabb1, aabb2, aabbster
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    aabb2.p1[0] += 0.1; aabb2.p3[0] += 0.1
    if (aabb2.p1[0] > 4.0):
        aabb2.p1[0] = -6.0; aabb2.p3[0] = -4.0
    dAABB2f(aabbster.p1, aabbster.p3, [0, 0, 1])
    dAABB2f(aabb2.p1, aabb2.p3, [0, 0.8, 0])
    dAABB2f(aabb1.p1, aabb1.p3, [0, 0.5, 0.5])
    txt = "-"
    if ccAABBtoAABB(aabbster.p1, aabbster.p3, aabb1.p1, aabb1.p3):
        txt += "aabbster x aabb1, "
    if ccAABBtoAABB(aabbster.p1, aabbster.p3, aabb2.p1, aabb2.p3):
        txt += "aabbster x aabb2, "
    txt += "\n"
    sys.stdout.write(txt)
    glFlush()
glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 01")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
# ustaw projekcje ortograficzna
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-10, 10, -10, 10, 15, 20)
gluLookAt(0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
glMatrixMode(GL_MODELVIEW)
def keyboard(k, x, y):
    global aabbster
    key = k.decode("utf-8")
    step = 0.5
    if key == "d":
        aabbster.p1[0] +=step
        aabbster.p3[0] +=step
    elif key == "a":
        aabbster.p1[0] -=step
        aabbster.p3[0] -=step
    elif key == "w":
        aabbster.p1[1] +=step
        aabbster.p3[1] +=step
    elif key == "s":
        aabbster.p1[1] -=step
        aabbster.p3[1] -=step
glutKeyboardFunc(keyboard)
glutMainLoop()