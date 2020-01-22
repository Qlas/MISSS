from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
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
part1.v = [0, 0, 0]
part1.p = [0, 0, 0]
part1.m = 10
part1.r = 1
part1.col = [1, 1, 1]
part1.quad = None

part2 = {}
part2 = dd(part2)
part2.v = [0, 0, 0]
part2.p = [5, 0, 5]
part2.m = 10
part2.r = 1
part2.col = [1, 0, 0]
part2.quad = None

part3 = {}
part3 = dd(part3)
part3.v = [0, 0, 0]
part3.p = [5, 0, -5]
part3.m = 10
part3.r = 1
part3.col = [0, 0, 1]
part3.quad = None

part4 = {}
part4 = dd(part4)
part4.v = [0, 0, 0]
part4.p = [-5, 5, -5]
part4.m = 10
part4.r = 1
part4.col = [0, 1, 1]
part4.quad = None

partcue = {}
partcue = dd(part3)
partcue.v = [0, 0, 0]
partcue.p = [part1.p[0]-2, part1.p[1], part1.p[2]]
partcue.m = 10
partcue.r = 0.50
partcue.col = [0, 0, 0]
partcue.quad = None
flag = 0
flag2 = 0
cuepoint = [part1.p[0]-2, part1.p[1], part1.p[2]]

s = 1
# rysowanie sfery
def drawSphere(part):
    glLoadIdentity()
    glTranslatef(part.p[0], part.p[1], part.p[2])
    glColor3fv(part.col)
    gluSphere(part.quad, part.r, 16, 16)

# rysowanie podłogi
def drawFloor():
    glLoadIdentity()
    glColor3fv([1, 1, 1])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, -10])
    glVertex3fv([-10, 0, 10])
    glVertex3fv([20, 0, 10])
    glVertex3fv([20, 0, -10])
    glEnd()

def drawOther():
    glLoadIdentity()
    glColor3fv([0, 1, 0])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 2, -10])
    glVertex3fv([-10, 0, -10])
    glVertex3fv([20, 0, -10])
    glVertex3fv([20, 2, -10])
    glEnd()

    glLoadIdentity()
    glColor3fv([0, 1, 0])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 2, 10])
    glVertex3fv([-10, 0, 10])
    glVertex3fv([20, 0, 10])
    glVertex3fv([20, 2, 10])
    glEnd()

    glLoadIdentity()
    glColor3fv([1, 0, 0])
    glBegin(GL_POLYGON)
    glVertex3fv([20, 2, -10])
    glVertex3fv([20, 0, -10])
    glVertex3fv([20, 0, 10])
    glVertex3fv([20, 2, 10])
    glEnd()

    glLoadIdentity()
    glColor3fv([1, 0, 0])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 2, -10])
    glVertex3fv([-10, 0, -10])
    glVertex3fv([-10, 0, 10])
    glVertex3fv([-10, 2, 10])
    glEnd()


xx = 5
rad =-1.6
def drawCue():
    global xx
    if flag == 1:
        if partcue.v == [0,0,0]:
            partcue.v=[(part1.p[0] - partcue.p[0])/xx*2,0,(part1.p[2] - partcue.p[2])/xx*2]
        else:
            xx -= 1
    else:
        partcue.p = cuepoint
        partcue.p=[part1.p[0] + xx * np.sin(rad), part1.p[1]+part1.r/2, part1.p[2] + xx*cos(rad)]
    if flag != 2 and part1.v == [0,0,0]:
        drawSphere(partcue)
        updateSphere(partcue, 0.5)
        glLoadIdentity()
        glColor3fv([0, 0, 0])
        glBegin(GL_POLYGON)
        glVertex3fv([part1.p[0] + xx * np.sin(rad), 1, part1.p[2] + xx * cos(rad - 0.05)])
        glVertex3fv([part1.p[0] + xx * np.sin(rad), 2, part1.p[2] + xx * cos(rad - 0.05)])
        glVertex3fv([part1.p[0] + (xx+10) * np.sin(rad), 2, part1.p[2] + (xx+10)*cos(rad - 0.05)])
        glVertex3fv([part1.p[0] + (xx+10) * np.sin(rad), 1, part1.p[2] + (xx+10)*cos(rad - 0.05)])
        glEnd()

        glLoadIdentity()
        glColor3fv([0, 0, 0])
        glBegin(GL_POLYGON)
        glVertex3fv([part1.p[0] + xx * np.sin(rad), 1, part1.p[2] + xx * cos(rad + 0.05)])
        glVertex3fv([part1.p[0] + xx * np.sin(rad), 2, part1.p[2] + xx * cos(rad + 0.05)])
        glVertex3fv([part1.p[0] + (xx+10) * np.sin(rad), 2, part1.p[2] + (xx+10)*cos(rad+0.05)])
        glVertex3fv([part1.p[0] + (xx+10) * np.sin(rad), 1, part1.p[2] + (xx+10)*cos(rad+0.05)])
        glEnd()


        glLoadIdentity()
        glColor3fv([0, 0, 0])
        glBegin(GL_POLYGON)
        glVertex3fv([part1.p[0] + xx * np.sin(rad), 1, part1.p[2] + xx*cos(rad+0.05)])
        glVertex3fv([part1.p[0] + xx * np.sin(rad), 1, part1.p[2] + xx*cos(rad-0.05)])
        glVertex3fv([part1.p[0] + (xx+10) * np.sin(rad), 1, part1.p[2] + (xx+10)*cos(rad-0.05)])
        glVertex3fv([part1.p[0] + (xx+10) * np.sin(rad), 1, part1.p[2] + (xx+10)*cos(rad+0.05)])
        glEnd()


        glLoadIdentity()
        glColor3fv([0, 0, 0])
        glBegin(GL_POLYGON)
        glVertex3fv([part1.p[0] + xx * np.sin(rad), 2, part1.p[2] + xx*cos(rad+0.05)])
        glVertex3fv([part1.p[0] + xx * np.sin(rad), 2, part1.p[2] + xx*cos(rad-0.05)])
        glVertex3fv([part1.p[0] + (xx+10) * np.sin(rad), 2, part1.p[2] + (xx+10)*cos(rad-0.05)])
        glVertex3fv([part1.p[0] + (xx+10) * np.sin(rad), 2, part1.p[2] + (xx+10)*cos(rad+0.05)])
        glEnd()
