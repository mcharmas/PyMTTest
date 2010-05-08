from pymt import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from OpengGL.GLU import *
from pymt.base import runTouchApp
from ModelViewer import ModelViewer
from pymt.ui.widgets.button import MTButton
import sys

class TriangleModel (ModelViewer):
    def __init__(self, window, **kargs):
        super(TriangleModel, self).__init__(window, **kargs)

    def draw(self):
        with DO(gx_begin(GL_TRIANGLE_FAN)):
            glColor3f(0,0,1)
            glVertex3f( 0.0, 1.0, 0.0)
            glColor3f(0,1,0)
            glVertex3f(-1.0,-1.0, 0.0)
            glColor3f(1,0,0)
            glVertex3f( 1.0,-1.0, 0.0)            
            glColor3f(0,0,0)
            glVertex3f( 0.0,0.0, -1.0)
             

if __name__ == '__main__':    
    tm = TriangleModel(window = getWindow(), size=getWindow().size)
    getWindow().add_widget(tm)
    button = MTButton(label = 'Exit')
    @button.event
    def on_press(*largs):
        sys.exit(0)
    getWindow().add_widget(button)
    runTouchApp()