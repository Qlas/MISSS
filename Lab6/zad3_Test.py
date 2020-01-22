from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np

# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0

# paramer koloru do kolizji
col = 0
# parametry kamery
eye = np.array([0, 0, 15])  # pozycja
orient = np.array([0, 0, -1])  # kierunek
up = np.array([0, 1, 0])  # góra


# tworzenie czworoscianów o zadanych wierzchołkach i kolorach
def mTetra(a, b, c, d, coll):
    tetra = list()
    col1, col2, col3, col4 = coll
    face = [a, b, c, col1]; tetra.append(face)
    face = [a, b, d, col2]; tetra.append(face)
    face = [b, c, d, col3]; tetra.append(face)
    face = [c, a, d, col4]; tetra.append(face)
    return tetra


# tu robimy szesciany
def mCube(center, s, coll):
    a = [center[0]-s, center[1]-s, center[2]-s]
    b = [center[0]+s, center[1]-s, center[2]-s]
    c = [center[0]+s, center[1]-s, center[2]+s]
    d = [center[0]-s, center[1]-s, center[2]+s]
    e = [center[0]-s, center[1]+s, center[2]-s]
    f = [center[0]+s, center[1]+s, center[2]-s]
    g = [center[0]+s, center[1]+s, center[2]+s]
    h = [center[0]-s, center[1]+s, center[2]+s]
    cube = list()
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = coll
    # dolna sciana
    face = [a, b, c, col1]; cube.append(face)
    face = [a, d, c, col2]; cube.append(face)
    # prawa sciana
    face = [b, c, g, col3]; cube.append(face)
    face = [b, f, g, col4]; cube.append(face)
    # tylnia sciana
    face = [b, f, e, col5]; cube.append(face)
    face = [b, a, e, col6]; cube.append(face)
    # lewa sciana
    face = [h, a, e, col7]; cube.append(face)
    face = [h, f, e, col8]; cube.append(face)
    # przednia sciana
    face = [d, c, g, col9]; cube.append(face)
    face = [d, h, g, col10]; cube.append(face)
    # gorna sciana
    face = [f, e, h, col11]; cube.append(face)
    face = [f, g, h, col12]; cube.append(face)
    return cube


# deklaracja kolorow
t_col = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]
c_col = np.zeros([12, 3])
for i in range(12):
    c_col[i, 0] = 1

# deklaracje czworościanów (wierzchołki i kolory ścian)
tetra1 = mTetra([-1/2, -1/2, 0], [2/2, 0, 0], [0, 2/2, 0], [0, 0, 1.3], t_col)

# tu mamy szesciany
cube1 = mCube([2, 2, 0], 1, c_col)
cube2 = mCube([-5, -5, 0], 1, c_col)
cube3 = mCube([5, 5, 0], 1, c_col)
cube4 = mCube([5, -5, 0], 1, c_col)
cube5 = mCube([-5, 5, 0], 1, c_col)


