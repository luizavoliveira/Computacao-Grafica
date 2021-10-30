from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import png

width = 800.0
height = 600.0
a = 0

class PlyReader():

    def __init__(self, filename, cor=[0, 0, 1]):
        with open(filename, 'r') as file:
            self.end_of_header = 0
            self.n_vertex = 0
            self.n_faces = 0
            self.vertex = []
            self.faces = []
            self.cor = cor

            for i, line in enumerate(file):
                if 'element' in line:
                    if 'vertex' in line:
                        self.n_vertex = int(line.split(' ')[2])
                    if 'face' in line:
                        self.n_faces = int(line.split(' ')[2])
                if 'end_header' in line:
                    self.end_of_header = i
                    break

            #VERTICES
            for i, line in enumerate(file):
                vertex = []
                for n in line.split(' ')[:-1]:
                    vertex.append(float(n))
                self.vertex.append(vertex)
                if i >= self.n_vertex - 1:
                    break

            #FACES
            for i, line in enumerate(file):
                if i >= self.n_faces:
                    break
                faces = []
                for n in line.split(' ')[1:-1]:
                    faces.append(int(n))
                self.faces.append(faces)

            self.gl_list = glGenLists(1)
            glNewList(self.gl_list, GL_COMPILE)
            glFrontFace(GL_CCW)

            for face in self.faces:
                glBegin(GL_POLYGON)
                for vertex in face:
                    glNormal3fv(self.vertex[vertex][0:3])
                    glVertex3fv(self.vertex[vertex][0:3])
                glEnd()
            glEndList()

    def draw(self):
        glCallList(self.gl_list)


def LoadTextures():
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
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo,
                 GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def desenha():
    global a
    global bunny
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glScalef(2, 2, 2)
    glRotatef(-a, 0, 1, 0)
    bunny.draw()
    glPopMatrix()
    glutSwapBuffers()
    if not False:
        a += 1
    return


def InitGL(Width, Height):
    global bunny
    mat_ambient = (0.3, 0.0, 0, 1.0)
    mat_diffuse = (0.0, 0.0, .7, 1.0)
    mat_specular = (0.0, 1.0, 0.0, 1.0)
    mat_shininess = (50,)
    light_position = (3, 3, 3)
    glClearColor(.7, 0.7, 0.7, 1.)
    glShadeModel(GL_SMOOTH)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_MULTISAMPLE)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, Width/Height, 0.1, 100.0)
    glTranslatef(0.0, -0.2, -1)
    bunny = PlyReader('bun_zipper.ply')


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(30, timer, 1)


# PRINCIPAL
if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(int(width), int(height))
    window = glutCreateWindow("Bunny")
    glutDisplayFunc(desenha)
    InitGL(width, height)
    glutTimerFunc(30, timer, 1)
    glutMainLoop()