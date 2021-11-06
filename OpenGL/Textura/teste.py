from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import numpy

class Sphere:

	half_pi = pi/2

	def __init__(self, x, y, z, radius,color = (0,0,0), density = 50, tx = None):
		self.position = (x, y, z)
		self.radius = radius
		self.color =  color
		self.density = density
		self.tx = tx

	def draw(self, rotation = (0,1,1,1), texture_index = None):
		if texture_index is not None:
			self._draw_texturized_sphere(rotation, texture_index)	
		else:
			self._draw_filled_sphere(rotation)		


	def move(self, x, y, z):
		self.position = (self.position[0] + x, self.position[1] + y, self.position[2] + z)


	def move_to (self, x, y, z):
		self.position = (x, y, z)


	def _sphere(self, u, v):
		theta = (u * pi / (self.density - 1)) - self.half_pi
		phi = (v * 2 * pi) / (self.density - 1)

		x = self.radius * cos(theta) * cos(phi)
		y = self.radius * sin(theta)
		z = self.radius * cos(theta) * sin(phi)

		return x, y, z


	def _draw_filled_sphere(self, rotation):
		glPushMatrix()
		
		glTranslatef(*self.position)
		glRotatef(*rotation)

		for i in range(0, self.density):
			glBegin(GL_TRIANGLE_STRIP)
			for j in range(0, self.density):
				# self._setColor(i, j)
				glVertex3fv(self._sphere(i,j))
				glVertex3fv(self._sphere(i - 1,j))
			glEnd()

		glPopMatrix()


	# def _setColor(self, i, j): 
	# 	if i < self.density//2: 
	# 		r = (i) / (self.density /2 - 1)
	# 		g = (i) / (self.density /2 - 1)
	# 		b = (i) / (self.density /2 - 1)
	# 	else:
	# 		r = ((self.density - i) / (self.density /2 - 1)) - 0.08
	# 		g = ((self.density - i) / (self.density /2 - 1)) - 0.08
	# 		b = ((self.density - i) / (self.density /2 - 1)) - 0.08
		
	# 	glColor3f(r + (self.color[0] / 255), g + (self.color[1] / 255), b + (self.color[2] / 255))


	def _draw_texturized_sphere(self, rotation, index):

		glBindTexture(GL_TEXTURE_2D, self.tx.textures[index])

		glPushMatrix()
		
		glTranslatef(*self.position)
		glRotatef(*rotation)

		for i in range(0, self.density):
			glBegin(GL_TRIANGLE_STRIP)
			for j in range(0, self.density):
				glTexCoord2f((self.density - 1 - j)/(self.density - 1), (self.density - 1 - i)/(self.density - 1)); glVertex3fv(self._sphere(i,j))
				glTexCoord2f((self.density - 1 - j)/(self.density - 1), (self.density - 1 - i)/(self.density - 1)); glVertex3fv(self._sphere(i - 1,j))
			glEnd()

		glPopMatrix()	


	def get_orbit_position(self, sphere, distance, angle):	

		x, y, z = sphere.position

		x2 = x + ((sphere.radius + distance) * cos(angle))
		y2 = y + ((sphere.radius + distance) * sin(angle))
		z2 = z 

		return x2, y2, z2



angle = {}
rotation_speed = {}
translation_speed = {}

def set_angle(index, rotation = (0,0), translation = (0,0)):
		angle[index] = {
			'rotation': rotation[0],
			'translation': translation[0]
		}
		rotation_speed[index] = rotation[1]
		translation_speed[index] = translation[1]


def rotate(name):
	global angle
	angle[name]['rotation'] += rotation_speed[name]
	angle[name]['translation'] += translation_speed[name]

sun = Sphere(0,0,0,1, color = (160, 100,  -300))
earth = Sphere(4,0,0,0.3, color = (0, 0, 200))
moon = Sphere(4.8,0,0,0.1, color = (200, 200, 200))


def draw():

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	sun.draw(rotation = (angle['sun']['translation'],1,1,1))
	rotate('sun')
	
	earth.draw(rotation = (angle['earth']['translation'],1,1,1))
	moon.draw(rotation = (angle['moon']['translation'],1,1,1))

	pos_earth = earth.get_orbit_position(sun, 3, angle['earth']['rotation'])
	earth.move_to(*pos_earth)
	rotate('earth')

	pos_moon = moon.get_orbit_position(earth, 0.5, angle['moon']['rotation'])
	moon.move_to(*pos_moon)
	rotate('moon')

	glutSwapBuffers()

def timer(i):
	glutPostRedisplay()
	glutTimerFunc(50,timer,1)

if __name__ == '__main__':
	set_angle('sun', rotation = (0,0.1), translation = (0,0.9))
	set_angle('earth', rotation = (0,0.02), translation = (0,0.9))
	set_angle('moon', rotation = (0,0.1), translation = (0,0.2))
	
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
	glutInitWindowSize(1000,800)
	glutCreateWindow('Solar System')
	glutDisplayFunc(draw)
	glEnable(GL_MULTISAMPLE)
	glEnable(GL_DEPTH_TEST)
	glClearColor(0.,0.,0.,1.)
	gluPerspective(45,800.0/600.0,0.1,100.0)
	glTranslatef(0.0,0.0,-15)
	glutTimerFunc(50,timer,1)
	glutMainLoop()