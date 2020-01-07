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
[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1])
tetra2 = mTetra([3, 0, 0], [5, 0, 0], [3, 2, 0], [4, 1, 2],
[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1])
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
def obrot(phi, v):
    a = v[0]
    b = v[1]
    c = v[2]
    M = np.array([[a ** 2 * (1 - np.cos(phi)) + np.cos(phi), a * b * (1 - np.cos(phi)) - c * np.sin(phi),
                   a * c * (1 - np.cos(phi)) + b * np.sin(phi)],
                  [a * b * (1 - np.cos(phi)) + c * np.sin(phi), b ** 2 * (1 - np.cos(phi)) + np.cos(phi),
                   b * c * (1 - np.cos(phi)) - a * np.sin(phi)],
                  [a * c * (1 - np.cos(phi)) - b * np.sin(phi), b * c * (1 - np.cos(phi)) + a * np.sin(phi),
                   c ** 2 * (1 - np.cos(phi)) + np.cos(phi)]])
    return M
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

    if key == b"l":
        for j in range(4):
            for i in range(3):
                tetra1[j][i][0] += 0.1

    if key == b"j":
        for j in range(4):
            for i in range(3):
                tetra1[j][i][0] -= 0.1
    if key == b"i":
        for j in range(4):
            for i in range(3):
                tetra1[j][i][1] += 0.1
    if key == b"k":
        for j in range(4):
            for i in range(3):
                tetra1[j][i][1] -= 0.1
    if key == b"o":
        for j in range(4):
            for i in range(3):
                tetra1[j][i][2] += 0.1
    if key == b"u":
        for j in range(4):
            for i in range(3):
                tetra1[j][i][2] -= 0.1


    if key == b"t":
        for j in range(4):
            for i in range(3):
                M = obrot(0.1, [1, 0, 0])
                tetra1[j][i][:3] = np.matmul(M, tetra1[j][i][:3])
    if key == b"g":
        for j in range(4):
            for i in range(3):
                M = obrot(-0.1, [1, 0, 0])
                tetra1[j][i][:3] = np.matmul(M, tetra1[j][i][:3])
    if key == b"f":
        for j in range(4):
            for i in range(3):
                M = obrot(0.1, [0, 1, 0])
                tetra1[j][i][:3] = np.matmul(M, tetra1[j][i][:3])
    if key == b"h":
        for j in range(4):
            for i in range(3):
                M = obrot(-0.1, [0, 1, 0])
                tetra1[j][i][:3] = np.matmul(M, tetra1[j][i][:3])


def prosta(p1, p2):
    if (p1[0] - p2[0]) != 0:
        a = (p1[1] - p2[1]) / (p1[0] - p2[0])
    else:
        a = 0
    b = p1[1] - a * p1[0]
    return a, b, -a, 1, -b
