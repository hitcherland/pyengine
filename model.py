# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 cc=80
from gameobject import GameObject
from pyglet.gl import GL_TRIANGLES

class Mesh(GameObject):
    def __init__(self, batch, vertices=[], indices=[], normals=[], group=None, 
                 **args):
        self.vertices = vertices
        self.indices = indices
        self.normals = normals
        self.batch = batch
        self.vertex_list = None
        self.group = group
        self.update_mesh()
        super(Mesh, self).__init__(**args)

    def update_mesh(self):
        if self.vertex_list:
            self.vertex_list.delete()
        self.vertex_list = self.batch.add_indexed(len(self.vertices)//3,
                                             GL_TRIANGLES,
                                             self.group,
                                             self.indices,
                                             ('v3f/static', self.vertices),
                                             ('n3f/static', self.normals))

    def __del__(self):
        if self.vertex_list is not None: self.vertex_list.delete()

    def onDraw(self):
        super(Mesh,self).onDraw(self)
        self.batch.draw()
        
