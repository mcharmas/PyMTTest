'''
Created on 2010-04-17

@author: orbit
'''
from pymt import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from OpengGL.GLU import *
from pymt.base import runTouchApp

class GL3DPerspective:
    """
    Handy Class for use with python 'with' statement.
    on enter: sets the openGL pojection matrix to a standart perspective projection, enables, lighting, normalizing fo normals and depth test
    on exit: restores matrices and states to what they were before
    """
    def __init__(self, angle=60.0, aspect=4.0/3.0, near=1.0, far=100.0):
        self.angle = angle
        self.aspect = aspect
        self.near = near
        self.far = far

    def __enter__(self):
        #glEnable(GL_LIGHTING)
        #glEnable(GL_LIGHT0)
        #glEnable(GL_NORMALIZE)
        #glEnable( GL_COLOR_MATERIAL )
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluPerspective(self.angle,self.aspect , self.near, self.far)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0.0,0.0,-3.0)


    def __exit__(self, type, value, traceback):
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_DEPTH_TEST)
        #glDisable(GL_LIGHTING)
        #glDisable(GL_LIGHT0)
        #glEnable( GL_COLOR_MATERIAL )
        


class ModelViewer(MTWidget):
    def __init__(self, window, **kargs):
        super(ModelViewer, self).__init__(**kargs)
        self.perspective = GL3DPerspective()
        
        self.rotation_matrix = None;
        self.reset_rotation()
        #self.rotate_model(50,0,0)
        #self.get_root_window()
        window.push_handlers(on_keyboard=self._window_on_keyboard)
        
    def reset_rotation(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.rotation_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        
    def rotate_model(self, x, y, z):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glRotatef(z, 0,0,1)
        glRotatef(x, 0,1,0)
        glRotatef(y, 1,0,0)
        glMultMatrixf(self.rotation_matrix)
        self.rotation_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
            
    def on_draw(self):
        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)               
        
        with DO(self.perspective):
            self.draw()      
    
    def _window_on_keyboard(self, key, scancode=None, unicode=None):
        if key == 276: #left
            self.rotate_model(-5,0,0)
        elif key == 275: #right
            self.rotate_model(5,0,0)
        elif key == 273: #up
            self.rotate_model(0,5,0)
        elif key == 274: #down
            self.rotate_model(0,-5,0)
        elif key == 122: #z
            self.rotate_model(0,0,-5)
        elif key == 120: #x
            self.rotate_model(0,0,5)
        
    def draw(self):
        glMultMatrixf(self.rotation_matrix)
        #glRotatef(70.0, 1,0,0)
        glColor3f(0,0,0)
        self.drawTriangle()
        #self.drawQuad()
        
    def on_resize(self, w, h):
        pass
    
    def drawQuad(self):
        with gx_begin(GL_QUADS):
            glColor3f(1.0,0.0,0.0)
            glVertex3f(-1.0, 1.0, 1.0)
            glVertex3f( 1.0, 1.0, 1.0)
            glVertex3f( 1.0, 1.0,-1.0)
            glVertex3f(-1.0, 1.0,-1.0)
 
            glColor3f(0.0,0.0,1.0)
            glVertex3f(-1.0,-1.0, 1.0)
            glVertex3f(-1.0,-1.0,-1.0)
            glVertex3f( 1.0,-1.0,-1.0)
            glVertex3f( 1.0,-1.0, 1.0)        
    
    def drawTriangle(self): 
        with DO(gx_begin(GL_TRIANGLE_FAN)):
            glColor3f(0,0,1)
            glVertex3f( 0.0, 1.0, 0.0)
            glColor3f(0,1,0)
            glVertex3f(-1.0,-1.0, 0.0)
            glColor3f(1,0,0)
            glVertex3f( 1.0,-1.0, 0.0)            
            glColor3f(0,0,0)
            glVertex3f( 0.0,0.0, -1.0)
            
    
    def on_touch_down(self, touch):
        print "Touched"
  

if __name__ == '__main__':
    mv = ModelViewer(window = getWindow(), size=getWindow().size)
    #mv = ModelViewer(size=(1,1))    

    getWindow().add_widget(mv)
    runTouchApp()