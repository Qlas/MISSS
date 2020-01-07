from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
from numpy import *

# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0


# klasa pomocnicza, pozwalająca na odwoływanie się do słowników przez notację kropkową
class dd(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# trojkaty
tri1 = {"a": [-4.0, 0.0], "b": [-2.0, 0.0], "c": [-1.0, 2.0],
        "col": [0, 0, 1]}
tri1 = dd(tri1)
tri1.center = [(tri1.a[0] + tri1.b[0] + tri1.c[0]) / 3,
               (tri1.a[1] + tri1.b[1] + tri1.c[1]) / 3]
tri2 = {"a": [-4.0, -4.0], "b": [-2.0, -6.0], "c": [-0.0, -0.0],
        "col": [0, 0, 1]}
tri2 = dd(tri2)
tri2.center = [(tri2.a[0] + tri2.b[0] + tri2.c[0]) / 3,
               (tri2.a[1] + tri2.b[1] + tri2.c[1]) / 3]
# tri3 = {"a":[4.0, 4.0], "b":[2.0, 6.0], "c":[1.0, 1.0],
tri3 = {"a": [4.5, 4.0], "b": [5.0, 4.0], "c": [3.0, 3.0],
        "col": [0, 0, 1]}
tri3 = dd(tri3)
tri3.center = [(tri3.a[0] + tri3.b[0] + tri3.c[0]) / 3,
               (tri3.a[1] + tri3.b[1] + tri3.c[1]) / 3]

color1 = tri1.col
color2 = tri2.col
color3 = tri3.col


# funkcja rysująca trójkąt w 2d
def dtri2f(a, b, c, col):
    glColor3fv(col)
    glBegin(GL_POLYGON)
    glVertex2fv(a);
    glVertex2fv(b);
    glVertex2fv(c)
    glEnd()


# obsługa klawiatury
def keypress(key, x, y):
    global tri3
    if key == b"a": tri3.a[0] -= 0.1; tri3.b[0] -= 0.1; tri3.c[0] -= 0.1
    if key == b"d": tri3.a[0] += 0.1; tri3.b[0] += 0.1; tri3.c[0] += 0.1
    if key == b"w": tri3.a[1] += 0.1; tri3.b[1] += 0.1; tri3.c[1] += 0.1
    if key == b"s": tri3.a[1] -= 0.1; tri3.b[1] -= 0.1; tri3.c[1] -= 0.1
    tri3.center = [(tri3.a[0] + tri3.b[0] + tri3.c[0]) / 3,
                   (tri3.a[1] + tri3.b[1] + tri3.c[1]) / 3]
    if key == b"q": tri3 = rotTri(tri3, 0.1)
    if key == b"e": tri3 = rotTri(tri3, -0.1)


# rotacja trójkąta (uwaga: deformacja przy każdym uruchomieniu)
def rotTri(tri, rot):
    nx = cos(rot) * (tri.a[0] - tri.center[0]) - sin(rot) * (tri.a[1] - tri.center[1]) + tri.center[0]
    ny = sin(rot) * (tri.a[0] - tri.center[0]) + cos(rot) * (tri.a[1] - tri.center[1]) + tri.center[1]
    tri.a[0] = nx;
    tri.a[1] = ny
    nx = cos(rot) * (tri.b[0] - tri.center[0]) - sin(rot) * (tri.b[1] - tri.center[1]) + tri.center[0]
    ny = sin(rot) * (tri.b[0] - tri.center[0]) + cos(rot) * (tri.b[1] - tri.center[1]) + tri.center[1]
    tri.b[0] = nx;
    tri.b[1] = ny
    nx = cos(rot) * (tri.c[0] - tri.center[0]) - sin(rot) * (tri.c[1] - tri.center[1]) + tri.center[0]
    ny = sin(rot) * (tri.c[0] - tri.center[0]) + cos(rot) * (tri.c[1] - tri.center[1]) + tri.center[1]
    tri.c[0] = nx;
    tri.c[1] = ny
    return tri


# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if (ltime < tick + 0.1):  # max 10 ramek / s
        return False
    tick = ltime
    return True


# pętla wyświetlająca
def display():
    if not cupdate():
        return
    global tri1, tri2, tri3

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    dtri2f(tri3.a, tri3.b, tri3.c, tri3.col)
    dtri2f(tri2.a, tri2.b, tri2.c, tri2.col)
    dtri2f(tri1.a, tri1.b, tri1.c, tri1.col)
    tri2 = rotTri(tri2, 0.1)
    txt = "-"

    if zderzenie(tri1, tri3):
        txt += "zderzenie t1 z t3, "

    if zderzenie(tri1, tri2):
        txt += "zderzenie t1 z t2, "

    if zderzenie(tri2, tri3):
        txt += "zderzenie t2 z t3, "
    if zawieranie(tri2, tri3):
        txt += "T2 zawiera sie w T3 "
    if zawieranie(tri3, tri2):
        txt += "T3 zawiera sie w T2 "
    if zawieranie(tri1, tri2):
        txt += "T1 zawiera sie w T2 "
    if zawieranie(tri2, tri1):
        txt += "T2 zawiera sie w T1 "
    if zawieranie(tri1, tri3):
        txt += "T1 zawiera sie w T3 "
    if zawieranie(tri3, tri1):
        txt += "T3 zawiera sie w T1 "
    if zawieranie(tri3, tri1) or zawieranie(tri1, tri3) or zawieranie(tri2, tri1) or zawieranie(tri1,
                                                                                                tri2) or zawieranie(
            tri3, tri2) or zawieranie(tri2, tri3):
        txt += ""
    txt += "\n"
    sys.stdout.write(txt)
    glFlush()


def prosta(p1, p2):
    a = (p1[1] - p2[1]) / (p1[0] - p2[0])
    b = p1[1] - a * p1[0]
    return a, b, -a, -b


def zderzenie(T1, T2):
    b = [prosta(T1.a, T1.b)[1], prosta(T1.a, T1.c)[1], prosta(T1.b, T1.c)[1]]
    a = [prosta(T1.a, T1.b)[0], prosta(T1.a, T1.c)[0], prosta(T1.b, T1.c)[0]]
    b1 = [prosta(T2.a, T2.c)[1], prosta(T2.a, T2.b)[1], prosta(T2.b, T2.c)[1]]
    a1 = [prosta(T2.a, T2.c)[0], prosta(T2.a, T2.b)[0], prosta(T2.b, T2.c)[0]]

    if a1[0] - a[0] != 0:
        x = (b[0] - b1[0]) / (a1[0] - a[0])
        if max(T2.a[1], T2.c[1]) >= a1[0] * x + b1[0] >= min(T2.a[1], T2.c[1]) \
                and max(T1.a[1], T1.b[1]) >= a1[0] * x + b1[0] >= min(T1.a[1], T1.b[1]) \
                and min(T2.a[0], T2.c[0]) <= x <= max(T2.a[0], T2.c[0]) \
                and min(T1.a[0], T1.b[0]) <= x <= max(T1.a[0], T1.b[0]):
            return 1
    if a1[1] - a[0] != 0:
        x = (b[0] - b1[1]) / (a1[1] - a[0])
        if max(T2.a[1], T2.b[1]) >= a1[1] * x + b1[1] >= min(T2.a[1], T2.b[1]) \
                and max(T1.a[1], T1.b[1]) >= a1[1] * x + b1[1] >= min(T1.a[1], T1.b[1]) \
                and min(T2.a[0], T2.b[0]) <= x <= max(T2.a[0], T2.b[0]) \
                and min(T1.a[0], T1.b[0]) <= x <= max(T1.a[0], T1.b[0]):
            return 1
    if a1[2] - a[0] != 0:
        x = (b[0] - b1[2]) / (a1[2] - a[0])
        if max(T2.b[1], T2.c[1]) >= a1[2] * x + b1[2] >= min(T2.b[1], T2.c[1]) \
                and max(T1.a[1], T1.b[1]) >= a1[2] * x + b1[2] >= min(T1.a[1], T1.b[1]) \
                and min(T2.b[0], T2.c[0]) <= x <= max(T2.b[0], T2.c[0]) \
                and min(T1.a[0], T1.b[0]) <= x <= max(T1.a[0], T1.b[0]):
            return 1

    if a1[0] - a[1] != 0:
        x = (b[1] - b1[0]) / (a1[0] - a[1])
        if max(T2.a[1], T2.c[1]) >= a1[0] * x + b1[0] >= min(T2.a[1], T2.c[1]) \
                and max(T1.a[1], T1.c[1]) >= a1[0] * x + b1[0] >= min(T1.a[1], T1.c[1]) \
                and min(T2.a[0], T2.c[0]) <= x <= max(T2.a[0], T2.c[0]) \
                and min(T1.a[0], T1.c[0]) <= x <= max(T1.a[0], T1.c[0]):
            return 1
    if a1[1] - a[1] != 0:
        x = (b[1] - b1[1]) / (a1[1] - a[1])
        if max(T2.a[1], T2.b[1]) >= a1[1] * x + b1[1] >= min(T2.a[1], T2.b[1]) \
                and max(T1.a[1], T1.c[1]) >= a1[1] * x + b1[1] >= min(T1.a[1], T1.c[1]) \
                and min(T2.a[0], T2.b[0]) <= x <= max(T2.a[0], T2.b[0]) \
                and min(T1.a[0], T1.c[0]) <= x <= max(T1.a[0], T1.c[0]):
            return 1
    if a1[2] - a[1] != 0:
        x = (b[1] - b1[2]) / (a1[2] - a[1])
        if max(T2.b[1], T2.c[1]) >= a1[2] * x + b1[2] >= min(T2.b[1], T2.c[1]) \
                and max(T1.a[1], T1.c[1]) >= a1[2] * x + b1[2] >= min(T1.a[1], T1.c[1]) \
                and min(T2.b[0], T2.c[0]) <= x <= max(T2.b[0], T2.c[0]) \
                and min(T1.a[0], T1.c[0]) <= x <= max(T1.a[0], T1.c[0]):
            return 1

    if a1[0] - a[2] != 0:
        x = (b[2] - b1[0]) / (a1[0] - a[2])
        if max(T2.a[1], T2.c[1]) >= a1[0] * x + b1[0] >= min(T2.a[1], T2.c[1]) \
                and max(T1.b[1], T1.c[1]) >= a1[0] * x + b1[0] >= min(T1.b[1], T1.c[1]) \
                and min(T2.a[0], T2.c[0]) <= x <= max(T2.a[0], T2.c[0]) \
                and min(T1.b[0], T1.c[0]) <= x <= max(T1.b[0], T1.c[0]):
            return 1
    if a1[1] - a[2] != 0:
        x = (b[2] - b1[1]) / (a1[1] - a[2])
        if max(T2.a[1], T2.b[1]) >= a1[1] * x + b1[1] >= min(T2.a[1], T2.b[1]) \
                and max(T1.b[1], T1.c[1]) >= a1[1] * x + b1[1] >= min(T1.b[1], T1.c[1]) \
                and min(T2.a[0], T2.b[0]) <= x <= max(T2.a[0], T2.b[0]) \
                and min(T1.b[0], T1.c[0]) <= x <= max(T1.b[0], T1.c[0]):
            return 1
    if a1[2] - a[2] != 0:
        x = (b[2] - b1[2]) / (a1[2] - a[2])
        if max(T2.b[1], T2.c[1]) >= a1[2] * x + b1[2] >= min(T2.b[1], T2.c[1]) \
                and max(T1.b[1], T1.c[1]) >= a1[2] * x + b1[2] >= min(T1.b[1], T1.c[1]) \
                and min(T2.b[0], T2.c[0]) <= x <= max(T2.b[0], T2.c[0]) \
                and min(T1.b[0], T1.c[0]) <= x <= max(T1.b[0], T1.c[0]):
            return 1

    return 0


def zawieranie(T1, T2):
    T2.col = color2
    if (prosta(T1.a, T1.b)[2] * T1.center[0] + T1.center[1] + prosta(T1.a, T1.b)[3]) * (
            prosta(T1.a, T1.b)[2] * T2.center[0] + T2.center[1] + prosta(T1.a, T1.b)[3]) > 0 \
            and (prosta(T1.a, T1.c)[2] * T1.center[0] + T1.center[1] + prosta(T1.a, T1.c)[3]) * (
            prosta(T1.a, T1.c)[2] * T2.center[0] + T2.center[1] + prosta(T1.a, T1.c)[3]) > 0 \
            and (prosta(T1.b, T1.c)[2] * T1.center[0] + T1.center[1] + prosta(T1.b, T1.c)[3]) * (
            prosta(T1.b, T1.c)[2] * T2.center[0] + T2.center[1] + prosta(T1.b, T1.c)[3]) > 0:
        if zderzenie(T1, T2):
            return 0
        else:
            T2.col = [1, 0, 0]
            T1.col = [1, 0, 0]
            return 1

    return 0


glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 02")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)

glutKeyboardFunc(keypress)

glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
# ustaw projekcję ortograficzną
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-10, 10, -10, 10, 15, 20)
gluLookAt(0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
glMatrixMode(GL_MODELVIEW)
glutMainLoop()
