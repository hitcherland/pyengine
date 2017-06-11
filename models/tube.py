# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 cc=80
from ..model import Mesh 
from math import pi, sin, cos
import numpy
from operator import sub

def GenerateRotationMatrix(rotation, ux, uy, uz):
    cos_t = cos(rotation)
    mcos_t = 1 - cos_t
    sin_t = sin(rotation)
    msin_t = 1 - sin_t
    return numpy.array([
        [ 
          cos_t + ux * ux * mcos_t,
          ux * uy * mcos_t - uz * sin_t,
          ux * uz * mcos_t + uy * sin_t,
        ],
        [ 
          uy * ux * mcos_t + uz * sin_t,
          cos_t + uy * uy * mcos_t,
          uy * uz * mcos_t - ux * sin_t,
        ],
        [ 
          uz * ux * mcos_t - uy * sin_t,
          uz * uy * mcos_t + ux * sin_t,
          cos_t + uz * uz * mcos_t,
        ],
    ])

class Tube(Mesh):
    list = None

    def __init__(self, path, radius=1, slices=16, **args):
        vertices = []
        normals = []
        indices = []

        u_step = 2 * pi / (slices - 1)
        l = m = 0

        for p,q in [ (path[i],path[i+1]) for i in range(len(path)-1)]:
            vec = map(sub,p,q)
            if numpy.linalg.norm(vec) != 0:
                vec = numpy.array([ e / numpy.linalg.norm(vec) for e in vec ])
            else:
                vec = numpy.array(vec)
            
            normal = numpy.array([-vec[1] if vec[0] != 0 else 1,
                                   vec[0],
                                   0]) 
            u = 0

            for i in range(slices):
                R = GenerateRotationMatrix(u, *vec)

                rnormal = normal.dot(R)
                offset = [ radius * e for e in rnormal]

                vertex_p = numpy.add(p, offset)
                vertex_q = numpy.add(q, offset)

                vertices.extend(vertex_p)
                normals.extend(rnormal)

                vertices.extend(vertex_q)
                normals.extend(rnormal)

                index = [ 2 * m * (slices + 0) + (l + o) % (slices * 2) \
                          for o in [ 0, 1, 2, 3, 2, 1]
                        ]
        
                indices.extend(index)
                l += 2
                u -= u_step
            m += 1

        m = 0
        for p,q in [ (path[i],path[i+1]) for i in range(len(path)-1)]:
            for i in range(1,slices-1):
                l = 2 * i + 2 * m * slices
                index = [ 2 * m * slices ] + [ 2 * m * (slices + 0) + (l + o) % (slices * 2) \
                          for o in [ 0, 2 ]
                        ]
                indices.extend(index) 
                index = [ 2 * m * slices + 1 ] + [ 2 * m * (slices + 0) + (l + o) % (slices * 2) \
                          for o in [ 3, 1 ]
                        ]
                indices.extend(index) 
            m += 1

        super(Tube,self).__init__(vertices = vertices,
                                   indices = indices,
                                   normals = normals,
                                   **args)
