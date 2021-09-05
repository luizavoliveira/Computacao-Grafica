from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math

vertices1 = []
vertices2 = []
n = 6
altura = 1
raio = 1
angulo = (2*math.pi)/n
width = 1000
height = 800
a = 0

for i in range(n+1):
    x = raio*math.cos(angulo*i)
    z = raio*math.sin(angulo*i)
    y = 0
    vertices1.append((x,y,z))

for i in range(n+1):
    x = raio*math.cos(angulo*i)
    z = raio*math.sin(angulo*i)
    y = altura
    vertices2.append((x,y,z))


def prisma():

    # BASE
    glBegin(GL_POLYGON)
    glColor3f(0.0, 0.0, 1.0)
    for vertice in vertices1:
        glVertex3fv(vertice)
    glEnd()

    #TOPO
    glBegin(GL_POLYGON)
    glColor3f(0.0, 0.0, 1.0)
    for vertice in vertices2:
        glVertex3fv(vertice)
    glEnd()

    #MEIO
    glBegin(GL_QUAD_STRIP)
    glColor3f(1.0, 0.0, 1.0)
    i = 0
    for vertice in vertices1:
        glVertex3fv(vertice)
        glVertex3fv(vertices2[i])
        i += 1
    glEnd()

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(10,timer,1)

def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(a,0,1,0)
    glScalef(2,2,2)
    prisma()
    glPopMatrix()
    glutSwapBuffers()
    a += 1
    return

# PRINCIPAL
if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(width,height)
    glutCreateWindow("Prisma de N lados")
    glutDisplayFunc(desenha)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.,0.,0.,1.)
    gluPerspective(45,width/height,0.1,100.0)
    glTranslatef(0.0,0.0,-8)
    glutTimerFunc(10,timer,1)
    glRotatef(45,2,1,1)
    glutMainLoop()
