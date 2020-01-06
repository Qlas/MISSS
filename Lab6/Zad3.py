from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np
# licznik czasu - do wymuszenia czestotliwosci odswiezania
tick = 0
# parametry kamery
eye = np.array([0., 0., 15.]) # pozycja
orient = np.array([0., 0., -1.]) # kierunek
up = np.array([0., 1., 0.]) # góra
# tworzenie czworoscianów o zadanych wierzchołkach i kolorach
def mTetra(a, b, c, d, col1, col2, col3, col4):
    tetra = []
    face = [a, b, c, col1]; tetra.append(face)
    face = [a, b, d, col2]; tetra.append(face)
    face = [b, c, d, col3]; tetra.append(face)
    face = [c, a, d, col4]; tetra.append(face)
    return tetra
# deklaracje czworoscianów (wierzchołki i kolory scian)
tetra1 = mTetra([0, 0, 0], [2, 0, 0], [0, 2, 0], [1, 1, 2],
[1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 1])
tetra2 = mTetra([3, 0, 0], [5, 0, 0], [3, 2, 0], [4, 1, 2],
[1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 1])
# rysowanie listy trójkatów
def dFacelist(flist):
    for face in flist:
        glColor3fv(face[3])
        glBegin(GL_POLYGON)
        glVertex3fv(face[0])
        glVertex3fv(face[1])
        glVertex3fv(face[2])
        glEnd()
# ruch kamery
def keypress(key, x, y):
    global eye, orient, up
    if key == b"e":
        eye = eye + orient * np.array([0.1, 0.1, 0.1])
    if key == b"q":
        eye = eye - orient * np.array([0.1, 0.1, 0.1])
    if key == b"a":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[np.cos(0.1), 0, np.sin(0.1)], [0, 1, 0],
        [-np.sin(0.1), 0, np.cos(0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
    if key == b"d":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[np.cos(-0.1), 0, np.sin(-0.1)], [0, 1, 0],
        [-np.sin(-0.1), 0, np.cos(-0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
    if key == b"s":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[1, 0, 0], [0, np.cos(0.1), -np.sin(0.1)],
        [0, np.sin(0.1), np.cos(0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
        up = np.matmul(rot, np.array([0, 1, 0]))
        up = np.matmul(inverse, up)
    if key == b"w":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[1, 0, 0], [0, np.cos(-0.1), -np.sin(-0.1)],
        [0, np.sin(-0.1), np.cos(-0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
        up = np.matmul(rot, np.array([0, 1, 0]))
        up = np.matmul(inverse, up)
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

    global eye, orient, up
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 100)
    center = eye + orient
    gluLookAt(eye[0], eye[1], eye[2], center[0], center[1], center[2], up[0], up[1], up[2])
    global tetra1, tetra2
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    dFacelist(tetra1)
    dFacelist(tetra2)
    glFlush()
glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 03")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keypress)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
glutMainLoop()