from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import numpy as np

# zmienne pomocnicze
pointSize = 5
windowSize = 200
clearColor = [0.0, 0.0, 0.0]
p = np.array([0.0, 0.0, 0.0])

pixelMapR = [[clearColor[0] for y in range(windowSize)] for x in range(windowSize)]
pixelMapG = [[clearColor[1] for y in range(windowSize)] for x in range(windowSize)]
pixelMapB = [[clearColor[2] for y in range(windowSize)] for x in range(windowSize)]


class OP:  # parametry projekcji
    l = -10
    r = 10
    b = -10
    t = 10
    n = 10
    f = 100


def clearMap(color):
    global pixelMapR, pixelMapG, pixelMapB
    for i in range(windowSize):
        for j in range(windowSize):
            pixelMapR[i][j] = color[0]
            pixelMapG[i][j] = color[1]
            pixelMapB[i][j] = color[2]


# funkcja rysująca zawartość macierzy pixelMap
def paint():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    for i in range(windowSize):
        for j in range(windowSize):
            glColor3f(pixelMapR[i][j], pixelMapG[i][j], pixelMapB[i][j])
            glVertex2f(0.5 + 1.0 * i, 0.5 + 1.0 * j)
    glEnd()
    glFlush()


# inicjalizacja okna
glutInit()
glutInitWindowSize(windowSize*pointSize, windowSize*pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Lab04")
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

# inicjalizacja wyświetlania
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0.0, windowSize, 0.0, windowSize)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glutDisplayFunc(paint)

glutIdleFunc(paint)
glClearColor(1.0, 1.0, 1.0, 1.0)
glEnable(GL_PROGRAM_POINT_SIZE)
glPointSize(pointSize)
pitch = 10
yaw = 15

def cupdate(step = 0.1):
    global tick
    ltime = time.clock()
    if ltime < tick + step:
        return False
    tick = ltime
    return True
def camera(position):
    global front
    front = np.array([np.cos(np.radians(pitch))*np.sin(np.radians(yaw)),
             np.sin(np.radians(pitch)),
             np.cos(np.radians(pitch)) * np.cos(np.radians(yaw))])
    direction = position + front
    len_direction = np.sqrt(direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2)
    if len_direction != 1:
        direction = direction / len_direction

    n = np.array([0, 1, 0])
    right = np.cross(n, direction)
    up = np.cross(direction, right)

    view = np.array([[right[0], right[1], right[2]], [up[0], up[1], up[2]], [direction[0], direction[1], direction[2]]])
    view[0] = view[0] - position[0]
    view[1] = view[1] - position[1]
    view[2] = view[2] - position[2]

    return view

def odcinek(x1, y1, x2, y2, R, G, B): # odcinek w 2d
    global pixelMapR
    global pixelMapG
    global pixelMapB
    if x2 == x1 and y2 == y1:
        x1 = round(x1)
        y1 = round(y1)
        if 0 <= x1 < windowSize:
            if 0 <= y1 < windowSize:
                pixelMapR[int(x1)][int(y1)] = R
                pixelMapR[int(x1)][int(y1)]  = G
                pixelMapR[int(x1)][int(y1)]  = B
        return
    ony = False
    d1 = None
    d2 = None
    if x2 == x1:
        d2 = 0
    elif y2 == y1:
        d1 = 0
    else:
        d2 = (x2 - x1) / (y2 - y1)
        if not -1 < d2 < 1:
            d1 = 1 / d2
    if d1 is not None:
        d = d1
        if x1 > x2:
            xtmp = x1; x1 = x2; x2 = xtmp
            ytmp = y1; y1 = y2; y2 = ytmp
        y = y1 - d
        for x in range(int(round(x1)), int(round(x2)+1)):
            y = y + d
            dcx = x
            dcy = round(y)
            if 0 <= dcx < windowSize:
                if 0 <= dcy < windowSize:
                    pixelMapR[int(dcx)][int(dcy)] = R
                    pixelMapG[int(dcx)][int(dcy)] = G
                    pixelMapB[int(dcx)][int(dcy)] = B
    else:
        d = d2
        if y1 > y2:
            xtmp = x1; x1 = x2; x2 = xtmp
            ytmp = y1; y1 = y2; y2 = ytmp
        x = x1 - d
        for y in range(int(round(y1)), int(round(y2)+1)):
            x = x + d
            dcy = y
            dcx = round(x)
            if 0 <= dcx < windowSize:
                if 0 <= dcy < windowSize:
                    pixelMapR[int(dcx)][int(dcy)] = R
                    pixelMapG[int(dcx)][int(dcy)] = G
                    pixelMapB[int(dcx)][int(dcy)] = B


def punkt(x, y, R, G, B):  # punkt w 2d
    global pixelMapR, pixelMapG, pixelMapB
    if 0 <= x <= windowSize:
        if 0 <= y <= windowSize:
            pixelMapR[x][y] = R
            pixelMapG[x][y] = G
            pixelMapB[x][y] = B


