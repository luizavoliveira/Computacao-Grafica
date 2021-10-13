from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import png

width = 1000.0
height = 600.0
pause_rotation = False
n= 50
a = 0

v = []
sub = 7
dt = math.pi / sub
fi_min = 0
fi_max = math.pi
dfi = math.pi / (sub * 2)
r = 1
t = 0
t_max = 2*math.pi


def carregaTexturas():
    global texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    reader = png.Reader(filename='./terra.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def polar2Cartesiano(r, t, f):
    x = r*math.cos(t)*math.sin(f)
    y = r*math.sin(t)*math.sin(f)
    z = r*math.cos(f)
    return x, y, z


def paraboloide(x, y):
    return x**2 + y**2


while t <= t_max:
    fi = fi_min
    while fi <= fi_max:
        x, y, z = polar2Cartesiano(r, t, fi)
        v += [[x, y, z]]
        fi += dfi
    t += dt


def myMap(v, b1, t1, b2, t2):
    return (v - b1)/(t1 - b1) * (t2 - b2) + b2


def desenhaFuncao():
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_TRIANGLES)
    t = 0
    while t <= t_max:
        fi = fi_min
        while fi <= fi_max:
            x, y, z = polar2Cartesiano(r, t, fi)
            vertex = [x, y, z]
            glTexCoord2f(t/t_max, fi/fi_max)
            glVertex3fv(vertex)
            glTexCoord2f(t/t_max, (fi+dfi)/fi_max)
            glVertex3fv(polar2Cartesiano(r, t, fi+dfi))
            glTexCoord2f((t+dt)/t_max, (fi+dfi)/fi_max)
            glVertex3fv(polar2Cartesiano(r, t+dt, fi+dfi))
            glTexCoord2f(t/t_max, fi/fi_max)
            glVertex3fv(vertex)
            glTexCoord2f((t+dt)/t_max, fi/fi_max)
            glVertex3fv(polar2Cartesiano(r, t+dt, fi))
            glTexCoord2f((t+dt)/t_max, (fi+dfi)/fi_max)
            glVertex3fv(polar2Cartesiano(r, t+dt, fi+dfi))
            fi += dfi
        t += dt
    glEnd()


def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glRotatef(-a, 0, 0, 1)
    desenhaFuncao()
    glPopMatrix()
    glutSwapBuffers()
    a += 1
    return


def InitGL(Width, Height):
    carregaTexturas()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_MULTISAMPLE)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(35, Width/Height, 0.1, 100.0)
    glTranslatef(0.0, -0.4, -6)


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(30, timer, 1)


# PRINCIPAL
if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(int(width), int(height))
    glutCreateWindow("Esfera com textura")
    glutDisplayFunc(desenha)
    InitGL(width, height)
    glutTimerFunc(30, timer, 1)
    glutMainLoop()