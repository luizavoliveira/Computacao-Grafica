from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

width = 1000
height = 800
x0 = -1
xn = 1
y0 = -1
yn = 1
n = 50
dx = (xn - x0)/n
dy = (yn - y0)/n
a = 0

def f(x,y):
    return x**3+y**3

def cor(t, c1 = np.array([1,0,1]), c2 = np.array([0,0,1])):
    return c1 + t*(c2 - c1)    

def superficie():
    y = y0
    for i in range(n):
        x = x0
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(n): 
            glColor3fv(cor(j/(n-1)))
            glVertex3f(x, y, f(x, y))
            glVertex3f(x, y + dy, f(x, y + dy))
            x += dx
        glEnd()
        y += dy

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(10,timer,1)

def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(a,0,1,0)
    glScalef(2,2,2)
    superficie()
    glPopMatrix()
    glutSwapBuffers()
    a += 1
    return

# PRINCIPAL
if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(width,height)
    glutCreateWindow("Funcao Implicita")
    glutDisplayFunc(desenha)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(80,width/height,0.1,100.0)
    glTranslatef(0.0,0.0,-8)
    glutTimerFunc(10,timer,1)
    glRotatef(50,2,2,1)
    glutMainLoop()