def ortho(p, l, r, b, t, n, f):  # projekcja ortograficzna
    ret = [
        2 * ((p[0] * n - r * p[2]) / (r * p[2] - l * p[2])) + 1,
        2 * ((p[1] * n - t * p[2]) / (t * p[2] - b * p[2])) + 1,
        1 - 2 * ((p[2] - f) / (n - f))]
    return ret


def screen(p, width, height): # przekształcanie na wymiary ekranu
    ret = [(width - 1) * (p[0] + 1) / 2, (height - 1) * (p[1] + 1) / 2]
    return ret


def odcinek3D(p1, p2, R=1, G=1, B=1): # rysowanie odcinka w 3D
    view = np.array(camera(p))
    p1 = view @ p1.T
    p2 = view @ p2.T

    p1 = p1.T
    p2 = p2.T
    p1o = np.array(ortho(p1, OP.l, OP.r, OP.b, OP.t, OP.n, OP.f))
    p2o = np.array(ortho(p2, OP.l, OP.r, OP.b, OP.t, OP.n, OP.f))


    p1s = screen([p1o[0], p1o[1]], windowSize, windowSize)
    p2s = screen([p2o[0], p2o[1]], windowSize, windowSize)
    odcinek(p1s[0], p1s[1], p2s[0], p2s[1], R, G, B)


def szescian(dlugoscboku, psrodek, p0, v, phi):
    p = np.array([[psrodek[0] - dlugoscboku, psrodek[1] - dlugoscboku, psrodek[2] - dlugoscboku],
                  [psrodek[0] + dlugoscboku, psrodek[1] - dlugoscboku, psrodek[2] - dlugoscboku],
                  [psrodek[0] + dlugoscboku, psrodek[1] + dlugoscboku, psrodek[2] - dlugoscboku],
                  [psrodek[0] - dlugoscboku, psrodek[1] + dlugoscboku, psrodek[2] - dlugoscboku],
                  [psrodek[0] - dlugoscboku, psrodek[1] - dlugoscboku, psrodek[2] + dlugoscboku],
                  [psrodek[0] + dlugoscboku, psrodek[1] - dlugoscboku, psrodek[2] + dlugoscboku],
                  [psrodek[0] + dlugoscboku, psrodek[1] + dlugoscboku, psrodek[2] + dlugoscboku],
                  [psrodek[0] - dlugoscboku, psrodek[1] + dlugoscboku, psrodek[2] + dlugoscboku]])

    v_len = np.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if v_len != 1:
        v = v / v_len

    a = v[0]
    b = v[1]
    c = v[2]
    M = np.array([[a ** 2 * (1 - np.cos(phi)) + np.cos(phi), a * b * (1 - np.cos(phi)) - c * np.sin(phi),
                   a * c * (1 - np.cos(phi)) + b * np.sin(phi)],
                  [a * b * (1 - np.cos(phi)) + c * np.sin(phi), b ** 2 * (1 - np.cos(phi)) + np.cos(phi),
                   b * c * (1 - np.cos(phi)) - a * np.sin(phi)],
                  [a * c * (1 - np.cos(phi)) - b * np.sin(phi), b * c * (1 - np.cos(phi)) + a * np.sin(phi),
                   c ** 2 * (1 - np.cos(phi)) + np.cos(phi)]])
    for i in range(len(p)):
        p[i] = p[i] - p0
        p[i] = M @ p[i].T
        p[i] = p[i].T
        p[i] = p[i] + np.array(p0)

    odcinek3D(p[0], p[1])
    odcinek3D(p[1], p[2])
    odcinek3D(p[2], p[3])
    odcinek3D(p[0], p[3])
    odcinek3D(p[4], p[5])
    odcinek3D(p[5], p[6])
    odcinek3D(p[6], p[7])
    odcinek3D(p[4], p[7])
    odcinek3D(p[0], p[4])
    odcinek3D(p[1], p[5])
    odcinek3D(p[2], p[6])
    odcinek3D(p[3], p[7])
akey = 0


camspeed = 0.01
def keyboard(k, x, y):
    global akey
    global yaw
    global pitch
    global p
    global front
    global a
    key = k.decode("utf-8")
    prze = 0.2
    print("p", p)
    print("fron", front)
    if key == 'w':
        p += camspeed * front
    elif key == 's':
        p -= camspeed * front
    elif key == 'q':
        yaw -= 1
    elif key == 'e':
        yaw += 1
    elif key == 'r':
        pitch += 1
    elif key == 'f':
        pitch -= 1




while True:
    clearMap([0.0, 0.0, 0.0])
    glutKeyboardFunc(keyboard)

    # szescian(0.5, [0, 2, 5], 0, 0, 0, 0, 1, 1)
    szescian(5, [2, 2, 30], [2, 3, 5], [1, 2, 3], np.radians(10))
    szescian(3, [-10, -10, 30], [2, 3, 5], [1, 2, 3], np.radians(20))
    szescian(2, [-5, 5, 10], [2, 3, 5], [1, 2, 3], np.radians(0))
    # szescian(0.5, [2, 3, 5], 0, 0, 0, 1, 0, 1)
    # szescian(0.5, [2, 0, 3], 0, 0, 0, 1, 1, 0)
    paint()
    glutMainLoopEvent()