# ruch sfery
flag3 = 0
def updateSphere(part, dt):
    # tutaj trzeba dodać obsługę sił, w tym grawitacji
    if flag3 == 0:
        part.p[0] += dt * part.v[0]
        part.p[1] += dt * part.v[1]
        part.p[2] += dt * part.v[2]

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
    if part.p[0] + part.r > 20:
        return True
# obsługa kolizji
def updateSphereCollision(part):
    if checkSphereToxCollision(part):
        if part.p[0] - part.r < 0:
            part.p[0] = -10 + part.r
        if part.p[0] + part.r > 10:
            part.p[0] = 20 - part.r
        part.v[0] = - part.v[0]
    if checkSphereTozCollision(part):
        if part.p[2] - part.r < 0:
            part.p[2] = -10 + part.r
        if part.p[2] + part.r > 10:
            part.p[2] = 10 - part.r
        part.v[2] = - part.v[2]
    if checkSphereToFloorCollision(part):
        # jeśli sfera zachodzi pod podłogę, to podnieś ją
        if part.p[1] - part.r < 0:
            part.p[1] = part.r
        if part.p[1] + part.r > 10:
            part.p[1] = 20 - part.r
        # u = -part.v[1] + s / part.m
        part.v[1] = 0

# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1: # max 10 ramek / s
        return False
    tick = ltime
    return True

