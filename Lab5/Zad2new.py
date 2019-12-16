from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import ctypes
import math
windowWidth = 800
windowHeight = 600
# vertex shader - kod
vsc = """
        #version 330 core
        layout (location = 0) in vec3 in_pozycja;
        layout (location = 1) in vec3 in_kolor;
        uniform mat4 mvp;
        out vec4 inter_kolor;
        void main() {
        gl_Position = mvp * vec4(in_pozycja.xyz, 1.0);
        inter_kolor = vec4(in_kolor.xyz, 1.0);
        }
        """

# fragment shader - kod
fsc = """
        #version 330 core
        in vec4 inter_kolor;
        layout (location = 0) out vec4 out_kolor;
        void main() {
        out_kolor = vec4(inter_kolor.xyzw);
        }
        """

pos=[0.0,0.0,-1.0]
class OP:  # parametry projekcji
    l = -10
    r = 10
    b = -10
    t = 10
    n = 10
    f = 100

def persp(fovy, aspect, n, f):
    s = 1.0/math.tan(math.radians(fovy)/2.0)
    sx, sy = s / aspect, s
    zz = (f+n)/(n-f)
    zw = 2*f*n/(n-f)
    return np.matrix([[sx,0,0,0],
                      [0,sy,0,0],
                      [0,0,zz,zw],
                      [0,0,-1,0]])

def dummy():
    glutSwapBuffers()

def paint():
    # czyszczenie sceny
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # reakcja na ruch myszką
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutSwapBuffers()

