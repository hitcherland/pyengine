import types
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 cc=80
from pyglet.gl import *

class GameObject(object):
    def __init__(self, position=[0,0,0], rotation = [0,0,0]):
        self.position = [ x for x in position ]
        self.rotation = [ y for y in rotation ]
        self.children = []
        
    def update(self, dt):
        self.onUpdate(dt)
        for child in self.children:
            child.update(dt)
    def onUpdate(self, dt): pass

    def setup(self):
        self.onSetup()
        for child in self.children:
            child.setup()
    def onSetup(self): pass

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[2], 0, 0, 1)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[0], 1, 0, 0)
        self.onDraw()
        for child in self.children:
            child.draw()
        glPopMatrix()
    def onDraw(self): pass

    def override(self,methodname):
        if not hasattr(self, methodname):
            raise Exception('{} does not have method {}'.format(self,
                                                                methodname))
        def override_decorator(function):
            setattr(self, methodname, types.MethodType(function,self))
            return getattr(self, methodname)
        return override_decorator

    def rotate(self, rx, ry, rz):
        self.rotation[0] += rx
        self.rotation[1] += ry
        self.rotation[2] += rz

        self.rotation[0] %= 360
        self.rotation[1] %= 360
        self.rotation[2] %= 360
        
    def __call__(self,methodname):
        return self.override(methodname)
