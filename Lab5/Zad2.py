from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import ctypes
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
hh = 0


def szescian(dlugoscboku, srodek, kat, os, przesuniecie_osi, rotx=0, roty=0, rotz=0):
    pkt = [[srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku]]
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
    # print(pkt[6]) # prawy gorny przedni
    # print(pkt[7]) # lewy gorny przedni

    pkt[7][0] += hh
    pkt[6][0] += hh
    pkt[5][0] += hh
    pkt[4][0] += hh

    pkt[0][0] -= hh
    pkt[1][0] -= hh
    pkt[2][0] -= hh
    pkt[3][0] -= hh





    punkt = [
        pkt[0], pkt[1], pkt[3],
        pkt[1], pkt[2], pkt[3],
        pkt[3], pkt[2], pkt[6],
        pkt[3], pkt[7], pkt[6],
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

    return pkt




def view(pos, front):
    direction = pos - front
    direction = direction / np.linalg.norm(direction)
    up = np.array(([0, 1, 0]))
    right = np.cross(up, direction)
    up_cam = np.cross(direction, right)
    x = -right.dot(pos)
    y = -up_cam.dot(pos)
    z = -direction.dot(pos)

    view_matrix = np.array(
        [
            [right[0], up_cam[0], direction[0], 0],
            [right[1], up_cam[1], direction[1], 0],
            [right[2], up_cam[2], direction[2], 0],
            [x, y, z, 1]
        ]
    )

    return view_matrix


def dummy():
    glutSwapBuffers()

def paint():
    # czyszczenie sceny
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # reakcja na ruch myszką
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutSwapBuffers()

class OP:  # parametry projekcji
    l = -10
    r = 10
    b = -10
    t = 10
    n = 10
    f = 100

def persp(l,r,b,t,n,f):
    ret= np.array(
        [[n / r, 0, 0, 0], [0, -n / t, 0, 0], [0, 0, (-(f + n)) / (f - n), (-2 * f * n) / (f - n)], [0, 0, -1, 0]])
    return ret



def ortho(p, l, r, b, t, n, f):  # projekcja ortograficzna
    ret = [2 / (r - l) * p[0] + (r + l) / (l - r),
        2 / (t - b) * p[1] + (t + b) / (b - t),
        2 / (f - n) * p[2] + (f + n) / (n - f),
           np.array([0,0,-1,0])]
    return ret

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


punkty1 = []

kolory1 = [1.0, 0.0, 0.0,
          0.0, 1.0, 0.0,
          0.0, 0.0, 1.0,
          0.0, 1.0, 1.0]

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
i = -1
pos = np.array([0.0,0.0,1.1])
pitch = 0
yaw = 0
front = np.array([np.cos(np.radians(pitch)) * np.sin(np.radians(yaw)),
                  np.sin(np.radians(pitch)),
                  np.cos(np.radians(pitch)) * np.cos(np.radians(yaw))])

def keyboard(k, x, y):
    global pos

    key = k.decode("utf-8")
    prze = 0.2
    if key == 'w':
        pos +=  front * 0.01
    elif key == 's':
        pos -= front * 0.01

while True:
    hh += 0.01
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # czyszczenie sceny
    glutKeyboardFunc(keyboard)
    # modyfikacja trójkąta
    # punkty[0] += 0.001
    # model, widok, projekcja
    i += 0.0000000001
    views = view(pos, front)
    I = np.array([[1, 0, 0, 1], [0, 0.5, 0, 0], [0, 0, 1, 0], [-0.5, 0, 0, 1]])
    b = persp(OP.l, OP.r, OP.b, OP.t, OP.n, OP.f)
    mvp = np.identity(4, float)
    mvp = np.matmul(I,mvp)
    # pos[0] -= 0.001
    # pos[1] -= 0.001
    # pos[2] += 0.001
    punkty = szescian(1, [0, 0, 0], 0.05, [1, 0, 0], [0, 0, 10])
    kolory = [
        0.583, 0.771, 0.014,
        0.583, 0.771, 0.014,
        0.583, 0.771, 0.014,
        0.583, 0.771, 0.014,
        0.583, 0.771, 0.014,
        0.583, 0.771, 0.014,
        0.597, 0.770, 0.761,
        0.559, 0.436, 0.730,
        0.359, 0.583, 0.152,
        0.597, 0.770, 0.761,
        0.559, 0.436, 0.730,
        0.359, 0.583, 0.152,
        0.014, 0.184, 0.576,
        0.771, 0.328, 0.970,
        0.406, 0.615, 0.116,
        0.014, 0.184, 0.576,
        0.771, 0.328, 0.970,
        0.406, 0.615, 0.116,
        0.997, 0.513, 0.064,
        0.945, 0.719, 0.592,
        0.543, 0.021, 0.978,
        0.997, 0.513, 0.064,
        0.945, 0.719, 0.592,
        0.543, 0.021, 0.978,
        0.055, 0.953, 0.042,
        0.714, 0.505, 0.345,
        0.783, 0.290, 0.734,
        0.055, 0.953, 0.042,
        0.714, 0.505, 0.345,
        0.783, 0.290, 0.734,
        0.517, 0.713, 0.338,
        0.053, 0.959, 0.120,
        0.393, 0.621, 0.362,
        0.517, 0.713, 0.338,
        0.053, 0.959, 0.120,
        0.393, 0.621, 0.362,
    ]


    mvp = views @ b
    mvploc = glGetUniformLocation(sp, "mvp") # pobieranie nazwy z shadera
    glUniformMatrix4fv(mvploc, 1, GL_FALSE, mvp) # przekazywanie do shadera
    # ustawiamy pozycję i kolor
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, punkty)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, kolory)
    glDrawArrays(GL_TRIANGLES, 0, int((len(punkty) + 1) / 3))
    glutSwapBuffers()
    glFlush()
    glutMainLoopEvent()