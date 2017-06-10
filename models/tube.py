# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 cc=80
from ..model import Mesh 
from math import pi, sin, cos

class Tube(Mesh):
    list = None

    def __init__(self, path, radius=1, slices=16, group=None, **args):
        vertices = []
        normals = []

        u_step = 2 * pi / (slices - 1)
        for p in path:
            u = 0
            for i in range(slices):
                cos_u = cos(u)
                sin_u = sin(u)
                x = p[0] + radius * cos_u 
                y = p[1] + radius * sin_u 
                z = p[2] + 0
                nx = cos_u
                ny = sin_u
                nz = 0

                vertices.extend([x, y, z])
                normals.extend([nx, ny, nz])
                u += u_step
             
        # Create a list of triangle indices.
        indices = []
        for i in range(slices - 1):
            indices.extend([i, i + slices + 1, i + slices, ])
            indices.extend([i, i + 1, i + slices + 1])

        print vertices

        super(Tube,self).__init__(vertices = vertices,
                                   indices = indices,
                                   normals = normals,
                                   **args)
