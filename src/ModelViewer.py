# -*- coding: utf-8 -*-
from pymt import *
from OpenGL.GL import *
from OpenGL.GLU import *

class GL3DPerspective:
    """
    Klasa do stosowania z konstrukcją "with". Inicjalizuje scenę opengla a po wykonaniu czyści ją.
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
    """
    Widget wyświetlający model w 3D używjąc OpenGL'a.
    Należy podziedziczyć i nadpisać metodę self.draw która odpowiada za rysowanie modelu.
    """
    def __init__(self, window, **kargs):
        super(ModelViewer, self).__init__(**kargs)
        self.perspective = GL3DPerspective()
        
        self.rotation_matrix = None;
        self.reset_rotation()
        
        self.touches = {}
        self.touch1, self.touch2 = None, None
        self.zoom = 1.0
        self.touch_distance = 0

        window.push_handlers(on_keyboard=self._window_on_keyboard)
        
    def reset_rotation(self):
        """
        Metoda resetuje wszystkie rotacje na scenie.
        """
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.rotation_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        
    def rotate_model(self, x, y, z):
        """
        Obraca scenę (nie model...) w płaszczyznach x,y,z.
        """
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
            self.drawWrapper()      
    
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
    
    def on_touch_down(self, touch):
        self.touches[touch.id] = (touch.x, touch.y)
        print touch.id
        if len(self.touches) == 1:
            self.touch1 = touch.id
        elif len(self.touches) == 2:
            self.touch1, self.touch2 = self.touches.keys()
            v1 = pymt.Vector(self.touches[self.touch1][0], self.touches[self.touch1][1])
            v2 = pymt.Vector(self.touches[self.touch2][0], self.touches[self.touch2][1])
            self.touch_distance = v1.distance(v2)
            
            
    def on_touch_up(self, touch):
        del self.touches[touch.id]
    
    def on_touch_move(self, touch):
        dx, dy, dz = 0, 0, 0
        if self.touches.has_key(self.touch1) and self.touches.has_key(self.touch2):
            v1 = pymt.Vector(self.touches[self.touch1][0], self.touches[self.touch1][1])
            v2 = pymt.Vector(self.touches[self.touch2][0], self.touches[self.touch2][1])
            
            new_touch_dist = v1.distance(v2)
            factor = new_touch_dist / self.touch_distance
            self.touch_distance = new_touch_dist
            self.zoom *= factor
            
            l1 = v1 - v2
            l2 = pymt.Vector(touch.x, touch.y) - v2
            if touch.id != self.touch1: l2 = v1 - pymt.Vector(touch.x, touch.y)
            dz = -l1.angle(l2)                        
            
        else: #tylko jeden palec jest przesuwany
            dx = 200 * (touch.x - self.touches[touch.id][0]) / float(self.width)
            dy = - (200 * (touch.y - self.touches[touch.id][1]) / float(self.width))
            
        self.rotate_model(dx, dy, dz)
        self.touches[touch.id] = (touch.x, touch.y)
        
    def drawWrapper(self):
        glMultMatrixf(self.rotation_matrix)
        glScalef(self.zoom, self.zoom, self.zoom)
        glColor3f(0,0,0)
        self.draw()        
        
    def on_resize(self, w, h):
        pass
    
    def draw(self):
        pass