# rysowanie listy trójkątów
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
    global eye, orient, up, tetra1
    if key == b"e":
        eye = eye + 3*(orient * np.array([0.1, 0.1, 0.1]))
    if key == b"q":
        eye = eye - 3*(orient * np.array([0.1, 0.1, 0.1]))
    if key == b"a":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[np.cos(0.1), 0, np.sin(0.1)], [0, 1, 0], [-np.sin(0.1), 0, np.cos(0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
    if key == b"d":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[np.cos(-0.1), 0, np.sin(-0.1)], [0, 1, 0], [-np.sin(-0.1), 0, np.cos(-0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
    if key == b"s":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[1, 0, 0], [0, np.cos(0.1), -np.sin(0.1)], [0, np.sin(0.1), np.cos(0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
        up = np.matmul(rot, np.array([0, 1, 0]))
        up = np.matmul(inverse, up)
    if key == b"w":
        right = np.cross(up, orient)
        right = right / np.linalg.norm(right)
        inverse = np.array([right, up, orient])
        inverse = np.transpose(inverse)
        rot = np.array([[1, 0, 0], [0, np.cos(-0.1), -np.sin(-0.1)], [0, np.sin(-0.1), np.cos(-0.1)]])
        orient = np.matmul(rot, np.array([0, 0, 1]))
        orient = np.matmul(inverse, orient)
        up = np.matmul(rot, np.array([0, 1, 0]))
        up = np.matmul(inverse, up)

    if key == b"i":  # ruch czworoscianem
        for triangle in tetra1:
            for i in triangle[:3]:
                i[1] += 0.1
                i[1] = np.around(i[1], 2)
    if key == b"k":
        for triangle in tetra1:
            for i in triangle[:3]:
                i[1] -= 0.1
                i[1] = np.around(i[1], 2)
    if key == b"j":
        for triangle in tetra1:
            for i in triangle[:3]:
                i[0] -= 0.1
                i[0] = np.around(i[0], 2)
    if key == b"l":
        for triangle in tetra1:
            for i in triangle[:3]:
                i[0] += 0.1
                i[0] = np.around(i[0], 2)
    if key == b"u":
        for triangle in tetra1:
            for i in triangle[:3]:
                i[2] -= 0.1
                i[2] = np.around(i[2], 2)
    if key == b"o":
        for triangle in tetra1:
            for i in triangle[:3]:
                i[2] += 0.1
                i[2] = np.around(i[2], 2)
    if key == b"n":
        for triangle in tetra1:
            for i in triangle[:3]:
                pass


# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1:  # max 10 ramek / s
        return False
    tick = ltime
    return True

# sprawdze strone po ktorej punkt p sie znajduje
def strona(a, b, c, p):
    st = np.array([[a[0] - p[0], a[1] - p[1], a[2] - p[2]],
                   [b[0] - p[0], b[1] - p[1], b[2] - p[2]],
                   [c[0] - p[0], c[1] - p[1], c[2] - p[2]]])
    return np.linalg.det(st)

# sprawdze czy trójkąt jest punktem
def isPoint(a, b, c):
    if a[0] == b[0] == c[0] and a[1] == b[1] == c[1] and a[2] == b[2] == c[2]:
        return True
    else:
        return False

# sprawdze czy trójkat jest odcinkiem
def isSection(a, b, c):
    test = np.cross(np.array(b) - np.array(a), np.array(c) - np.array(a))
    return True if test[0] == 0 and test[1] == 0 and test[2] == 0 else False


# sprawdze czy "trójkąt" jest trójkątem
def isTriangle(a, b, c):
    return True if not isPoint(a, b, c) and not isSection(a, b, c) else False


# sciana kodu sprawdzająca przecinanie się odcinków
def crossingSectionWithSection(a, b, c, d):
    """Function checks if given sections (a, b) and (c, d) cross"""

    # Funkcje pomocnicze
    def calculate_t1(a, b, c):
        if b[0] == a[0] and b[1] != a[1]:
            return calculate_t2(a, b, c)
        elif b[0] == a[0] and b[1] == a[1]:
            return calculate_t3(a, b, c)
        else:
            return (c[0] - a[0])/(b[0] - a[0])
    def calculate_t2(a, b, c):
        if b[1] == a[1] and b[0] != a[0]:
            return calculate_t1(a, b, c)
        elif b[1] == a[1] and b[0] == a[0]:
            return calculate_t3(a, b, c)
        else:
            return (c[1] - a[1])/(b[1] - a[1])
    def calculate_t3(a, b, c):
        if b[2] == a[2] and b[0] != a[0]:
            return calculate_t1(a, b, c)
        elif b[2] == a[2] and b[0] == a[0]:
            return calculate_t2(a, b, c)
        else:
            return (c[2] - a[2])/(b[2] - a[2])
    def calculate_k1(a, b, c, d):
        if b[0] == a[0] and b[1] != a[1]:
            return calculate_t2(a, b, c)
        elif b[0] == a[0] and b[1] == a[1]:
            return calculate_t3(a, b, c)
        else:
            return (d[0] - a[0])/(b[0] - a[0])
    def calculate_k2(a, b, c, d):
        if b[1] == a[1] and b[0] != a[0]:
            return calculate_t1(a, b, c)
        elif b[1] == a[1] and b[0] == a[0]:
            return calculate_t3(a, b, c)
        else:
            return (d[1] - a[1])/(b[1] - a[1])
    def calculate_k3(a, b, c, d):
        if b[2] == a[2] and b[0] != a[0]:
            return calculate_t1(a, b, c)
        elif b[2] == a[2] and b[0] == a[0]:
            return calculate_t3(a, b, c)
        else:
            return (d[2] - a[2])/(b[2] - a[2])


    # Sprawdzenie czy odcinki nie są punktami i są równoległe
    if not isPoint(a, b, b) and not isPoint(c, d, d) and np.cross(np.array(b) - np.array(a), np.array(d) - np.array(c)).all() == 0:
        t1 = calculate_t1(a, b, c)
        t2 = calculate_t2(a, b, c)
        t3 = calculate_t3(a, b, c)
        k1 = calculate_k1(a, b, c, d)
        k2 = calculate_k2(a, b, c, d)
        k3 = calculate_k3(a, b, c, d)
        t = (t1, t2, t3)
        k = (k1, k2, k3)
        if (not (b[0] == a[0] and (c[0] != a[0] or d[0] != a[0]))
            and not (b[1] == a[1] and (c[1] != a[1] or d[1] != a[1]))
            and not (b[2] == a[2] and (c[2] != a[2] or d[2] != a[2]))
            and t1 == t2 == t3
            and k1 == k2 == k3
            and (
                   min(min(t), min(k)) == 0
                or min(min(t), min(k)) == 1
                or max(max(t), max(k)) == 0
                or max(max(t), max(k)) == 1
            )
        ):
            return True
        else:
            return False
    elif not isPoint(a, b, b) and not isPoint(c, d, d) and np.cross(np.array(b) - np.array(a), np.array(d) - np.array(c)).all() != 0:
        t = s = 0
        bxax = b[0] - a[0]
        byay = b[1] - a[1]
        bzaz = b[2] - a[2]
        cxax = c[0] - a[0]
        cxdx = c[0] - d[0]
        cyay = c[1] - a[1]
        cydy = c[1] - d[1]
        czaz = c[2] - a[2]
        czdz = c[2] - d[2]
        if (bxax*cydy) != (cxdx*byay):
            t = ((cxdx*cyay) - (cxax*cydy))/((bxax*cydy)-(cxdx*byay))
            s = ((bxax*cyay) - (cxax*byay))/((bxax*cydy)-(cxdx*byay))
        elif (bxax*czdz) != (cxdx*bzaz):
            t = ((cxdx*czaz) - (cxax*czdz))/((bxax*czdz)-(cxdx*bzaz))
            s = ((bxax*czaz) - (cxax*bzaz))/((bxax*czdz)-(cxdx*bzaz))
        elif (byay*czdz) != (cydy*bzaz):
            t = ((cydy*czaz) - (cyay*czdz))/((byay*czdz)-(cydy*bzaz))
            s = ((byay*czaz) - (cyay*bzaz))/((byay*czdz)-(cydy*bzaz))
        # Sprawdzanie przecinania
        return True if t == s else False
    return False


# sprawdze czy dany odcinek znajduje sie w trójkącie
def sectionInTriangle(a, b, d, e, f):
    if isSection(a, b, b) and isTriangle(d, e, f):
        return True if pointInTriangle(d, e, f, a) and pointInTriangle(d, e, f, b) else False
    else:
        return False


# sprawdze czy punkt jest w trójkącie
def pointInTriangle(a, b, c, p):
    alpha = beta = 0
    bxax = b[0] - a[0]
    byay = b[1] - a[1]
    bzay = b[2] - a[1]
    bzaz = b[2] - a[2]
    cxax = c[0] - a[0]
    cyay = c[1] - a[1]
    czaz = c[2] - a[2]
    pxax = p[0] - a[0]
    pyay = p[1] - a[1]
    pzaz = p[2] - a[2]
    # Calculate alpha & beta
    if (bxax*cyay) != (cxax*byay):
        alpha = ((pxax*cyay) - (cxax*pyay))/((bxax*cyay)-(cxax*byay))
        beta = ((bxax*pyay) - (pxax*byay))/((bxax*cyay)-(cxax*byay))
    elif (bxax*czaz) != (cxax*bzaz):
        alpha = ((pzaz*cxax) - (czaz*pxax))/((bxax*czaz)-(cxax*bzaz))
        beta = ((pzaz*bxax) - (bzaz*pxax))/((bxax*czaz)-(cxax*bzaz))
    elif (bzay*czaz) != (cyay*bzaz):
        alpha = ((pzaz*cyay) - (czaz*pyay))/((bzay*czaz)-(cyay*bzaz))
        beta = ((pzaz*byay) - (bzaz*pyay))/((bzay*czaz)-(cyay*bzaz))

    # Sprawdzanie przecięcia
    if alpha >= 0 and beta >= 0 and alpha + beta <= 1:
        return True
    else:
        return False


# sprawdze czy dany odcinek koliduje/przecina trójkąt
def crossingSectionWithTriangle(a, b, d, e, f):
    if not isPoint(a, b, b) and not isSection(d, e, f) and strona(d, e, f, a) == 0 and strona(d, e, f, b) == 0:
        if ((pointInTriangle(d, e, f, a) or pointInTriangle(d, e, f, b))
            or crossingSectionWithSection(a, b, d, e)
            or crossingSectionWithSection(a, b, e, f)
            or crossingSectionWithSection(a, b, f, d)
        ):
            return True
    elif not isPoint(a, b, b) and not isSection(d, e, f) and (strona(d, e, f, a) != 0 or strona(d, e, f, b) != 0):
        v = np.cross(np.array(e) - np.array(d), np.array(f) - np.array(d))
        u = np.dot(v, d)
        t = (u - np.dot(v, a))/(np.dot(v, (np.array(b) - np.array(a))))
        p = np.array(a) + t*(np.array(b) - np.array(a))
        if 0 <= t <= 1 and pointInTriangle(d, e, f, p):
            return True
    return False


# sprawdzanie degeneracji
def degeneracja_Troj(a, b, c, d, e, f):
    # Trójkąty są punktami
    if isPoint(a, b, c) and isPoint(d, e, f):
        if a == d:
            return True
        else:
            return False

    # Jeden trójkąt jest punktem, drugi odcinkiem (nie punktem)
    if isPoint(a, b, c) and isSection(d, e, f):
        return pointonline(e - d, f - d, a)

    # Jeden trójkąt jest punktem, drugi trójkątem (nie odcinkiem)
    if isPoint(a, b, c) and not isSection(d, e, f):
        if strona(d, e, f, a) == 0 and pointInTriangle(e, d, f, a):
            return True
        else:
            return False

    # Drugi trójkąt jest punktem, pierwszy odcinkiem (nie punktem)
    if isPoint(d, e, f) and isSection(a, b, c):
        return pointonline(b - a, c - a, d)

    # Drugi trójkąt jest punktem, pierwszy trójkątem (nie odcinkiem)
    if isPoint(d, e, f) and not isSection(a, b, c):
        if strona(a, b, c, d) == 0 and pointInTriangle(a, b, c, d):
            return True
        else:
            return False

    # Trójkąty są odcinkami (ale nie punktami)
    if not(isPoint(a, b, c)) and not(isPoint(d, e, f)) and isSection(a, b, c) and isSection(d, e, f):
        return crossingSectionWithSection(a, b, c, d)

    # Jeden trójkąt jest odcinkiem (ale nie punktem), drugi jest trójkątem (ale nie odcinkiem)
    if not(isPoint(a, b, c) or isPoint(d, e, f)) and not isSection(d, e, f) and isSection(a, b, c):
        return sectionInTriangle(b - a, c - a, d, e, f)

    # Drugi trójkąt jest odcinkiem (ale nie punktem), drugi jest trójkątem (ale nie odcinkiem)
    if not(isPoint(a, b, c) or isPoint(d, e, f)) and not isSection(a, b, c) and isSection(d, e, f):
        return sectionInTriangle(e - d, f - d, a, b, c)

    # Brak degeneracji
    return crossingTriangleWithTriangle(a, b, c, d, e, f)


# kolizja trójkątów co nie chce działac  w 100%
def crossingTriangleWithTriangle(a, b, c, d, e, f):
    sabcd = strona(a, b, c, d)
    sabce = strona(a, b, c, e)
    sabcf = strona(a, b, c, f)
    if (not isSection(a, b, c) and not isSection(d, e, f)
        and sabcd == 0 and sabce == 0 and sabcf == 0):
        if (
            pointInTriangle(d, e, f, a)
            or pointInTriangle(a, b, c, d)
            or crossingSectionWithSection(a, b, d, e)
            or crossingSectionWithSection(b, c, d, e)
            or crossingSectionWithSection(c, a, d, e)
            or crossingSectionWithSection(a, b, e, f)
            or crossingSectionWithSection(b, c, e, f)
            or crossingSectionWithSection(c, a, e, f)
            or crossingSectionWithSection(a, b, f, d)
            or crossingSectionWithSection(b, c, f, d)
            or crossingSectionWithSection(c, a, f, d)
        ):
            return True
    elif not isSection(a, b, c) and not isSection(d, e, f):
        o = m = n = 0
        if sabcd * sabce < 0 and sabcd * sabcf < 0:
            o = d
            m = e
            n = f
        elif sabce * sabcd < 0 and sabce * sabcf < 0:
            o = e
            m = d
            n = f
        elif sabcf * sabcd < 0 and sabcf * sabce < 0:
            o = f
            m = d
            n = e
        else:
            return False
        v = np.cross(np.array(b) - np.array(a), np.array(c) - np.array(a))
        u = np.dot(v, a)
        s = (u - np.dot(v, np.array(o)))/(np.dot(v, (np.array(m) - np.array(o))))
        p = np.array(o) + s*(np.array(m) - np.array(o))
        t = (u - np.dot(v, np.array(o)))/(np.dot(v, (np.array(n) - np.array(o))))
        q = np.array(o) + t*(np.array(n) - np.array(o))
        if crossingSectionWithTriangle(p, q, a, b, c):
            return True
    return False


# sprawdze czy fig1 zawiera sie w fig2 (tworze odcinek miedzy fig i jezeli przetrznie sciane fig1 to sie nie zawiera)
def checkContains(fig1, fig2):
    """
    Function checks if fig1 contains fig2
    Creates section from fig1 middle to fig2 middle.
    If section crosses any wall of fig1 then fig2 is outside fig1 - returns false
    """
    fig1_middle = findMiddle(fig1)
    fig2_middle = findMiddle(fig2)
    crossing = False
    fig1_walls = 4 if len(fig1) == 4 else 12
    for i in range(0, fig1_walls):
        if crossingSectionWithTriangle(fig1_middle, fig2_middle, *fig1[i][:3]):
            crossing = True
    return False if crossing else True


# przeklety obrót punktu w 3d
def rotate(point, p0, phi, v=None):  # obrót punktu - to samo co w poprzedniej liście
    if v is None:
        v = [0, 1, 0]
    v = v / np.linalg.norm(v)
    a, b, c = v[0], v[1], v[2]
    phi = np.radians(phi)

    M = np.array([[a ** 2 * (1 - np.cos(phi)) + np.cos(phi), a * b * (1 - np.cos(phi)) - c * np.sin(phi), a * c * (1 - np.cos(phi)) + b * np.sin(phi)],
                  [a * b * (1 - np.cos(phi)) + c * np.sin(phi), b ** 2 * (1 - np.cos(phi)) + np.cos(phi), b * c * (1 - np.cos(phi)) - a * np.sin(phi)],
                  [a * c * (1 - np.cos(phi)) - b * np.sin(phi), b * c * (1 - np.cos(phi)) + a * np.sin(phi), c ** 2 * (1 - np.cos(phi)) + np.cos(phi)]])
    point -= p0
    point = M @ point.T
    point = point.T + p0
    return point


# pętla wyświetlająca
def display():
    if not cupdate():
        return

    global eye, orient, up
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 100)
    center = eye + orient
    gluLookAt(eye[0], eye[1], eye[2], center[0], center[1], center[2], up[0], up[1], up[2])

    global tetra1, cube1, cube2, cube3, cube4, cube5, t_col, c_col, col
    # reset kolorów
    for i in range(len(tetra1)):
        tetra1[i][3] = t_col[i]
    for i in range(len(cube1)):
        cube1[i][3] = c_col[i]
        cube2[i][3] = c_col[i]
        cube3[i][3] = c_col[i]
        cube4[i][3] = c_col[i]
        cube5[i][3] = c_col[i]

    # test kolizji
    txt = " "
    col = 0
    for t1 in tetra1:
        for t2 in cube1:
            if degeneracja_Troj(t1[0], t1[1], t1[2], t2[0], t2[1], t2[2]):
                txt = "Kolizja z cube1"
                t1[3] = [1,0,1]
                t2[3] = [1,0,1]
                col = 1
    if col == 0:
        for t1 in tetra1:
            for t2 in cube2:
                if degeneracja_Troj(t1[0], t1[1], t1[2], t2[0], t2[1], t2[2]):
                    txt = "Kolizja z cube2"
                    t1[3] = [1, 0, 1]
                    t2[3] = [1, 0, 1]
                    col = 2
    if col == 0:
        for t1 in tetra1:
            for t2 in cube3:
                if degeneracja_Troj(t1[0], t1[1], t1[2], t2[0], t2[1], t2[2]):
                    txt = "Kolizja z cube3"
                    t1[3] = [1, 0, 1]
                    t2[3] = [1, 0, 1]
                    col = 3
    if col == 0:
        for t1 in tetra1:
            for t2 in cube4:
                if degeneracja_Troj(t1[0], t1[1], t1[2], t2[0], t2[1], t2[2]):
                    txt = "Kolizja z cube4"
                    t1[3] = [1, 0, 1]
                    t2[3] = [1, 0, 1]
                    col = 4
    if col == 0:
        for t1 in tetra1:
            for t2 in cube5:
                if degeneracja_Troj(t1[0], t1[1], t1[2], t2[0], t2[1], t2[2]):
                    txt = "Kolizja z cube5"
                    t1[3] = [1, 0, 1]
                    t2[3] = [1, 0, 1]
                    col = 5
    # if col != 0:
    #     for t1 in tetra1:
    #         t1[3] = [1, 0, 0]
    #     if col == 1:
    #         for t2 in cube1:
    #             t2[3] = [1, 0, 1]
    #     if col == 2:
    #         for t2 in cube2:
    #             t2[3] = [1, 0, 1]
    #     if col == 3:
    #         for t2 in cube3:
    #             t2[3] = [1, 0, 1]
    #     if col == 4:
    #         for t2 in cube4:
    #             t2[3] = [1, 0, 1]
    #     if col == 5:
    #         for t2 in cube5:
    #             t2[3] = [1, 0, 1]
        col = 0


    print(txt)
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    dFacelist(tetra1)
    dFacelist(cube1)
    dFacelist(cube2)
    dFacelist(cube3)

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
