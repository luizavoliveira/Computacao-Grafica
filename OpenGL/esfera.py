import math
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

width = 1200
height = 800
n = 50
a = 0

v = []
sub = 10
dt = math.pi / sub
fi_min = 0
fi_max = math.pi
dfi = math.pi / (sub * 2)
r = 1
t = 0

def polar2Cartesiano(r, t, f):
    x = r*math.cos(t)*math.sin(f)
    y = r*math.sin(t)*math.sin(f)
    z = r*math.cos(f)
    return x, y, z


while t <= 2*math.pi:
    fi = fi_min
    while fi <= fi_max:
        x, y, z = polar2Cartesiano(r, t, fi)
        v += [[x, y, z]]
        fi += dfi
    t += dt


def desenhaFuncao():
    glBegin(GL_TRIANGLES)
    i = 0
    for vertex in v[:(len(v)-sub*2 - 2)]:
        vs = vertex
        glColor3fv(vs)
        glVertex3fv(vs)
        vs = v[i+1]
        glColor3fv(vs)
        glVertex3fv(vs)
        vs = v[i+(sub*2)+2]
        glColor3fv(vs)
        glVertex3fv(vs)
        vs = vertex
        glColor3fv(vs)
        glVertex3fv(vs)
        vs = v[i+(sub*2)+1]
        glColor3fv(vs)
        glVertex3fv(vs)
        vs = v[i+(sub*2)+2]
        glColor3fv(vs)
        glVertex3fv(vs)
        i += 1
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


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(30, timer, 1)


 #PRINCIPAL
if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA |GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(int(width), int(height))
    glutCreateWindow("Esfera")
    glutDisplayFunc(desenha)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0., 0., 0., 1.)
    gluPerspective(45, width/height, 0.1, 100.0)
    glTranslatef(0.0, -0.4, -6)
    glutTimerFunc(30, timer, 1)
    glutMainLoop()