def kol(T1, T2, T1a, T1b, T1c, T2a, T2b, T2c):
    b = [prosta(T1a, T1b)[1], prosta(T1a, T1c)[1], prosta(T1b, T1c)[1]]
    a = [prosta(T1a, T1b)[0], prosta(T1a, T1c)[0], prosta(T1b, T1c)[0]]
    b1 = [prosta(T2a, T2c)[1], prosta(T2a, T2b)[1], prosta(T2b, T2c)[1]]
    a1 = [prosta(T2a, T2c)[0], prosta(T2a, T2b)[0], prosta(T2b, T2c)[0]]
    if a1[0] - a[0] != 0:
        x = (b[0] - b1[0]) / (a1[0] - a[0])
        if max(T2a[1], T2c[1]) >= a1[0] * x + b1[0] >= min(T2a[1], T2c[1]) \
                and min(T2a[0], T2c[0]) <= x <= max(T2a[0], T2c[0]) \
                and max(T1a[1], T1b[1]) >= a1[0] * x + b1[0] >= min(T1a[1], T1b[1]) \
                and min(T1a[0], T1b[0]) <= x <= max(T1a[0], T1b[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1
    if a1[1] - a[0] != 0:
        x = (b[0] - b1[1]) / (a1[1] - a[0])
        if max(T2a[1], T2b[1]) >= a1[1] * x + b1[1] >= min(T2a[1], T2b[1]) \
                and min(T2a[0], T2b[0]) <= x <= max(T2a[0], T2b[0]) \
                and max(T1a[1], T1b[1]) >= a1[1] * x + b1[1] >= min(T1a[1], T1b[1]) \
                and min(T1a[0], T1b[0]) <= x <= max(T1a[0], T1b[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1
    if a1[1] - a[0] != 0:
        x = (b[0] - b1[2]) / (a1[2] - a[0])
        if max(T2b[1], T2c[1]) >= a1[2] * x + b1[2] >= min(T2b[1], T2c[1]) \
                and min(T2b[0], T2c[0]) <= x <= max(T2b[0], T2c[0]) \
                and max(T1a[1], T1b[1]) >= a1[2] * x + b1[2] >= min(T1a[1], T1b[1]) \
                and min(T1a[0], T1b[0]) <= x <= max(T1a[0], T1b[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1

    if a1[0] - a[1] != 0:
        x = (b[1] - b1[0]) / (a1[0] - a[1])
        if max(T2a[1], T2c[1]) >= a1[0] * x + b1[0] >= min(T2a[1], T2c[1]) \
                and min(T2a[0], T2c[0]) <= x <= max(T2a[0], T2c[0]) \
                and max(T1a[1], T1c[1]) >= a1[0] * x + b1[0] >= min(T1a[1], T1c[1]) \
                and min(T1a[0], T1c[0]) <= x <= max(T1a[0], T1c[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1
    if a1[1] - a[1] != 0:
        x = (b[1] - b1[1]) / (a1[1] - a[1])
        if max(T2a[1], T2b[1]) >= a1[1] * x + b1[1] >= min(T2a[1], T2b[1]) \
                and min(T2a[0], T2b[0]) <= x <= max(T2a[0], T2b[0]) \
                and max(T1a[1], T1c[1]) >= a1[1] * x + b1[1] >= min(T1a[1], T1c[1]) \
                and min(T1a[0], T1c[0]) <= x <= max(T1a[0], T1c[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1
    if a1[2] - a[1] != 0:
        x = (b[1] - b1[2]) / (a1[2] - a[1])
        if max(T2b[1], T2c[1]) >= a1[2] * x + b1[2] >= min(T2b[1], T2c[1]) \
                and min(T2b[0], T2c[0]) <= x <= max(T2b[0], T2c[0]) \
                and max(T1a[1], T1c[1]) >= a1[2] * x + b1[2] >= min(T1a[1], T1c[1])\
                and min(T1a[0], T1c[0]) <= x <= max(T1a[0], T1c[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1

    if a1[0] - a[2] != 0:
        x = (b[2] - b1[0]) / (a1[0] - a[2])
        if max(T2a[1], T2c[1]) >= a1[0] * x + b1[0] >= min(T2a[1], T2c[1]) \
                and min(T2a[0], T2c[0]) <= x <= max(T2a[0], T2c[0]) \
                and max(T1b[1], T1c[1]) >= a1[0] * x + b1[0] >= min(T1b[1], T1c[1]) \
                and min(T1b[0], T1c[0]) <= x <= max(T1b[0], T1c[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1
    if a1[1] - a[2] != 0:
        x = (b[2] - b1[1]) / (a1[1] - a[2])
        if max(T2a[1], T2b[1]) >= a1[1] * x + b1[1] >= min(T2a[1], T2b[1]) \
                and min(T2a[0], T2b[0]) <= x <= max(T2a[0], T2b[0]) \
                and max(T1b[1], T1c[1]) >= a1[1] * x + b1[1] >= min(T1b[1], T1c[1]) \
                and min(T1b[0], T1c[0]) <= x <= max(T1b[0], T1c[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1
    if a1[2] - a[2] != 0:
        x = (b[2] - b1[2]) / (a1[2] - a[2])
        if max(T2b[1], T2c[1]) >= a1[2] * x + b1[2] >= min(T2b[1], T2c[1]) \
                and min(T2b[0], T2c[0]) <= x <= max(T2b[0], T2c[0]) \
                and max(T1b[1], T1c[1]) >= a1[2] * x + b1[2] >= min(T1b[1], T1c[1]) \
                and min(T1b[0], T1c[0]) <= x <= max(T1b[0], T1c[0]):
            T2 = [1,0,0]
            T1 = [1, 0, 0]
            return 1
def zderzenie(T1, T2):
    T1a = T1[0][0]
    T1b = T1[0][1]
    T1c = T1[0][2]

    T2a = T2[0][0]
    T2b = T2[0][1]
    T2c = T2[0][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[0][3] = [1,0,0]
        T2[0][3] = [1,0,0]
        return 1

    T1a = T1[1][0]
    T1b = T1[1][1]
    T1c = T1[1][2]

    T2a = T2[1][0]
    T2b = T2[1][1]
    T2c = T2[1][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[1][3] = [1,0,0]
        T2[1][3] = [1,0,0]
        return 1

    T1a = T1[2][0]
    T1b = T1[2][1]
    T1c = T1[2][2]

    T2a = T2[2][0]
    T2b = T2[2][1]
    T2c = T2[2][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[2][3] = [1,0,0]
        T2[2][3] = [1,0,0]
        return 1

    T1a = T1[3][0]
    T1b = T1[3][1]
    T1c = T1[3][2]

    T2a = T2[3][0]
    T2b = T2[3][1]
    T2c = T2[3][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[3][3] = [1,0,0]
        T2[3][3] = [1,0,0]
        return 1

    T1a = T1[0][0]
    T1b = T1[0][1]
    T1c = T1[0][2]

    T2a = T2[3][0]
    T2b = T2[3][1]
    T2c = T2[3][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[0][3] = [1, 0, 0]
        T2[3][3] = [1, 0, 0]
        return 1
    T1a = T1[1][0]
    T1b = T1[1][1]
    T1c = T1[1][2]

    T2a = T2[3][0]
    T2b = T2[3][1]
    T2c = T2[3][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[1][3] = [1, 0, 0]
        T2[3][3] = [1, 0, 0]
        return 1
    T1a = T1[2][0]
    T1b = T1[2][1]
    T1c = T1[2][2]

    T2a = T2[3][0]
    T2b = T2[3][1]
    T2c = T2[3][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[2][3] = [1, 0, 0]
        T2[3][3] = [1, 0, 0]
        return 1
    T1a = T1[0][0]
    T1b = T1[0][1]
    T1c = T1[0][2]

    T2a = T2[2][0]
    T2b = T2[2][1]
    T2c = T2[2][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[0][3] = [1, 0, 0]
        T2[2][3] = [1, 0, 0]
        return 1
    T1a = T1[1][0]
    T1b = T1[1][1]
    T1c = T1[1][2]

    T2a = T2[2][0]
    T2b = T2[2][1]
    T2c = T2[2][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[1][3] = [1, 0, 0]
        T2[2][3] = [1, 0, 0]
        return 1
    T1a = T1[3][0]
    T1b = T1[3][1]
    T1c = T1[3][2]

    T2a = T2[2][0]
    T2b = T2[2][1]
    T2c = T2[2][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[3][3] = [1, 0, 0]
        T2[2][3] = [1, 0, 0]
        return 1
    T1a = T1[0][0]
    T1b = T1[0][1]
    T1c = T1[0][2]

    T2a = T2[1][0]
    T2b = T2[1][1]
    T2c = T2[1][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[0][3] = [1, 0, 0]
        T2[1][3] = [1, 0, 0]
        return 1

    T1a = T1[3][0]
    T1b = T1[3][1]
    T1c = T1[3][2]

    T2a = T2[1][0]
    T2b = T2[1][1]
    T2c = T2[1][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[3][3] = [1, 0, 0]
        T2[1][3] = [1, 0, 0]
        return 1
    T1a = T1[3][0]
    T1b = T1[3][1]
    T1c = T1[3][2]

    T2a = T2[0][0]
    T2b = T2[0][1]
    T2c = T2[0][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[3][3] = [1, 0, 0]
        T2[0][3] = [1, 0, 0]
        return 1

    T1a = T1[1][0]
    T1b = T1[1][1]
    T1c = T1[1][2]

    T2a = T2[0][0]
    T2b = T2[0][1]
    T2c = T2[0][2]

    if kol(T1[1][3], T2[1][3], T1a, T1b, T1c, T2a, T2b, T2c) == 1:
        T1[1][3] = [1, 0, 0]
        T2[0][3] = [1, 0, 0]
        return 1
    return 0

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
    for i in range(4):
        tetra1[i][3] = [0, 0, 1]
        tetra2[i][3] = [0, 0, 1]
    if zderzenie(tetra1, tetra2):
        print("zderzenie")
    else:
        print("")
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