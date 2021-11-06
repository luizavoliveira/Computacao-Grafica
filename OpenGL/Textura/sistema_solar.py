from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import png

width = 1000.0
height = 600.0
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

IDsol = None
IDlua = None
IDterra = None

def carregaTextura(path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    reader = png.Reader(filename=path)
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

    return texture


def polar2Cartesiano(r, t, f):
    x = r*math.cos(t)*math.sin(f)
    y = r*math.sin(t)*math.sin(f)
    z = r*math.cos(f)
    return x, y, z


while t <= t_max:
    fi = fi_min
    while fi <= fi_max:
        x, y, z = polar2Cartesiano(r, t, fi)
        v += [[x, y, z]]
        fi += dfi
    t += dt


def desenhaEsfera(IDtexture,r):
    glBindTexture(GL_TEXTURE_2D, IDtexture)
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
    desenhaEsfera(IDsol,1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(3*math.cos(a),0,3*math.sin(a))
    glRotatef(-90, 1, 0, 0)
    glRotatef(-a, 0, 0, 1)
    desenhaEsfera(IDterra,0.4)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(3*math.cos(a)+0.8*math.cos(a*2),0,3*math.sin(a)+0.8*math.sin(a*2))
    glRotatef(-90, 1, 0, 0)
    glRotatef(-a, 0, 0, 1)
    desenhaEsfera(IDlua,0.1)
    glPopMatrix()

    glutSwapBuffers()
    a += 0.03
    return


def InitGL(Width, Height):
    global IDsol, IDlua, IDterra
    IDsol = carregaTextura('./sol.png')
    IDlua = carregaTextura('./lua.png')
    IDterra = carregaTextura('./terra.png')
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_MULTISAMPLE)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(35, Width/Height, 0.1, 100.0)
    glTranslatef(0.3, -0.7, -10)


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(30, timer, 1)

# PRINCIPAL
if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(int(width), int(height))
    glutCreateWindow("Sistema Solar")
    glutDisplayFunc(desenha)
    InitGL(width, height)
    glutTimerFunc(30, timer, 1)
    glutMainLoop()
    