def szescian(dlugoscboku, srodek, phi, v, rotx=0, roty=0, rotz=0):
    pkt = np.array([[srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku]])
    for i in range(8):
        npkt = np.matmul(np.array([[1, 0, 0], [0, np.cos(rotx), -np.sin(rotx)],
                                   [0, np.sin(rotx), np.cos(rotx)]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt
    for i in range(8):
        npkt = np.matmul(np.array([[np.cos(roty), 0, np.sin(roty)], [0, 1, 0],
                                   [-np.sin(roty), 0, np.cos(roty)]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt
    for i in range(8):
        npkt = np.matmul(np.array([[np.cos(rotz), -np.sin(rotz), 0],
                                   [np.sin(rotz), np.cos(rotz), 0], [0, 0, 1]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt


    # print(pkt[0]) #lewy dolny tylni
    # print(pkt[1]) # prawy dolny tylni
    # print(pkt[2]) # prawy gorny tylni
    # print(pkt[3]) # lewy gorny tylni
    # print(pkt[4]) # lewy dolny przedni
    # print(pkt[5]) # prawy dolny przedni
    # print(pkt[6]) # prawy gorny przedniw
    # print(pkt[7]) # lewy gorny przedni
    # hh = 3
    # pkt[7][0] += hh
    # pkt[6][0] += hh
    # pkt[5][0] += hh
    # pkt[4][0] += hh
    #
    # pkt[0][0] -= hh
    # pkt[1][0] -= hh
    # pkt[2][0] -= hh
    # pkt[3][0] -= hh



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
    print(M)

    for punkt in pkt:
        punkt[0] -= srodek[0]
        punkt[1] -= srodek[1]
        punkt[2] -= srodek[2]

    for i in range(len(pkt)):
        pkt[i] = np.matmul(M, pkt[i])

    for punkt in pkt:
        punkt[0] += srodek[0]
        punkt[1] += srodek[1]
        punkt[2] += srodek[2]

    for punkt in pkt:
        punkt[0] += pos[0]
        punkt[1] += pos[1]
        punkt[2] += pos[2]

    punkt = [
        pkt[0], pkt[1], pkt[3],
        pkt[1], pkt[2], pkt[3],
        pkt[3], pkt[2], pkt[6],
        pkt[6], pkt[7], pkt[3],
        pkt[1], pkt[2], pkt[6],
        pkt[1], pkt[5], pkt[6],
        pkt[0], pkt[3], pkt[7],
        pkt[0], pkt[4], pkt[7],
        pkt[0], pkt[1], pkt[5],
        pkt[0], pkt[4], pkt[5],
        pkt[4], pkt[5], pkt[6],
        pkt[4], pkt[7], pkt[6]
    ]
    pkt = []
    for i in punkt:
        for j in i:
            pkt.append(j)

    kolor = [
        1, 1, 1,
        1, 1, 1,
        1, 1, 1,
        1, 1, 1,
        1, 1, 1,
        1, 1, 1,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 1, 1,
        0, 1, 1,
        0, 1, 1,
        0, 1, 1,
        0, 1, 1,
        0, 1, 1,
        1, 1, 0,
        1, 1, 0,
        1, 1, 0,
        1, 1, 0,
        1, 1, 0,
        1, 1, 0,
    ]
    return pkt,kolor




# utworzenie okna
glutInit(sys.argv)
glutInitWindowPosition(int((ctypes.windll.user32.GetSystemMetrics(0) - windowWidth)/2),
int((ctypes.windll.user32.GetSystemMetrics(1) - windowHeight)/2))
glutInitWindowSize(windowWidth, windowHeight)
glutCreateWindow(b"PyOpenGL")

# macierz punktów
punkty = [-1.0, 0.0, 1.0,
           1.0, 0.0, 1.0,
           0.0, 1.0, 1.0]
zplus = 0.0
kolory = [1.0, 0.0, 0.0,
          0.0, 1.0, 0.0,
          0.0, 0.0, 1.0]

# shadery
vs = compileShader(vsc, GL_VERTEX_SHADER)
fs = compileShader(fsc, GL_FRAGMENT_SHADER)
sp = glCreateProgram()
glAttachShader(sp, vs)
glAttachShader(sp, fs)
glLinkProgram(sp)
glUseProgram(sp)

# przekazujemy dwa atrybuty do vertex shader-a; pozycję i kolor
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)
glutDisplayFunc(dummy) # niewykorzystana
obr_os = 0.01
a = 0
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
eyes = [0.0,0.0,1.0]
def keyboard(k, x, y):
    global pos

    key = k.decode("utf-8")
    prze = 0.2
    if key == 'e':
        pos[2] += 0.5
    elif key == 'q':
        pos[2] -= 0.5
    elif key == 'w':
        pos[1] -= 0.2
    elif key == 's':
        pos[1] += 0.2
    elif key == 'a':
        pos[0] += 0.2
    elif key == 'd':
        pos[0] -= 0.2
    elif key == 'j':
        eyes[0] += 0.2
    elif key == 'l':
        eyes[0] -= 0.2
    elif key == 'i':
        eyes[1] -= 0.2
    elif key == 'k':
        eyes[1] += 0.2
def perspective(fov, aspect, near, far):
    n, f = near, far
    t = np.tan((fov * np.pi / 180) / 2) * near
    b = - t
    r = t * aspect
    l = b * aspect
    assert abs(n - f) > 0
    return np.array((
        ((2*n)/(r-l),           0,           0,  0),
        (          0, (2*n)/(t-b),           0,  0),
        ((r+l)/(r-l), (t+b)/(t-b), (f+n)/(n-f), -1),
        (          0,           0, 2*f*n/(n-f),  0)))


def normalized(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


def look_at(eye, target, up):
    zax = normalized(eye - target)
    xax = normalized(np.cross(up, zax))
    yax = np.cross(zax, xax)
    x = - xax.dot(eye)
    y = - yax.dot(eye)
    z = - zax.dot(eye)
    return np.array(((xax[0], yax[0], zax[0], 0),
                     (xax[1], yax[1], zax[1], 0),
                     (xax[2], yax[2], zax[2], 0),
                     (x, y, z, 1)))
def create_mvp():
    fov, near, far = 45, 0.1, 100
    eye = eyes
    target, up = np.array((0,0,0)), np.array((0,1,0))
    projection = perspective(fov, float(windowWidth/windowHeight), near, far)
    view = look_at(eye, target, up)
    model = np.identity(4)
    mvp = model @ view @ projection
    return mvp.astype(np.float32)

while True:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # czyszczenie sceny
    glutKeyboardFunc(keyboard)
    # per = persp(OP.l, OP.r, OP.b, OP.t, OP.n, OP.f)
    cube1 = szescian(2, [0, 0, 0.0], obr_os, [1, 0, 0])
    cube2 = szescian(2, [7, 0, 10.0], obr_os, [0, 1, 0])
    cube3 = szescian(2, [-7, 7, -20.0], obr_os, [0, 0, 1])

    punkty = cube1[0] + cube2[0]+ cube3[0]
    kolory = cube1[1] + cube1[1]+ cube3[1]
    # modyfikacja trójkąta
    # punkty[0] += 0.0001
    # model, widok, projekcja
    mvp = np.identity(4, float)
    per = persp(90.0, float(windowWidth / windowHeight), 10, 100)
    mvp = np.matmul(per, mvp)

    mvp = create_mvp()
    mvploc = glGetUniformLocation(sp, "mvp") # pobieranie nazwy z shadera
    glUniformMatrix4fv(mvploc, 1, GL_FALSE, mvp) # przekazywanie do shadera
    # ustawiamy pozycję i kolor
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, punkty)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, kolory)
    glDrawArrays(GL_TRIANGLES, 0, int((len(punkty) + 1) / 3))
    glutSwapBuffers()
    glFlush()
    glutMainLoopEvent()
    obr_os = 0