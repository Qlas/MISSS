from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import ctypes
import math
windowWidth = 800
windowHeight = 600
pos_cam = np.array([0.0,0.0,10.0])
front = np.array([0.0,0.0,-1.0])
pos=[0.0,0.0,-20.0]
up = np.array([0.0, 1.0, 0.0])
yaw = -90
pitch = 0
lastX = 800 / 2
lastY = 800 / 2
firstmouse = 1
mousex = windowWidth/2
mousey = windowHeight/2
obr_os = 0
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
    # print(M)

    for punkt in pkt:                   # przesuniecie na srodek
        punkt[0] -= srodek[0]
        punkt[1] -= srodek[1]
        punkt[2] -= srodek[2]

    for i in range(len(pkt)):           # obrot
        pkt[i] = np.matmul(M, pkt[i])

    for punkt in pkt:                   # powrot na miejsce
        punkt[0] += srodek[0]
        punkt[1] += srodek[1]
        punkt[2] += srodek[2]

    punkt = [                           # rysowanie trojkatow
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
        1, 1, 1,                        # trojkat 1 start
        1, 1, 1,
        1, 1, 1,                        # trojkat 1 end
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

def mouseMotion(x, y):
    global firstmouse, lastX, lastY, yaw, pitch, front

    mousex = 0 if x < 0 else windowWidth if x > windowWidth else x
    mousey = 0 if y < 0 else windowHeight if y > windowHeight else y
    # if firstmouse == 1:
    #     firstmouse = 0
    #     lastX = mousex
    #     lastY = mousey
    xoffset = mousex-lastX
    yoffset = lastY-mousey
    lastX = mousex
    lastY = mousey
    sensitivity = 0.1
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    if pitch > 89:
        pitch = 89
    if pitch < -89:
        pitch = -89
    fro = np.array([0.0, 0.0, 0.0])
    fro[0] = np.cos(np.radians(yaw) * np.cos(np.radians(pitch)))
    fro[1] = np.sin(np.radians(pitch))
    fro[2] = np.sin(np.radians(yaw) * np.cos(np.radians(pitch)))

    front = normalized(fro)

# utworzenie

glutInit(sys.argv)
glutInitWindowPosition(int((ctypes.windll.user32.GetSystemMetrics(0) - windowWidth)/2),
int((ctypes.windll.user32.GetSystemMetrics(1) - windowHeight)/2))
glutInitWindowSize(windowWidth, windowHeight)
glutCreateWindow(b"PyOpenGL")


# shadery
vs = compileShader(vsc, GL_VERTEX_SHADER)
fs = compileShader(fsc, GL_FRAGMENT_SHADER)
sp = glCreateProgram()
glAttachShader(sp, vs)
glAttachShader(sp, fs)
glLinkProgram(sp)
glUseProgram(sp)
glutPassiveMotionFunc(mouseMotion)
# przekazujemy dwa atrybuty do vertex shader-a; pozycję i kolor
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)
glutDisplayFunc(dummy) # niewykorzystana

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

def normalized(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def keyboard(k, x, y):
    global pos_cam, front

    key = k.decode("utf-8")
    if key == 'e':
        pos_cam += front
    elif key == 'q':
        pos_cam -= front
    elif key == 'a':
        pos_cam -= normalized(np.cross(front, up))
    elif key == 'd':
        pos_cam += normalized(np.cross(front, up))
    elif key == 'w':
        pos_cam[1] += 1
    elif key == 's':
        pos_cam[1] -= 1

def perspective(fov, aspect, near, far):
    n, f = near, far
    t = np.tan((fov * np.pi / 180) / 2) * near
    b = - t
    r = t * aspect
    l = b * aspect

    return np.array((
        ((2*n)/(r-l),           0,           0,  0),
        (          0, (2*n)/(t-b),           0,  0),
        ((r+l)/(r-l), (t+b)/(t-b), (f+n)/(n-f), -1),
        (          0,           0, 2*f*n/(n-f),  0)))





def look_at(pos_cam, front, up):
    direction = normalized(pos_cam - front)
    right = np.cross(up, direction)
    up_ca = np.cross(direction, right)
    x = - right.dot(pos_cam)
    y = - up_ca.dot(pos_cam)
    z = - direction.dot(pos_cam)

    return np.array(((right[0], up_ca[0], direction[0], 0),
                     (right[1], up_ca[1], direction[1], 0),
                     (right[2], up_ca[2], direction[2], 0),
                     (x, y, z, 1)))
def create_mvp():
    fov, near, far = 45, 0.1, 100
    projection = perspective(fov, float(windowWidth/windowHeight), near, far)
    view = look_at(pos_cam, pos_cam + front, up)
    model = np.identity(4, float)
    mvp = model @ view @ projection
    return mvp.astype(np.float32)


while True:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # czyszczenie sceny
    glutKeyboardFunc(keyboard)
    cube1 = szescian(2, [0, 0, 0.0], obr_os, [1, 1, 1])
    cube2 = szescian(2, [7, 0, 10.0], obr_os, [0, 1, 0])
    cube3 = szescian(2, [-7, 7, -20.0], obr_os, [0, 0, 1])

    punkty = cube1[0] + cube2[0] + cube3[0]
    kolory = cube1[1] + cube1[1] + cube3[1]

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
    obr_os += 0.005
    # print(pitch)
    # print(yaw)