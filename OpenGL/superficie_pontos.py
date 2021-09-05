from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

x0 = -1
xn = 1

y0 = -1
yn = 1

n = 50
dx = (xn - x0)/n
dy = (yn - y0)/n

def f2(x,y):
    # Paraboloide Circular
    return x**2+y**2

def f(x,y):
    # Paraboloide Circular
    return x**2-y**2


def desenhaSuperficie():
    glBegin(GL_POINTS)
    
    y = y0
    
    for i in range(n):
        x = x0
        for j in range(n):    
            z = f(x, y)
            glVertex3f(x, y, z)
            x += dx
        y += dy

    glEnd()

a = 0

def desenhaSuperficie2():
    glBegin(GL_POINTS)
    
    y = y0
    
    for i in range(n):
        x = x0
        for j in range(n):    
            z = f2(x, y)
            glVertex3f(x, y, z)
            x += dx
        y += dy

    glEnd()

def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    glTranslate(-3, 3, 0)
    glRotatef(-a,1,0,0)
    desenhaSuperficie()
    
    glPopMatrix()
    glPushMatrix()

    glTranslate(3, -3, 0)
    glRotatef(-a,1,0,0)
    desenhaSuperficie2()
    
    glPopMatrix()
    glutSwapBuffers()
    a += 1
 
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

# PROGRAMA PRINCIPAL
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800,600)
glutCreateWindow("Superficie")
glutDisplayFunc(desenha)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)
gluPerspective(45,800.0/600.0,0.1,100.0)
glTranslatef(0.0,0.0,-15)
glutTimerFunc(50,timer,1)
glutMainLoop()
