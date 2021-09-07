from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import math
import numpy as np

width = 1200
height = 800
n = 50
r1 = 2
r2 = 1
a = 0

def torus(u, v):
    x = (r1+r2 * cos((u*2*pi)/(n-1))) * cos((v*2*pi)/(n-1))
    y = (r1+r2 * cos((u*2*pi)/(n-1))) * sin((v*2*pi)/(n-1))
    z = (r2 * sin((u*2*pi)/(n-1)))
    return x, y, z


def desenhaFuncao():
    for i in range(n):    
        glBegin(GL_TRIANGLE_STRIP)
        glColor3f(1.0, 0.0, 1.0)
        for j in range(n):
            glVertex3fv(torus(i,j))
            glVertex3fv(torus(i - 1,j))
        glEnd()


def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(a,0,1,0)
    desenhaFuncao()
    glPopMatrix()
    glutSwapBuffers()
    a += 1
    return
 

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(30,timer,1)


 #PRINCIPAL
if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(width,height)
    glutCreateWindow("Torus")
    glutDisplayFunc(desenha)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45,width/height,0.1,100.0)
    glTranslatef(0.0,0.0,-15)
    glutTimerFunc(30,timer,1)
    glutMainLoop()