def sfereColl(sphere0, sphere1):
    global flag3
    r0sqr = sphere0.r * sphere0.r
    r1sqr = sphere1.r * sphere1.r

    distX = sphere0.p[0] - sphere1.p[0]
    distY = sphere0.p[1] - sphere1.p[1]
    distZ = sphere0.p[2] - sphere1.p[2]

    distSqrX = distX**2
    distSqrY = distY**2
    distSqrZ = distZ**2

    sqrDist = np.sqrt(distSqrX + distSqrY + distSqrZ)
    if r0sqr + r1sqr >= sqrDist:
        flag3 = 1
        totalRadius = sphere0.r + sphere1.r
        if totalRadius < 2:
            totalRadius = 2.5
        dist = sqrt(sqrDist)
        minMovement = (totalRadius - dist)
        minMovement /= dist
        mvmtX = distX * minMovement * 1
        mvmtY = distY * minMovement * 1
        mvmtZ = distZ * minMovement * 1


        glLineWidth(2.5)
        glColor3f(1,0,0)
        glBegin(GL_LINES)
        glVertex3f(sphere0.p[0], sphere0.p[1], sphere0.p[2])
        glVertex3f(sphere0.p[0]+mvmtX*5, sphere0.p[1], sphere0.p[2]+mvmtZ*5)
        glEnd()

        print(mvmtX, mvmtY, mvmtZ)
        glLineWidth(2.5)
        glColor3f(0,1,0)
        glBegin(GL_LINES)
        glVertex3f(sphere1.p[0], sphere1.p[1], sphere1.p[2])
        glVertex3f(sphere1.p[0]-mvmtX*5, sphere1.p[1], sphere1.p[2]-mvmtZ*5)
        glEnd()
        if sphere0.v[0] != 0 or sphere1.v[0] != 0:
            if sphere0.p[0] < sphere1.p[0]:
                # sphere0.p[0] -= mvmtX
                # sphere1.p[0] += mvmtX
                sphere0.v[0] = mvmtX * s
                sphere1.v[0] = -  mvmtX * s
            elif sphere0.p[0] > sphere1.p[0]:
                # sphere0.p[0] += mvmtX
                # sphere1.p[0] -= mvmtX
                sphere0.v[0] = mvmtX * s
                sphere1.v[0] = - mvmtX * s

        if sphere0.v[2] != 0 or sphere1.v[2] != 0:
            if sphere0.p[2] < sphere1.p[2]:
                # sphere0.p[2] -= mvmtZ
                # sphere1.p[2] += mvmtZ
                sphere0.v[2] = mvmtZ * s
                sphere1.v[2] = - mvmtZ * s
            elif sphere0.p[2] > sphere1.p[2]:
                # sphere0.p[2] += mvmtZ
                # sphere1.p[2] -= mvmtZ
                sphere0.v[2] = mvmtZ * s
                sphere1.v[2] = - mvmtZ * s

        if sphere0.v[1] != 0 or sphere1.v[1] != 0:
            if sphere0.p[1] <= sphere1.p[1]:
                # sphere1.p[1] -= mvmtY
                if sphere0.p[0] < sphere1.p[0]:
                    sphere0.v[0] = mvmtY * s
                    sphere1.v[0] = - mvmtY * s
                else:
                    if sphere0.v[0] == 0:
                        sphere0.v[0] = mvmtZ
                    if sphere1.v[0] == 0:
                        sphere1.v[0] = -mvmtZ
                    sphere0.v[0] = mvmtY
                    sphere1.v[0] = - mvmtY
                # sphere0.v[1] = - sphere0.v[1]
                # sphere1.v[1] = - sphere1.v[1]
                if sphere0.p[2] <= sphere1.p[2]:
                    sphere0.v[2] = mvmtY * s
                    sphere1.v[2] = - mvmtY * s
                else:
                    if sphere0.v[2] == 0:
                        sphere0.v[2] = mvmtY * s
                    if sphere1.v[2] == 0:
                        sphere1.v[2] = - mvmtY * s
                    sphere0.v[2] = mvmtY * s
                    sphere1.v[2] = - mvmtY * s
            else:
                pass
        return True
                # sphere0.p[1] += mvmtY
                # sphere1.p[1] -= mvmtY
                # sphere0.v[1] = - sphere0.v[1]
                # sphere1.v[1] = - sphere1.v[1]


# pętla wyświetlająca
def display():
    if not cupdate():
        return
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 100)
    gluLookAt(-5, 15, 0, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    global part1, part2, part3, part4, partcue, flag, flag2
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    updateSphere(part1, 0.5)
    updateSphereCollision(part1)
    updateSphere(part2, 0.5)
    updateSphereCollision(part2)
    updateSphere(part3, 0.5)
    updateSphereCollision(part3)
    updateSphere(part4, 0.5)
    updateSphereCollision(part4)
    if flag2 == 1:
        print("a")
        part4.p[0] = part1.p[0]+part1.v[0]+1
        part4.p[2] = part1.p[2]+part1.v[2]+1
        part4.p[1] = 5
        part4.v = [0,-2,0]
        flag2 = 2
    drawFloor()
    drawOther()
    drawCue()
    sfereColl(part1, part2)
    sfereColl(part1, part4)
    sfereColl(part2, part4)
    sfereColl(part3, part4)
    sfereColl(part1, part3)
    sfereColl(part2, part3)

    if sfereColl(part1, partcue):
        flag = 2
    drawSphere(part1)
    drawSphere(part2)
    drawSphere(part3)
    if flag2 == 2:
        drawSphere(part4)
    glFlush()

def keypress(k, x, y):
    global s, rad, flag, flag2, flag3
    key = k.decode("utf-8")
    if key == "i":
        s += 0.1
    elif key == "j":
        s -= 0.1
    elif key == "q":
        rad -= 0.1
    elif key == "e":
        rad += 0.1
    elif key == "t" and flag == 0:
        flag = 1
    elif key == "p":
        flag2 = 1
    elif key == "b":
        flag3 = 0

glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 05")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)
glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
# przygotowanie oświetlenia
glEnable(GL_LIGHT0)
glLight(GL_LIGHT0, GL_POSITION, [0., 5., 5., 0.])
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glutKeyboardFunc(keypress)
# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
# przygotowanie sfery
part1.quad = gluNewQuadric()
part2.quad = gluNewQuadric()
part3.quad = gluNewQuadric()
part4.quad = gluNewQuadric()
partcue.quad = gluNewQuadric()
gluQuadricNormals(part1.quad, GLU_SMOOTH)
glutMainLoop()
