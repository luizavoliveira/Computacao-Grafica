import math
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

width = 1200
height = 800
n= 50
dx = 0.05
dy = 0.05
a = 0
v = []
r_min = 0
r_max = 1
subdivisoes = 20
dr = .1
dt = math.pi / subdivisoes
r = r_min

def polar2Cartesiana(r, t):
    x = r*math.cos(t)
    y = r*math.sin(t)
    return x, y


def paraboloide(x, y):
    return x**2 + y**2


while r < r_max:
    t = 0
    while t < 2*math.pi:
        x, y = polar2Cartesiana(r, t)
        z = paraboloide(x, y)
        v += [[x, y, z]]
        t += dt
    r += dr


def desenhaFuncao():

    glBegin(GL_TRIANGLES)
    i = 0
    for vertex in v:

        vs = vertex
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = v[i-1]
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = v[max(i-(subdivisoes*2), 0)]
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = vertex
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = v[max(i-(subdivisoes*2), 0)]
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = v[max(i-(subdivisoes*2)+1, 0)]
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
    glutCreateWindow("Paraboloide")
    glutDisplayFunc(desenha)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0., 0., 0., 1.)
    gluPerspective(45, width/height, 0.1, 100.0)
    glTranslatef(0.0, -0.4, -6)
    glutTimerFunc(30, timer, 1)
    glutMainLoop()